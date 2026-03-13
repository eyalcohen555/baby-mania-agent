"""
Activate staged internal links — v2.
Handles ב-prefix morphology for C1, and adds missing link sentences to C4.
"""

import sys, io, re, time, requests
from shopify_client import _headers, BASE_URL

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BLOG_ID = 109164036409

PILLAR_URL = "https://www.babymania-il.com/blogs/news/how-to-help-baby-sleep-through-the-night"
WHITE_URL  = "https://www.babymania-il.com/blogs/news/white-noise-for-babies"


def fetch_body(article_id):
    resp = requests.get(
        f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json",
        headers=_headers(), timeout=30
    )
    resp.raise_for_status()
    return resp.json()["article"]["body_html"]


def put_body(article_id, body_html):
    resp = requests.put(
        f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json",
        headers=_headers(),
        json={"article": {"id": article_id, "body_html": body_html}},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["article"]


results = []

# ─────────────────────────────────────────────────────────────────────────────
# ARTICLE 2 — white-noise-for-babies (id=681272115513)
# AL-C1-001: wrap "מדריך המלא לשינת תינוקות בלילה" inside "במדריך המלא..."
# ─────────────────────────────────────────────────────────────────────────────
ART2_ID = 681272115513
print("Fetching article 2 (white-noise-for-babies)...")
body2 = fetch_body(ART2_ID)

ANCHOR_C1_001 = "מדריך המלא לשינת תינוקות בלילה"
LINK_TAG_C1_001 = f'<a href="{PILLAR_URL}">{ANCHOR_C1_001}</a>'

if PILLAR_URL in body2:
    status_c1_001 = "ALREADY_ACTIVE"
    print("  AL-C1-001: already active, skipping")
elif ANCHOR_C1_001 in body2:
    body2 = body2.replace(ANCHOR_C1_001, LINK_TAG_C1_001, 1)
    status_c1_001 = "WRAPPED"
    print(f"  AL-C1-001: wrapped")
else:
    status_c1_001 = "NOT_FOUND"
    print(f"  AL-C1-001: WARNING — anchor not found")

results.append({
    "id": "AL-C1-001", "article": "white-noise-for-babies",
    "anchor": ANCHOR_C1_001, "href": PILLAR_URL, "status": status_c1_001,
})

# AL-C1-002 was already wrapped in v1 — just verify
if "baby-sleep-routine" in body2:
    results.append({
        "id": "AL-C1-002", "article": "white-noise-for-babies",
        "anchor": "שגרת שינה קבועה ועקבית",
        "href": "https://www.babymania-il.com/blogs/news/baby-sleep-routine",
        "status": "ALREADY_ACTIVE",
    })
    print("  AL-C1-002: already active (confirmed)")

if status_c1_001 == "WRAPPED":
    print("  PUTting article 2...")
    put_body(ART2_ID, body2)
    time.sleep(1)
    refreshed2 = fetch_body(ART2_ID)
    results[-2]["verified"] = PILLAR_URL in refreshed2
    results[-1]["verified"] = "baby-sleep-routine" in refreshed2
else:
    refreshed2 = body2
    results[-1]["verified"] = "baby-sleep-routine" in body2

# ─────────────────────────────────────────────────────────────────────────────
# ARTICLE 3 — all-in-one-baby-sleep-solution (id=681272246585)
# AL-C4-001: add pillar link sentence after tip-box in #what-is
# AL-C4-002: append white-noise link to first criteria <p>
# ─────────────────────────────────────────────────────────────────────────────
ART3_ID = 681272246585
print("\nFetching article 3 (all-in-one-baby-sleep-solution)...")
body3 = fetch_body(ART3_ID)

# ── AL-C4-001 ────────────────────────────────────────────────────────────────
# Insert after the closing </div> of the tip-box inside #what-is section.
# The tip-box is followed by </article> or the next H2.
# We add a short paragraph before the H2#criteria.
NEW_PARA_C4_001 = (
    f'\n    <p>לבניית שגרת שינה שלמה שתשלים את השימוש במכשיר, '
    f'עיינו ב<a href="{PILLAR_URL}">מדריך המלא לשינת תינוקות בלילה</a>.</p>'
)

# Insert before <h2 id="criteria">
CRITERIA_H2 = '<h2 id="criteria">'
if PILLAR_URL in body3:
    status_c4_001 = "ALREADY_ACTIVE"
    print("  AL-C4-001: already active")
elif CRITERIA_H2 in body3:
    body3 = body3.replace(CRITERIA_H2, NEW_PARA_C4_001 + "\n    " + CRITERIA_H2, 1)
    status_c4_001 = "INSERTED"
    print("  AL-C4-001: inserted paragraph before #criteria")
else:
    status_c4_001 = "NOT_FOUND"
    print("  AL-C4-001: WARNING — criteria anchor not found")

results.append({
    "id": "AL-C4-001", "article": "all-in-one-baby-sleep-solution",
    "anchor": "מדריך המלא לשינת תינוקות בלילה",
    "href": PILLAR_URL, "status": status_c4_001,
})

# ── AL-C4-002 ────────────────────────────────────────────────────────────────
# Append cross-link to first criteria item's <p> (white noise types paragraph).
# Target: the <p> inside first <li> of .criteria-list that mentions "תינוקות שונים"
EXISTING_P_C4_002 = "תינוקות שונים מגיבים אחרת לצפיפות הגל.</p>"
NEW_P_C4_002 = (
    f'תינוקות שונים מגיבים אחרת לצפיפות הגל. '
    f'לסקירה מלאה של ההבדלים, ראו '
    f'<a href="{WHITE_URL}">רעש לבן לתינוקות — האם זה עובד?</a></p>'
)

if WHITE_URL in body3:
    status_c4_002 = "ALREADY_ACTIVE"
    print("  AL-C4-002: already active")
elif EXISTING_P_C4_002 in body3:
    body3 = body3.replace(EXISTING_P_C4_002, NEW_P_C4_002, 1)
    status_c4_002 = "INSERTED"
    print("  AL-C4-002: appended cross-link to criteria item 1")
else:
    status_c4_002 = "NOT_FOUND"
    print("  AL-C4-002: WARNING — target paragraph not found")

results.append({
    "id": "AL-C4-002", "article": "all-in-one-baby-sleep-solution",
    "anchor": "רעש לבן לתינוקות — האם זה עובד?",
    "href": WHITE_URL, "status": status_c4_002,
})

if status_c4_001 in ("INSERTED",) or status_c4_002 in ("INSERTED",):
    print("  PUTting article 3...")
    put_body(ART3_ID, body3)
    time.sleep(1)
    refreshed3 = fetch_body(ART3_ID)
    results[-2]["verified"] = PILLAR_URL in refreshed3
    results[-1]["verified"] = WHITE_URL in refreshed3
else:
    results[-2]["verified"] = PILLAR_URL in body3
    results[-1]["verified"] = WHITE_URL in body3

# ─────────────────────────────────────────────────────────────────────────────
# RESULTS TABLE
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 76)
print("ACTIVATION RESULTS")
print("=" * 76)
print(f"{'ID':<12} {'Article':<34} {'Action':<14} {'Verified'}")
print("-" * 76)
for r in results:
    print(f"{r['id']:<12} {r['article']:<34} {r['status']:<14} {str(r.get('verified', '—'))}")

print()
print("=" * 76)
print("DETAIL")
print("=" * 76)
for r in results:
    print(f"\n  {r['id']}")
    print(f"    Article:  {r['article']}")
    print(f"    Anchor:   {r['anchor']}")
    print(f"    Target:   {r['href']}")
    print(f"    Action:   {r['status']}")
    print(f"    Verified: {r.get('verified', '—')}")
