"""
reborn_fix_layout_and_labels.py — Terminal 6
Transforms levi-reborn-product-liquid-draft.liquid:

1. Remove {% layout none %} → use Dawn layout (header/footer from theme)
2. Remove HTML wrapper: DOCTYPE, <html>, <head>, <body> tags
3. Remove local <nav> block → keep Dawn's nav
4. Add dir="rtl" to <main>
5. Remove local <footer> block → keep Dawn's footer
6. Remove </body> and </html>
7. Remove all visible section-number labels (sec-lbl, section-label divs/spans)
8. Strip "S\d+ — " prefix from eyebrow text that has real content

DOES NOT touch: v2.html original, Shopify live theme, product data.
Writes result back to same file (in-place).
Also writes a copy to output/theme-test/templates/product.reborn.liquid (ready for upload).
"""

import re
from pathlib import Path

DRAFT = Path(r"C:\Projects\baby-mania-agent\output\pages\reborn-landing\levi-reborn-product-liquid-draft.liquid")
THEME_OUT = Path(r"C:\Projects\baby-mania-agent\output\theme-test\templates\product.reborn.liquid")

content = DRAFT.read_text(encoding="utf-8")
original_lines = len(content.splitlines())

# ── 1. Remove {% layout none %} ──────────────────────────────────────────────
content = content.replace("{% layout none %}\n", "", 1)

# ── 2. Remove DOCTYPE / <html> / <head> opening / meta / title tags ──────────
# These are lines 2-7 of the original file (now lines 1-6 after step 1)
content = re.sub(
    r"<!DOCTYPE html>\n<html dir=\"rtl\" lang=\"he\">\n<head>\n"
    r"<meta charset=\"utf-8\"/>\n"
    r"<meta content=\"width=device-width, initial-scale=1\.0\" name=\"viewport\"/>\n"
    r"<title>.*?</title>\n",
    "",
    content,
    count=1,
)

# ── 3. Remove </head> tag ─────────────────────────────────────────────────────
content = content.replace("\n</head>\n", "\n", 1)

# ── 4. Remove <body ...> tag ──────────────────────────────────────────────────
content = re.sub(r"<body[^>]*>\n", "", content, count=1)

# ── 5. Remove <nav> block (local nav) ────────────────────────────────────────
content = re.sub(
    r"\n<!-- ── NAV ── -->\n<nav[^>]*>.*?</nav>\n",
    "\n",
    content,
    count=1,
    flags=re.DOTALL,
)

# ── 6. Add dir="rtl" to <main> ────────────────────────────────────────────────
content = content.replace("\n<main>\n", '\n<main dir="rtl">\n', 1)

# ── 7. Remove <footer> block (local footer) ──────────────────────────────────
content = re.sub(
    r"\n<!-- ── FOOTER ── -->\n<footer[^>]*>.*?</footer>\n",
    "\n",
    content,
    count=1,
    flags=re.DOTALL,
)

# ── 8. Remove </body> and </html> ─────────────────────────────────────────────
content = content.replace("\n</body>\n</html>", "", 1)

# ── 9. Remove pure section-number label divs (sec-lbl, section-label) ────────
# These are development markers that should never appear in production.
# Pattern: <div class="sec-lbl..."> or <div class="section-label..."> containing only "S\d — ..."
pure_label_patterns = [
    r'<div class="sec-lbl">[^<]*S\d+[^<]*</div>\n?',
    r'<div class="sec-lbl [^"]*"[^>]*>[^<]*S\d+[^<]*</div>\n?',
    r'<div class="section-label"[^>]*>[^<]*S\d+[^<]*</div>\n?',
    r'<div class="section-label [^"]*"[^>]*>[^<]*S\d+[^<]*</div>\n?',
]
for pat in pure_label_patterns:
    content = re.sub(pat, "", content)

# ── 10. Strip "S\d+ — " prefix from eyebrow content that has real Hebrew text ─
# e.g., "S7 — מחקרים" → "מחקרים"
# e.g., "S10 — התוצאה בבית" → "התוצאה בבית"
# e.g., "S5 — הגברת" → delete entire div (word alone is meaningless)
# Handle S5 eyebrow separately (content is meaningless without prefix)
content = content.replace(
    '<div class="bm-reborn-problem__eyebrow">S5 — הגברת</div>\n', ""
)
# Generic strip for remaining "S\d — " prefixes inside tags
content = re.sub(r'S\d{1,2} [—–] ', "", content)

# ── Verify ───────────────────────────────────────────────────────────────────
new_lines = len(content.splitlines())
checks = {
    "layout none removed":     "{% layout none %}" not in content,
    "DOCTYPE removed":         "<!DOCTYPE" not in content,
    "<html> removed":          "<html" not in content,
    "<head> removed":          "<head>" not in content,
    "<body> removed":          "<body" not in content,
    "local nav removed":       "<nav class=" not in content,
    "local footer removed":    "<footer " not in content,
    "</body> removed":         "</body>" not in content,
    "</html> removed":         "</html>" not in content,
    "main dir=rtl present":    '<main dir="rtl">' in content,
    "sec-lbl labels removed":  "sec-lbl" not in content,
    "S\\d labels stripped":    not re.search(r'>S\d+ [—–]', content),
    "form product S1 present": "bm-product-form-s1" in content,
    "form product S17 present":"bm-product-form-s17" in content,
    "tailwind CDN present":    "cdn.tailwindcss.com" in content,
    "style block present":     "<style>" in content,
}

print(f"\nLines: {original_lines} → {new_lines}")
print("\nChecks:")
all_ok = True
for label, ok in checks.items():
    status = "ok" if ok else "FAIL"
    if not ok:
        all_ok = False
    print(f"  {status}  {label}")

if all_ok:
    DRAFT.write_text(content, encoding="utf-8")
    print(f"\n  [ok] Written: {DRAFT.name}")
    THEME_OUT.parent.mkdir(parents=True, exist_ok=True)
    THEME_OUT.write_text(content, encoding="utf-8")
    print(f"  [ok] Written: {THEME_OUT}")
else:
    print("\n  ABORTED — fix failures above before writing.")
