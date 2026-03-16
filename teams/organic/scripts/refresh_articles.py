"""
refresh_articles.py — BabyMania Article Refresh Cycle
=====================================================
מבצע סבב בדיקה ורענון לכל מאמרי הבלוג "news".

בדיקות לכל מאמר:
  1. updated_at — האם לא עודכן מעל 30 יום?
  2. לינקים שבורים — בדיקת כל <a href> במאמר
  3. ביטויי מותג — האם יש לפחות 2 ביטויי מותג?
  4. מילות blacklist — האם יש מילים אסורות מ-brand-voice.md?

למאמרים ישנים (>30 יום):
  - Gemini מוסיף/מעדכן משפט אחד רלוונטי
  - מוודא לפחות 2 ביטויי מותג
  - עדכון ב-Shopify

הרצה:
  python teams/organic/scripts/refresh_articles.py          # dry-run
  python teams/organic/scripts/refresh_articles.py --live   # עדכון אמיתי
"""

import sys
import io
import re
import time
import json
import argparse

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from google import genai

sys.path.insert(0, "C:/Projects/baby-mania-agent")
from shopify_client import get_blog_articles, update_blog_article
from config.settings import GEMINI_API_KEY

# ─── Config ───────────────────────────────────────────────────────────────────

BLOG_ID = 109164036409
STALE_DAYS = 30
TODAY = datetime.now(timezone.utc)

# ביטויי מותג — נדרשים לפחות 2 בכל מאמר
# (Section 13 עדיין לא קיים ב-ORGANIC-CONTENT-KNOWLEDGE.md — משתמשים בנתונים הידועים)
BRAND_TERMS = [
    "BabyMania",
    "babymania",
    "Lino™",
    "LUMI™",
    "BabySleep Pro",
    "babysleep",
    "babymania-il.com",
    "ביימייניה",
    "בייבי מאניה",
]

# מילות blacklist מ-brand-voice.md + ביטויים אסורים מ-ORGANIC-CONTENT-KNOWLEDGE.md §9.7
BLACKLIST = [
    "תינוקכם",
    "מושלם",
    "הכי טוב",
    "פרימיום במיוחד",
    "חוויית שימוש",
    "מוצר חובה",
    "איכות ללא פשרות",
    "קנה עכשיו",
    "מבצע מוגבל",
    "אל תפספסו",
    "Buy now",
    "Shop today",
    "Limited offer",
    "Don't miss out",
]

LINK_CHECK_TIMEOUT = 6  # שניות לכל לינק
LINK_CHECK_HEADERS = {"User-Agent": "Mozilla/5.0 (BabyMania-bot/1.0)"}

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
GEMINI_MODEL = "gemini-2.5-flash"


# ─── Analysis ─────────────────────────────────────────────────────────────────

def is_stale(article):
    """True אם המאמר לא עודכן מעל STALE_DAYS ימים."""
    updated_str = article.get("updated_at") or article.get("published_at", "")
    if not updated_str:
        return True
    updated = datetime.fromisoformat(updated_str.replace("Z", "+00:00"))
    return (TODAY - updated).days > STALE_DAYS


def days_since_update(article):
    updated_str = article.get("updated_at") or article.get("published_at", "")
    if not updated_str:
        return 999
    updated = datetime.fromisoformat(updated_str.replace("Z", "+00:00"))
    return (TODAY - updated).days


def check_broken_links(html):
    """בדוק את כל הלינקים ב-HTML. מחזיר רשימת (url, status_code/error)."""
    soup = BeautifulSoup(html or "", "html.parser")
    broken = []
    checked = set()
    for tag in soup.find_all("a", href=True):
        url = tag["href"].strip()
        if not url or url.startswith("#") or url.startswith("mailto:"):
            continue
        if not url.startswith("http"):
            continue
        if url in checked:
            continue
        checked.add(url)
        try:
            r = requests.head(url, timeout=LINK_CHECK_TIMEOUT, headers=LINK_CHECK_HEADERS, allow_redirects=True)
            if r.status_code >= 400:
                broken.append((url, r.status_code))
        except requests.RequestException as e:
            broken.append((url, str(e)[:60]))
        time.sleep(0.3)
    return broken


def count_brand_terms(html):
    """מחזיר כמה ביטויי מותג שונים מופיעים ב-HTML."""
    text = BeautifulSoup(html or "", "html.parser").get_text()
    found = []
    for term in BRAND_TERMS:
        if term.lower() in text.lower():
            found.append(term)
    return found


def find_blacklist_words(html):
    """מחזיר מילים מה-blacklist שנמצאו ב-HTML."""
    text = BeautifulSoup(html or "", "html.parser").get_text()
    found = []
    for word in BLACKLIST:
        if word.lower() in text.lower():
            found.append(word)
    return found


def analyze_article(article):
    """מחזיר dict עם כל ממצאי הבדיקה למאמר."""
    html = article.get("body_html") or ""
    return {
        "id": article["id"],
        "title": article.get("title", ""),
        "handle": article.get("handle", ""),
        "days_old": days_since_update(article),
        "stale": is_stale(article),
        "broken_links": check_broken_links(html),
        "brand_terms_found": count_brand_terms(html),
        "blacklist_found": find_blacklist_words(html),
    }


# ─── Refresh ──────────────────────────────────────────────────────────────────

def build_refresh_prompt(article, analysis, attempt=1):
    html = article.get("body_html") or ""
    soup = BeautifulSoup(html, "html.parser")
    plain_text = soup.get_text(separator="\n")[:3000]

    brand_terms_missing = len(analysis["brand_terms_found"]) < 2
    brand_note = ""
    if brand_terms_missing:
        brand_note = (
            '\n- חשוב: הוסף התייחסות טבעית אחת ל-BabyMania (למשל: "ב-BabyMania אנחנו ממליצים..." '
            'או "מבחר המוצרים של BabyMania").'
        )

    blacklist_reminder = ""
    if attempt > 1:
        blacklist_reminder = (
            f"\n- ניסיון {attempt}: הניסיון הקודם נכשל כי המשפט הכיל מילה אסורה."
            f"\n- מילים אסורות לחלוטין: {', '.join(BLACKLIST)}"
            "\n- אסור להשתמש בהן בשום אופן."
        )

    return f"""אתה עורך תוכן בכיר של BabyMania — חנות בגדי תינוקות ישראלית.

המאמר הבא לא עודכן {analysis['days_old']} ימים:
כותרת: {article.get('title', '')}

תוכן המאמר (קצר):
{plain_text}

המשימה שלך:
1. הוסף **משפט אחד בלבד** (מקסימום 20 מילה) שמשדרג את המאמר — הוסף אותו בסוף הפסקה הראשונה שמגיע אחרי ה-H2 הראשון.
2. המשפט צריך להיות רלוונטי לנושא המאמר, טבעי, ולא פרסומי.
3. אל תשנה שום דבר אחר במאמר — לא מבנה, לא כותרות, לא קישורים.{brand_note}{blacklist_reminder}

החזר רק את המשפט החדש שיש להוסיף, בלי הסברים נוספים, בלי HTML.
"""


def refresh_article_html(article, analysis):
    """מחזיר את ה-HTML המעודכן עם משפט הרענון. מנסה עד 3 פעמים אם המשפט מכיל blacklist."""
    new_sentence = None
    for attempt in range(1, 4):
        prompt = build_refresh_prompt(article, analysis, attempt=attempt)
        resp = gemini_client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        candidate = resp.text.strip().strip('"').strip("'")
        # בדוק שהמשפט לא מכיל מילות blacklist
        has_blacklist = any(w.lower() in candidate.lower() for w in BLACKLIST)
        if not has_blacklist:
            new_sentence = candidate
            break
        print(f"    ניסיון {attempt} נכשל (blacklist) — מנסה שוב...")
    if not new_sentence:
        # fallback בטוח
        new_sentence = "ב-BabyMania תמצאו מבחר בגדי תינוקות רכים שמתאימים לכל שלב בגדילה."

    html = article.get("body_html") or ""
    soup = BeautifulSoup(html, "html.parser")

    # מצא את הפסקה הראשונה אחרי H2 הראשון
    first_h2 = soup.find(re.compile(r"^h[23]$", re.I))
    if first_h2:
        next_p = first_h2.find_next_sibling("p")
        if next_p:
            next_p.append(f" {new_sentence}")
        else:
            # אם אין p אחרי h2 — הוסף p חדש
            new_tag = soup.new_tag("p")
            new_tag.string = new_sentence
            first_h2.insert_after(new_tag)
    else:
        # fallback — הוסף בסוף ה-body
        last_p = soup.find_all("p")
        if last_p:
            last_p[-1].append(f" {new_sentence}")

    # אם חסרים ביטויי מותג — הוסף אחד בסוף
    brand_found = count_brand_terms(str(soup))
    if len(brand_found) < 2:
        brand_p = soup.new_tag("p")
        brand_p.string = "ב-BabyMania תמצאו מבחר בגדי תינוקות רכים ואיכותיים שמתאימים לכל שלב בגדילה."
        if soup.body:
            soup.body.append(brand_p)
        else:
            soup.append(brand_p)

    return str(soup)


# ─── Report ───────────────────────────────────────────────────────────────────

def print_report(results, live_mode):
    mode_label = "🔴 LIVE" if live_mode else "🟡 DRY-RUN"
    print(f"\n{'='*65}")
    print(f"  BabyMania — Article Refresh Report  |  {mode_label}")
    print(f"  תאריך: {TODAY.strftime('%Y-%m-%d')}  |  blog_id: {BLOG_ID}")
    print(f"{'='*65}\n")

    updated = [r for r in results if r.get("action") == "updated"]
    skipped = [r for r in results if r.get("action") == "skipped"]
    errors  = [r for r in results if r.get("action") == "error"]

    print(f"סה\"כ מאמרים שנבדקו: {len(results)}")
    print(f"  עודכנו:  {len(updated)}")
    print(f"  דולגו:   {len(skipped)}")
    print(f"  שגיאות:  {len(errors)}\n")

    if updated:
        print("─── מאמרים שעודכנו ───────────────────────────────────────")
        for r in updated:
            a = r["analysis"]
            print(f"\n  [{r['article_id']}] {r['title'][:60]}")
            print(f"    ימים ללא עדכון: {a['days_old']}")
            print(f"    ביטויי מותג לפני: {a['brand_terms_found']} ({len(a['brand_terms_found'])})")
            if a["broken_links"]:
                print(f"    ⚠️  לינקים שבורים: {[l[0][:60] for l in a['broken_links']]}")
            if a["blacklist_found"]:
                print(f"    ⚠️  מילות blacklist: {a['blacklist_found']}")
            print(f"    משפט הרענון: \"{r.get('refresh_sentence', '—')}\"")
            print(f"    סטטוס: {'✅ עודכן ב-Shopify' if live_mode else '📝 ימתין לאישור (dry-run)'}")

    if skipped:
        print("\n─── מאמרים שדולגו (עדכניים) ──────────────────────────────")
        for r in skipped:
            a = r["analysis"]
            issues = []
            if a["broken_links"]:
                issues.append(f"לינקים שבורים: {len(a['broken_links'])}")
            if a["blacklist_found"]:
                issues.append(f"blacklist: {a['blacklist_found']}")
            issues_str = " | ".join(issues) if issues else "תקין"
            print(f"  [{r['article_id']}] {r['title'][:55]} — {a['days_old']}d — {issues_str}")

    if errors:
        print("\n─── שגיאות ────────────────────────────────────────────────")
        for r in errors:
            print(f"  [{r['article_id']}] {r['title'][:55]} — {r.get('error', '')}")

    print(f"\n{'='*65}\n")

    # שמור דוח JSON
    report_path = f"C:/Projects/baby-mania-agent/logs/refresh_report_{TODAY.strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"📄 דוח מלא נשמר: {report_path}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BabyMania Article Refresh")
    parser.add_argument("--live", action="store_true", help="עדכן מאמרים ב-Shopify (ברירת מחדל: dry-run)")
    args = parser.parse_args()
    live_mode = args.live

    print(f"\n🔍 שולף מאמרים מבלוג {BLOG_ID}...")
    articles = get_blog_articles(BLOG_ID)
    print(f"✓ נמצאו {len(articles)} מאמרים\n")

    results = []

    for i, article in enumerate(articles, 1):
        title = article.get("title", "")
        art_id = article["id"]
        print(f"[{i}/{len(articles)}] בודק: {title[:55]}...", end=" ", flush=True)

        try:
            analysis = analyze_article(article)
            result = {
                "article_id": art_id,
                "title": title,
                "handle": article.get("handle", ""),
                "analysis": analysis,
            }

            if analysis["stale"]:
                print(f"⏰ {analysis['days_old']}d — מרענן...")
                new_html = refresh_article_html(article, analysis)

                # שלוף את המשפט החדש לדוח
                old_text = BeautifulSoup(article.get("body_html") or "", "html.parser").get_text()
                new_text = BeautifulSoup(new_html, "html.parser").get_text()
                added_chars = new_text.replace(old_text, "").strip()[:120]
                result["refresh_sentence"] = added_chars

                if live_mode:
                    update_blog_article(BLOG_ID, art_id, new_html)
                    result["action"] = "updated"
                    print(f"  ✅ עודכן ב-Shopify")
                else:
                    result["action"] = "updated"
                    result["new_html_preview"] = new_html[:500]
                    print(f"  📝 (dry-run)")
            else:
                result["action"] = "skipped"
                issues = []
                if analysis["broken_links"]:
                    issues.append(f"{len(analysis['broken_links'])} broken links")
                if analysis["blacklist_found"]:
                    issues.append(f"blacklist: {analysis['blacklist_found']}")
                print(f"✓ עדכני ({analysis['days_old']}d)" + (f" ⚠️ {', '.join(issues)}" if issues else ""))

            results.append(result)

        except Exception as e:
            print(f"  ❌ שגיאה: {e}")
            results.append({
                "article_id": art_id,
                "title": title,
                "action": "error",
                "error": str(e),
                "analysis": {},
            })

    print_report(results, live_mode)
    return results


if __name__ == "__main__":
    main()
