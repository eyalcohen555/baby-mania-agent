"""
fix_hub9_images.py
Insert a second contextual image into HUB-9 cluster articles C1-C6.
Insertion point: before the final H2 section ("עוד מדריכי ריבורן").
PUT back to Shopify. Verify image count after each PUT.
"""
import re
import os
import requests

TOKEN = "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"
SHOP = "a2756c-c0.myshopify.com"
BASE = f"https://{SHOP}/admin/api/2024-10"
BLOG_ID = 109164036409
HEADERS = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}
CDN = "https://cdn.shopify.com/s/files/1/0864/9677/2409/files/"
OUTPUT_DIR = r"C:\Projects\baby-mania-agent\output\hub9-reborn"

ARTICLES = [
    {
        "id": "C1",
        "article_id": 686018756921,
        "file": "HUB9_C1_blog_article.html",
        "img_file": "S15487067023948ca8ff9f2cc97f82e2ej.webp?v=1730196949",
        "img_alt": "דגמי ריבורן שונים — השוואה לפני הבחירה",
        "img_caption": "כל דגם מציע שילוב שונה של חומר, גודל ורמת פירוט — כדאי לראות את האפשרויות לפני ההחלטה.",
        "pid_source": "9690182385977",
    },
    {
        "id": "C2",
        "article_id": 686018724153,
        "file": "HUB9_C2_blog_article.html",
        "img_file": "S82026b7c9c3e4423be9717dc12bdb1b2f.webp?v=1730201455",
        "img_alt": "בובת ריבורן בלבוש — מידות ובחירת לבוש נכון",
        "img_caption": "בובת ריבורן בגודל 50–55 ס\"מ מתאימה לבגדי 0–3 חודשים — אותן מידות שמתאימות גם לתינוק אמיתי.",
        "pid_source": "9690247627065",
    },
    {
        "id": "C3",
        "article_id": 686018789689,
        "file": "HUB9_C3_blog_article.html",
        "img_file": "Saba738e477da4bf38bfa7dff166406d7Y.webp?v=1730201453",
        "img_alt": "בובת ריבורן כמתנה — דגם פרמיום לאספן או לילדה",
        "img_caption": "בחירת הדגם הנכון כמתנה תלויה בגיל המקבל ובמטרה — תצוגה, משחק, או אספנות.",
        "pid_source": "9690247659833",
    },
    {
        "id": "C4",
        "article_id": 686018822457,
        "file": "HUB9_C4_blog_article.html",
        "img_file": "S99d5019759394925b7c81461031b864dI.webp?v=1730196949",
        "img_alt": "חומרי ריבורן מקרוב — ויניל וסיליקון: הבדל במגע ובטיפול",
        "img_caption": "ויניל וסיליקון נראים דומים מרחוק, אך מגיבים אחרת לניקוי — הכרת החומר קריטית לשמירה על מצב הבובה.",
        "pid_source": "9690182385977",
    },
    {
        "id": "C5",
        "article_id": 686018855225,
        "file": "HUB9_C5_blog_article.html",
        "img_file": "Sd63426e85d8543f9954ad3b727c758e5A.webp?v=1730196953",
        "img_alt": "ריבורן לאספנים — רמת פירוט ומגע מציאותי גבוהים",
        "img_caption": "ריבורן לאספנים מגיע עם פירוט עורי גבוה, שיניים מורכבות ביד, ומשקל מותאם — מאפיינים שאינם מועדים לשימוש יומיומי של ילד.",
        "pid_source": "9690182451513",
    },
    {
        "id": "C6",
        "article_id": 686018887993,
        "file": "HUB9_C6_blog_article.html",
        "img_file": "Sf461af07570a436aa35fcea274ce8ad2t.webp?v=1730201455",
        "img_alt": "ריבורן 50 ס\"מ — השוואת גודל, חומר ורמת פירוט בין הדגמים",
        "img_caption": "גודל 50 ס\"מ הוא הנפוץ ביותר — מאפשר לבוש בבגדי 0–3 חודשים ומשקל מציאותי.",
        "pid_source": "9690247627065",
    },
]

IMG_BLOCK_TEMPLATE = """
<div class="article-image-mid" style="margin: 2.5rem auto; text-align: center; max-width: 680px;">
  <img
    src="{src}"
    alt="{alt}"
    style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.10);"
    loading="lazy"
  >
  <p style="font-size: 0.85rem; color: #9A8878; margin-top: 0.6rem; text-align: center; direction: rtl;">{caption}</p>
</div>
"""

INSERTION_MARKER = '<h2'  # insert before the LAST h2 (navigation section)


def fetch_body(article_id):
    r = requests.get(
        f"{BASE}/blogs/{BLOG_ID}/articles/{article_id}.json",
        headers={"X-Shopify-Access-Token": TOKEN}, timeout=20
    )
    if r.status_code != 200:
        return None, r.status_code
    return r.json()["article"]["body_html"], 200


def put_body(article_id, body_html):
    r = requests.put(
        f"{BASE}/blogs/{BLOG_ID}/articles/{article_id}.json",
        headers=HEADERS, timeout=30,
        json={"article": {"id": article_id, "body_html": body_html}}
    )
    return r.status_code, r.json().get("article", {})


def count_images(html):
    return len(re.findall(r'<img[^>]+>', html, re.I))


def insert_before_last_h2(html, insertion):
    """Find last <h2 occurrence and insert block before it."""
    positions = [m.start() for m in re.finditer(r'<h2', html, re.I)]
    if not positions:
        return html + insertion
    last_h2 = positions[-1]
    return html[:last_h2] + insertion + html[last_h2:]


print("=" * 68)
print("HUB-9 IMAGE RECOVERY — C1 TO C6")
print("=" * 68)

results = []

for art in ARTICLES:
    print(f"\n[{art['id']}] article_id={art['article_id']}")

    # Fetch current body
    body, status = fetch_body(art["article_id"])
    if body is None:
        print(f"  FETCH FAIL — HTTP {status}")
        results.append({"id": art["id"], "status": "FAIL", "reason": f"fetch HTTP {status}"})
        break

    img_before = count_images(body)
    print(f"  Images before: {img_before}")

    # Verify candidate image not already present
    img_src = CDN + art["img_file"]
    if img_src in body:
        print(f"  SKIP — image already present")
        results.append({"id": art["id"], "status": "SKIP", "img_count": img_before})
        continue

    # Build image block
    img_block = IMG_BLOCK_TEMPLATE.format(
        src=img_src,
        alt=art["img_alt"],
        caption=art["img_caption"],
    )

    # Insert before last H2
    updated_body = insert_before_last_h2(body, img_block)
    img_after = count_images(updated_body)
    print(f"  Images after insertion: {img_after}")

    # Save locally
    local_path = os.path.join(OUTPUT_DIR, art["file"])
    # Read current local file and apply same insertion
    local_html = open(local_path, encoding="utf-8").read()
    updated_local = insert_before_last_h2(local_html, img_block)
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(updated_local)
    print(f"  Local file updated.")

    # PUT to Shopify
    print(f"  [PUT] {art['article_id']}...")
    put_status, put_data = put_body(art["article_id"], updated_body)
    if put_status != 200:
        print(f"  PUT FAIL — HTTP {put_status}")
        results.append({"id": art["id"], "status": "FAIL", "reason": f"PUT HTTP {put_status}"})
        break

    print(f"  PUT PASS — HTTP 200")

    # Verify image count from API response
    verify_html = put_data.get("body_html", "")
    verify_count = count_images(verify_html)
    print(f"  VERIFY: images in live body = {verify_count}")

    results.append({
        "id": art["id"],
        "status": "PASS",
        "img_before": img_before,
        "img_after": verify_count,
        "img_src": img_src,
    })

print("\n" + "=" * 68)
print("SUMMARY")
print("=" * 68)
all_ok = True
for r in results:
    ok = r.get("status") in ("PASS", "SKIP")
    if not ok:
        all_ok = False
    print(f"  {r['id']:4} | {r.get('status','?'):4} | imgs: {r.get('img_before','?')} -> {r.get('img_after','?')}")
print(f"\nFINAL: {'ALL PASS' if all_ok else 'PARTIAL FAIL'}")
