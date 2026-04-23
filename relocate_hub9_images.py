"""
relocate_hub9_images.py
Move <div class="article-image-mid"> from inside <div class="cluster-nav">
to immediately before <div class="cluster-nav"> in all 6 HUB-9 cluster articles.
"""
import re
import os
import requests

TOKEN = "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"
SHOP = "a2756c-c0.myshopify.com"
BASE = f"https://{SHOP}/admin/api/2024-10"
BLOG_ID = 109164036409
HEADERS_API = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}
OUTPUT_DIR = r"C:\Projects\baby-mania-agent\output\hub9-reborn"

ARTICLES = [
    {"id": "C1", "article_id": 686018756921, "file": "HUB9_C1_blog_article.html"},
    {"id": "C2", "article_id": 686018724153, "file": "HUB9_C2_blog_article.html"},
    {"id": "C3", "article_id": 686018789689, "file": "HUB9_C3_blog_article.html"},
    {"id": "C4", "article_id": 686018822457, "file": "HUB9_C4_blog_article.html"},
    {"id": "C5", "article_id": 686018855225, "file": "HUB9_C5_blog_article.html"},
    {"id": "C6", "article_id": 686018887993, "file": "HUB9_C6_blog_article.html"},
]

ANCHOR_OPEN = '<div class="cluster-nav">'
BLOCK_OPEN = '<div class="article-image-mid"'
BLOCK_CLOSE = "</div>"


def fetch_body(article_id):
    r = requests.get(
        f"{BASE}/blogs/{BLOG_ID}/articles/{article_id}.json",
        headers={"X-Shopify-Access-Token": TOKEN},
        timeout=20,
    )
    if r.status_code != 200:
        return None, r.status_code
    return r.json()["article"]["body_html"], 200


def extract_block(html):
    """Extract the full article-image-mid block. Returns (block_str, start, end)."""
    start = html.find(BLOCK_OPEN)
    if start < 0:
        return None, -1, -1
    # No nested divs inside article-image-mid — first </div> after start is correct
    end = html.find(BLOCK_CLOSE, start)
    if end < 0:
        return None, -1, -1
    end += len(BLOCK_CLOSE)
    return html[start:end], start, end


def relocate(html):
    """
    Remove article-image-mid from its current position inside cluster-nav.
    Re-insert it immediately before <div class="cluster-nav">.
    Returns (new_html, diagnostics).
    """
    diag = {}

    # 1. Find article-image-mid block
    block, b_start, b_end = extract_block(html)
    if block is None:
        return html, {"error": "article-image-mid block not found"}

    diag["block_found_at"] = b_start
    diag["block_len"] = len(block)

    # 2. Find cluster-nav position (before removal)
    cnav_pos = html.find(ANCHOR_OPEN)
    if cnav_pos < 0:
        return html, {"error": "cluster-nav anchor not found"}

    diag["cluster_nav_at"] = cnav_pos
    diag["block_inside_cluster_nav"] = b_start > cnav_pos

    # 3. Remove block from current position
    html_without_block = html[:b_start] + html[b_end:]

    # 4. Find cluster-nav in the cleaned html
    cnav_pos_clean = html_without_block.find(ANCHOR_OPEN)
    if cnav_pos_clean < 0:
        return html, {"error": "cluster-nav not found after block removal"}

    # 5. Insert block immediately before cluster-nav (with newline separation)
    new_html = (
        html_without_block[:cnav_pos_clean]
        + block
        + "\n"
        + html_without_block[cnav_pos_clean:]
    )

    # 6. Verify final positions
    final_block_pos = new_html.find(BLOCK_OPEN)
    final_cnav_pos = new_html.find(ANCHOR_OPEN)
    diag["final_block_at"] = final_block_pos
    diag["final_cnav_at"] = final_cnav_pos
    diag["block_before_cnav"] = final_block_pos < final_cnav_pos
    diag["block_inside_cnav_after"] = (
        final_block_pos > final_cnav_pos
        and final_block_pos < final_cnav_pos + len(ANCHOR_OPEN) + 5000
    )

    return new_html, diag


def count_images(html):
    return len(re.findall(r"<img[^>]+>", html, re.I))


def put_body(article_id, body_html):
    r = requests.put(
        f"{BASE}/blogs/{BLOG_ID}/articles/{article_id}.json",
        headers=HEADERS_API,
        json={"article": {"id": article_id, "body_html": body_html}},
        timeout=30,
    )
    return r.status_code, r.json().get("article", {})


print("=" * 68)
print("HUB-9 IMAGE RELOCATION FIX — C1 TO C6")
print("=" * 68)

results = []

for art in ARTICLES:
    print(f"\n[{art['id']}] article_id={art['article_id']}")

    # Fetch live body
    body, status = fetch_body(art["article_id"])
    if body is None:
        print(f"  FETCH FAIL — HTTP {status}")
        results.append({"id": art["id"], "status": "FAIL", "reason": f"fetch HTTP {status}"})
        break

    imgs_before = count_images(body)
    print(f"  Images in live body: {imgs_before}")

    # Pre-check: confirm block is inside cluster-nav
    block_pos = body.find(BLOCK_OPEN)
    cnav_pos = body.find(ANCHOR_OPEN)
    print(f"  article-image-mid at pos {block_pos} | cluster-nav at pos {cnav_pos}")
    print(f"  Currently inside cluster-nav: {block_pos > cnav_pos}")

    # Relocate
    new_body, diag = relocate(body)
    if "error" in diag:
        print(f"  RELOCATE ERROR: {diag['error']}")
        results.append({"id": art["id"], "status": "FAIL", "reason": diag["error"]})
        break

    print(f"  block_before_cnav after relocation: {diag['block_before_cnav']}")
    print(f"  block_inside_cnav after: {diag['block_inside_cnav_after']}")

    imgs_after = count_images(new_body)
    print(f"  Images after relocation: {imgs_after}")

    if not diag["block_before_cnav"] or diag["block_inside_cnav_after"]:
        print(f"  LOGIC FAIL — relocation did not produce correct structure")
        results.append({"id": art["id"], "status": "FAIL", "reason": "position check failed"})
        break

    # Update local file
    local_path = os.path.join(OUTPUT_DIR, art["file"])
    local_html = open(local_path, encoding="utf-8").read()
    new_local, local_diag = relocate(local_html)
    if "error" not in local_diag:
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(new_local)
        print(f"  Local file updated.")

    # PUT to Shopify
    print(f"  [PUT] ...")
    put_status, put_data = put_body(art["article_id"], new_body)
    if put_status != 200:
        print(f"  PUT FAIL — HTTP {put_status}")
        results.append({"id": art["id"], "status": "FAIL", "reason": f"PUT HTTP {put_status}"})
        break

    print(f"  PUT PASS — HTTP 200")

    # Verify from API response body
    verify_html = put_data.get("body_html", "")
    v_block_pos = verify_html.find(BLOCK_OPEN)
    v_cnav_pos = verify_html.find(ANCHOR_OPEN)
    v_imgs = count_images(verify_html)
    v_before = v_block_pos < v_cnav_pos
    v_inside = v_block_pos > v_cnav_pos

    print(f"  VERIFY: imgs={v_imgs} | block@{v_block_pos} | cnav@{v_cnav_pos}")
    print(f"  VERIFY: block_before_cnav={v_before} | block_inside_cnav={v_inside}")

    ok = v_imgs == 2 and v_before and not v_inside
    results.append({
        "id": art["id"],
        "status": "PASS" if ok else "FAIL",
        "imgs": v_imgs,
        "block_before_cnav": v_before,
        "inside_cnav": v_inside,
    })

print("\n" + "=" * 68)
print("SUMMARY")
print("=" * 68)
all_ok = all(r.get("status") == "PASS" for r in results)
for r in results:
    flag = "OK" if r.get("block_before_cnav") and not r.get("inside_cnav") else "FAIL"
    print(f"  {r['id']:4} | {r.get('status'):4} | imgs={r.get('imgs','?')} | pos={flag}")
print(f"\nFINAL: {'ALL PASS' if all_ok else 'PARTIAL/FAIL'}")
