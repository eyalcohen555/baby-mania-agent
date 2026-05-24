"""
reborn_dawn_prep.py
Terminal 6 — BabyMania Reborn only

From levi-reborn-product-liquid-draft.liquid, builds:
  output/theme-test/sections/bm-reborn-product-page.liquid
  output/theme-test/templates/product.reborn-test.json

Also applies small fixes to the draft:
  - S13 stat: "48 ס״מ" -> metafield (dynamic)
  - S11 social proof: "2,400" / "+2,400" -> safer text without exact number
  - S1 hero stars: keep 4.9 (visible trust signal, mark as TODO)

NEVER: touches live theme, Shopify products, metafields, v2.html original.
"""

import json
import re
from pathlib import Path

DRAFT   = Path(__file__).parent.parent / "output" / "pages" / "reborn-landing" / "levi-reborn-product-liquid-draft.liquid"
OUT_DIR = Path(__file__).parent.parent / "output" / "theme-test"
SECTION = OUT_DIR / "sections" / "bm-reborn-product-page.liquid"
TMPL    = OUT_DIR / "templates" / "product.reborn-test.json"

# ── Fix 1: S13 stat "48 ס״מ" -> metafield ────────────────────────────────────
# In S13, the stat chip shows hardcoded 48. Replace with metafield + fallback.
S13_OLD = '<span class="stat-num">48 ס״מ</span>'
S13_NEW = '<span class="stat-num">{{ product.metafields.reborn_specs.size_cm.value | default: \'46 ס״מ\' }}</span>'

# ── Fix 2: S11 "+2,400 אמהות כבר בחרו בלוי" -> safe text ────────────────────
S11_H2_OLD = '<h2 class="headline"><span class="highlight">+2,400</span> אמהות כבר בחרו בלוי</h2>'
S11_H2_NEW = '<h2 class="headline">אמהות כבר בחרו ב{{ product.metafields.reborn_doll.hebrew_name.value | default: product.title }}</h2><!-- TODO: replace with real review count once collected -->'

# ── Fix 3: S1 hero stars (2,400 ביקורות) -> safe text ────────────────────────
S1_REVIEWS_OLD = '<a class="hero-review-count" href="#section-reviews">(2,400 ביקורות)</a>'
S1_REVIEWS_NEW = '<a class="hero-review-count" href="#section-reviews"><!-- TODO: real review count -->ביקורות לקוחות</a>'

# ── Fix 4: S11 rating "4.9 מתוך 5" -> safe text ─────────────────────────────
S11_RATING_OLD = '<span class="rating-text">4.9 מתוך 5</span>'
S11_RATING_NEW = '<span class="rating-text"><!-- TODO: real rating -->דירוג לקוחות</span>'

# ── Fix 5: S11 "מאות ביקורות מאמהות" — already neutral, keep ──────────────────

# Also fix S13 gap/margin "48px" — these are CSS numbers, NOT product sizes. Keep them.

SCHEMA = """{
  "name": "Reborn Product Page",
  "tag": "div",
  "class": "bm-reborn-page",
  "settings": [],
  "presets": [
    {
      "name": "Reborn Product Page"
    }
  ]
}"""


def main():
    print("reborn_dawn_prep.py — Terminal 6")
    if not DRAFT.exists():
        print(f"ERROR: draft not found: {DRAFT}")
        return

    content = DRAFT.read_text(encoding="utf-8")
    lines   = content.splitlines()
    print(f"  Read {len(lines)} lines from draft.")

    # ── Step 1: Apply small fixes ─────────────────────────────────────────────
    fixes = [
        (S13_OLD,        S13_NEW,        "S13 stat 48->metafield"),
        (S11_H2_OLD,     S11_H2_NEW,     "S11 headline +2400->dynamic"),
        (S1_REVIEWS_OLD, S1_REVIEWS_NEW, "S1 review count->TODO"),
        (S11_RATING_OLD, S11_RATING_NEW, "S11 rating->TODO"),
    ]
    for old, new, label in fixes:
        if old in content:
            content = content.replace(old, new, 1)
            print(f"  [ok] {label}")
        else:
            print(f"  [WARN] not found: {label}")

    # Write fixed draft back
    DRAFT.write_text(content, encoding="utf-8")
    print(f"  [ok] Draft updated: {DRAFT.name}")

    # ── Step 2: Extract parts from fixed draft ────────────────────────────────
    # CSS: between first <style> and its closing </style>
    css_match = re.search(r"<style>(.*?)</style>", content, re.DOTALL)
    if not css_match:
        print("  [WARN] <style> block not found — CSS extraction failed")
        css_content = "/* CSS extraction failed */"
    else:
        css_content = css_match.group(1).strip()
        print(f"  [ok] CSS extracted ({len(css_content.splitlines())} lines)")

    # Tailwind config script (between <script id="tailwind-config"> and </script>)
    tw_match = re.search(r'(<script id="tailwind-config">.*?</script>)', content, re.DOTALL)
    tw_block = tw_match.group(1).strip() if tw_match else "<!-- tailwind config not found -->"

    # Google Fonts link tags
    fonts_match = re.findall(r'<link[^>]+fonts\.googleapis[^>]+/>', content)
    fonts_block = "\n".join(fonts_match) if fonts_match else ""

    # Main content: from page-level <main> to the last </main> before </body>
    # Note: S3 mobile section has a nested <main> — we must use the PAGE-level open/close.
    # Page-level <main> is on its own line; last </main> is just before \n\n<!-- FOOTER
    main_open_idx  = content.find("\n<main>\n")
    footer_idx     = content.rfind("<!-- ── FOOTER ──")
    # The page-level </main> is just before \n</main>\n\n<!-- FOOTER
    main_close_idx = content.rfind("\n</main>\n", 0, footer_idx)
    if main_open_idx == -1 or main_close_idx == -1:
        print("  [WARN] page-level <main> boundaries not found")
        main_content = "<!-- main extraction failed -->"
    else:
        start = main_open_idx + len("\n<main>\n")
        end   = main_close_idx
        main_content = content[start:end].strip()
        print(f"  [ok] Main content extracted ({len(main_content.splitlines())} lines)")

    # JS: the last <script> block before </body>
    js_matches = list(re.finditer(r"<script>(.*?)</script>", content, re.DOTALL))
    if js_matches:
        js_content = js_matches[-1].group(1).strip()
        print(f"  [ok] JS extracted ({len(js_content.splitlines())} lines)")
    else:
        print("  [WARN] JS block not found")
        js_content = "/* JS extraction failed */"

    # ── Step 3: Build section file ────────────────────────────────────────────
    parts = []
    parts.append("{% comment %}")
    parts.append("bm-reborn-product-page.liquid")
    parts.append("Terminal 6 — BabyMania | ריבורן | test only")
    parts.append("DO NOT PUSH TO LIVE — testing template for levi (PID 9689589383481)")
    parts.append("{% endcomment %}")
    parts.append("")
    parts.append(fonts_block)
    parts.append('<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>')
    parts.append(tw_block)
    parts.append("")
    parts.append("{% stylesheet %}")
    parts.append(css_content)
    parts.append("{% endstylesheet %}")
    parts.append("")
    parts.append(main_content)
    parts.append("")
    parts.append("{% javascript %}")
    parts.append(js_content)
    parts.append("{% endjavascript %}")
    parts.append("")
    parts.append("{% schema %}")
    parts.append(SCHEMA)
    parts.append("{% endschema %}")
    section_content = "\n".join(parts)

    # ── Step 4: Write files ───────────────────────────────────────────────────
    SECTION.parent.mkdir(parents=True, exist_ok=True)
    TMPL.parent.mkdir(parents=True, exist_ok=True)

    SECTION.write_text(section_content, encoding="utf-8")
    print(f"  [ok] Section: {SECTION}")

    template = {
        "sections": {
            "main": {
                "type": "bm-reborn-product-page",
                "settings": {}
            }
        },
        "order": ["main"]
    }
    TMPL.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  [ok] Template: {TMPL}")

    # ── Step 5: Validation ────────────────────────────────────────────────────
    sc = SECTION.read_text(encoding="utf-8")
    print("\nValidation (section file):")
    checks = [
        ("{%- assign bm_variant",   "bm_variant assign"),
        ("form 'product', product", "product form present (S1)"),
        ("bm-product-form-s17",     "product form present (S17)"),
        ("endform",                 "endform closed"),
        ("{% stylesheet %}",        "stylesheet block"),
        ("{% javascript %}",        "javascript block"),
        ("{% schema %}",            "schema block"),
        ("money_without_trailing",  "money filter"),
        ("reborn_doll.model_label", "model_label metafield"),
        ("reborn_copy.hero_subtitle","hero_subtitle metafield"),
        ("reborn_specs.size_cm",    "size_cm metafield"),
    ]
    for needle, label in checks:
        found = needle in sc
        print(f"  {'ok' if found else 'FAIL'} {label}")

    neg_checks = [
        ("Reborn Baby Levi 48cm",       "hardcoded prod-name"),
        ('"48 ס״מ"',               "hardcoded 48cm stat"),
        ("+2,400",                       "hardcoded +2400"),
        ("<!DOCTYPE",                    "DOCTYPE removed"),
        ("<html",                        "html tag removed"),
        ("<head",                        "head tag removed"),
        ("<nav",                         "nav removed"),
        ("<footer",                      "footer removed"),
    ]
    print("\nNegative checks (should be absent):")
    for needle, label in neg_checks:
        found = needle in sc
        print(f"  {'WARN — still present' if found else 'ok absent'}: {label}")

    sl = len(sc.splitlines())
    print(f"\n  Section lines: {sl}")
    print("Done.")


if __name__ == "__main__":
    main()
