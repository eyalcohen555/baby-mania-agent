import re
import requests

url = "https://babymania-il.com/blogs/news/eich-livhor-bobat-reborn-madrih-larokhesh-harishon"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
page = r.text

# Stylesheets
stylesheets = re.findall(r'<link[^>]+stylesheet[^>]+href=["\']([^"\']+)["\']', page, re.I)
print("=== STYLESHEETS ===")
for s in stylesheets:
    print(" ", s)

# Article body wrapper
print("\n=== ARTICLE BODY WRAPPERS ===")
wrappers = re.findall(r'class="([^"]*(?:rte|article-body|blog-body|article__body|entry-content)[^"]*)"', page, re.I)
for w in wrappers:
    print(" ", w)

# Find where inserted image block lands in live page
print("\n=== INSERTED IMAGE BLOCK IN LIVE PAGE ===")
mid_idx = page.find("article-image-mid")
if mid_idx >= 0:
    print("FOUND at pos", mid_idx)
    ctx = page[max(0, mid_idx - 300):mid_idx + 400]
    print(repr(ctx))
else:
    print("NOT FOUND — image may be inside a wrapped container")
    # Look for one of the inserted CDN images
    img_idx = page.find("S15487067023948ca8ff9f2cc97f82e2ej")
    if img_idx >= 0:
        print("Image src found at pos", img_idx)
        print(repr(page[max(0, img_idx - 400):img_idx + 300]))

# Find inline style blocks in the live page that affect img
print("\n=== THEME INLINE IMG STYLES ===")
style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", page, re.DOTALL | re.I)
for i, block in enumerate(style_blocks):
    img_rules = re.findall(r"[^{}]*img[^{}]*\{[^{}]*\}", block)
    if img_rules:
        print(f"Style block {i}:")
        for rule in img_rules:
            print("  ", rule.strip())
