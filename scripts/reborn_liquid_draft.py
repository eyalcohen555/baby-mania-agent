"""
reborn_liquid_draft.py
Terminal 6 — BabyMania Reborn only

Converts levi-reborn-product-v2.html → levi-reborn-product-liquid-draft.liquid
by replacing ONLY S1 Hero and S17 Final CTA with Liquid-dynamic versions.

NEVER: modifies original file, touches other sections, writes to Shopify.
"""

import re
from pathlib import Path

SRC  = Path(__file__).parent.parent / "output" / "pages" / "reborn-landing" / "levi-reborn-product-v2.html"
DEST = Path(__file__).parent.parent / "output" / "pages" / "reborn-landing" / "levi-reborn-product-liquid-draft.liquid"

# ── Liquid replacement: S1 Hero ───────────────────────────────────────────────
S1_LIQUID = """\
<!-- ════════════════════════════════════════
     S1 — HERO (Liquid)
════════════════════════════════════════ -->
{%- assign bm_variant  = product.selected_or_first_available_variant -%}
{%- assign bm_model    = product.metafields.reborn_doll.model_label.value | default: product.title -%}
{%- assign bm_size     = product.metafields.reborn_specs.size_cm.value -%}
{%- assign bm_subtitle = product.metafields.reborn_copy.hero_subtitle.value | default: product.description -%}
{%- assign bm_price    = bm_variant.price -%}
{%- assign bm_compare  = bm_variant.compare_at_price -%}
{%- if bm_compare > bm_price -%}
  {%- assign bm_save_pct = bm_compare | minus: bm_price | times: 100 | divided_by: bm_compare | round -%}
{%- endif -%}
<section class="hero-sec" data-section="1">
  <div class="sc">
    <div class="hero-grid">
      <!-- TEXT -->
      <div>
        <div class="sec-lbl">S1 — HERO</div>
        <div class="hero-tag">אהובה על לקוחות Baby Mania</div>
        <div class="hero-prod-name">{{ bm_model }}{% if bm_size %} {{ bm_size }}{% endif %}</div>
        <h1 class="hero-h1">הרגע שבו היא מחזיקה אותה בפעם הראשונה —<br/>ומתחילה לטפל כמו אמא קטנה</h1>
        <p class="hero-sub">{{ bm_subtitle }}</p>
        <div class="hero-stars">
          <span class="stars-ico">★★★★★</span>
          <span class="hero-rating">4.9</span>
          <a class="hero-review-count" href="#section-reviews">(2,400 ביקורות)</a>
        </div>
        <div class="hero-price-row">
          <span class="price-now">{{ bm_price | money_without_trailing_zeros }}</span>
          {%- if bm_compare > bm_price -%}
          <span class="price-old">{{ bm_compare | money_without_trailing_zeros }}</span>
          <span class="price-save">חוסכים {{ bm_save_pct }}%</span>
          {%- endif -%}
        </div>
        <div class="hero-daily">פחות מ-₪1 ליום</div>
        {%- form 'product', product, id: 'bm-product-form-s1' -%}
          {%- unless product.has_only_default_variant -%}
          <div class="bm-variant-selector" style="margin-bottom:16px;">
            {%- for option in product.options_with_values -%}
            <div style="margin-bottom:10px;">
              <label style="font-size:14px;font-weight:700;color:var(--heading);display:block;margin-bottom:6px;text-align:right;">{{ option.name }}</label>
              <select name="options[{{ option.name }}]" id="option-{{ option.position }}-s1"
                      style="width:100%;padding:10px 14px;border:1px solid rgba(184,149,106,0.3);border-radius:8px;font-family:'Heebo',sans-serif;font-size:15px;background:#fff;color:var(--heading);">
                {%- for value in option.values -%}
                <option value="{{ value }}"{% if option.selected_value == value %} selected{% endif %}>{{ value }}</option>
                {%- endfor -%}
              </select>
            </div>
            {%- endfor -%}
          </div>
          {%- else -%}
          <input type="hidden" name="id" value="{{ product.variants.first.id }}"/>
          {%- endunless -%}
          <div class="hero-btns">
            <button type="submit" name="add" class="btn-cta">הוסיפי לעגלה</button>
            <!-- TODO Stage 8: "קני עכשיו" requires JS buy-now redirect to checkout -->
            <button type="button" class="btn-outline">קני עכשיו</button>
          </div>
        {%- endform -%}
        <div class="hero-trust" id="bm-hero-trust" role="list" aria-label="יתרונות הזמנה">
          <div class="hero-trust-item" role="listitem">
            <div class="hero-trust-icon hero-trust-icon--green" aria-hidden="true">
              <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 3h15v13H1z"/><path d="M16 8h4l3 4v4h-7V8z"/>
                <circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>
              </svg>
            </div>
            <span class="hero-trust-label">משלוח חינם</span>
            <span class="hero-trust-sub">לכל הארץ</span>
          </div>
          <div class="hero-trust-item" role="listitem">
            <div class="hero-trust-icon hero-trust-icon--blue" aria-hidden="true">
              <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 12a9 9 0 1 0 9-9 9 9 0 0 0-6.36 2.64L3 8"/>
                <path d="M3 3v5h5"/>
              </svg>
            </div>
            <span class="hero-trust-label">החזרה עד 14 יום</span>
            <span class="hero-trust-sub">ממועד קבלת המוצר</span>
          </div>
          <div class="hero-trust-item" role="listitem">
            <div class="hero-trust-icon hero-trust-icon--amber" aria-hidden="true">
              <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L3 6v6c0 5.5 3.8 10.7 9 12 5.2-1.3 9-6.5 9-12V6l-9-4z"/>
                <path d="M9 12l2 2 4-4"/>
              </svg>
            </div>
            <span class="hero-trust-label">תשלום מאובטח</span>
            <span class="hero-trust-sub">הצפנה מלאה SSL</span>
          </div>
        </div>
      </div>
      <!-- IMAGE -->
      <div class="hero-img-col">
        {%- if product.images.size > 0 -%}
        <img src="{{ product.images[0] | image_url: width: 800 }}"
             srcset="{{ product.images[0] | image_url: width: 400 }} 400w, {{ product.images[0] | image_url: width: 800 }} 800w, {{ product.images[0] | image_url: width: 1200 }} 1200w"
             sizes="(max-width:768px) 100vw, 50vw"
             alt="{{ bm_model }}{% if bm_size %} {{ bm_size }}{% endif %}"
             class="hero-img" loading="eager" width="800" height="1000"/>
        {%- else -%}
        <div class="hero-img-ph">תמונת {{ bm_model }} תוזן מגלריית המוצר בחנות</div>
        {%- endif -%}
      </div>
    </div>
  </div>
</section>
"""

# ── Liquid replacement: S17 Final CTA ────────────────────────────────────────
S17_LIQUID = """\
<!-- ════════════════════════════════════════
     S17 — CTA סופי (Liquid)
════════════════════════════════════════ -->
{%- assign bm17_variant = product.selected_or_first_available_variant -%}
{%- if bm17_variant.compare_at_price > bm17_variant.price -%}
  {%- assign bm17_save = bm17_variant.compare_at_price | minus: bm17_variant.price | times: 100 | divided_by: bm17_variant.compare_at_price | round -%}
{%- endif -%}
<section class="finalcta-sec" data-section="17">
  <div class="sc">
    <div class="sec-lbl center" style="color:rgba(184,149,106,0.4);">S17 — CTA סופי</div>
    <h2>תני לה מתנה שהיא לא רק תפתח — היא תטפל בה</h2>
    <p class="finalcta-txt">רכה. ריאליסטית. מוכנה לחיבוק הראשון.</p>
    <div class="finalcta-price-row">
      <span class="finalcta-price-now">{{ bm17_variant.price | money_without_trailing_zeros }}</span>
      {%- if bm17_variant.compare_at_price > bm17_variant.price -%}
      <span class="finalcta-price-old">{{ bm17_variant.compare_at_price | money_without_trailing_zeros }}</span>
      <span class="finalcta-price-save">חוסכים {{ bm17_save }}%</span>
      {%- endif -%}
    </div>
    <div class="finalcta-countdown" id="bm-countdown" aria-label="מבצע מוגבל בזמן">
      <div class="bm-cd-unit">
        <div class="bm-cd-num"><span id="bm-cd-h">00</span></div>
        <div class="bm-cd-lbl">שעות</div>
      </div>
      <div class="bm-cd-sep">:</div>
      <div class="bm-cd-unit">
        <div class="bm-cd-num"><span id="bm-cd-m">10</span></div>
        <div class="bm-cd-lbl">דקות</div>
      </div>
      <div class="bm-cd-sep">:</div>
      <div class="bm-cd-unit">
        <div class="bm-cd-num"><span id="bm-cd-s">00</span></div>
        <div class="bm-cd-lbl">שניות</div>
      </div>
    </div>
    {%- form 'product', product, id: 'bm-product-form-s17' -%}
      <input type="hidden" name="id" value="{{ product.selected_or_first_available_variant.id }}"/>
      <div class="finalcta-btns">
        <button type="submit" name="add" class="btn-cta btn-cta--glow">כן, אני רוצה את {{ product.metafields.reborn_doll.model_label.value | default: product.title }}</button>
        <!-- TODO Stage 8: secondary CTA — buy-now JS redirect -->
        <button type="button" class="btn-outline-white">הוסיפי לעגלה</button>
      </div>
    {%- endform -%}
    <div class="finalcta-badges">
      <span class="finalcta-badge-svg">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M1 3h15v13H1z"/><path d="M16 8h4l3 4v4h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
        משלוח חינם
      </span>
      <span class="finalcta-badge-svg">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L3 6v6c0 5.5 3.8 10.7 9 12 5.2-1.3 9-6.5 9-12V6l-9-4z"/><path d="M9 12l2 2 4-4"/></svg>
        תשלום מאובטח
      </span>
      <span class="finalcta-badge-svg">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M3 12a9 9 0 1 0 9-9 9 9 0 0 0-6.36 2.64L3 8"/><path d="M3 3v5h5"/></svg>
        14 יום להחזרה
      </span>
    </div>
    <div class="finalcta-close">כי המשחק של היום הוא הזיכרון של מחר.</div>
  </div>
</section>
"""

# ── Patterns to locate and replace ───────────────────────────────────────────

# ═ = U+2550 BOX DRAWINGS DOUBLE HORIZONTAL
# — = U+2014 EM DASH
_BAR = "═"  # ═
_EM  = "—"  # —

# S1: everything from the comment block through </section>\n (before S2 comment)
S1_PATTERN = re.compile(
    r"<!-- " + _BAR + r"{30,}\n\s+S1 " + _EM + r" HERO\n" + _BAR + r"{30,} -->\n.*?</section>\n",
    re.DOTALL
)

# S17: everything from the comment block through </section>\n
S17_PATTERN = re.compile(
    r"<!-- " + _BAR + r"{30,}\n\s+S17 " + _EM + r" CTA .*?\n" + _BAR + r"{30,} -->\n.*?</section>\n",
    re.DOTALL
)

# Title tag
TITLE_PATTERN = re.compile(
    r"<title>[^<]+</title>"
)
TITLE_LIQUID = "<title>{{ product.metafields.reborn_doll.model_label.value | default: product.title }}{%- if product.metafields.reborn_specs.size_cm.value %} {{ product.metafields.reborn_specs.size_cm.value }}{%- endif %} | Baby Mania</title>"


def main():
    print("reborn_liquid_draft.py — Terminal 6")
    print(f"Source:  {SRC}")
    print(f"Dest:    {DEST}")

    if not SRC.exists():
        print(f"ERROR: source file not found: {SRC}")
        return

    content = SRC.read_text(encoding="utf-8")
    original_len = len(content.splitlines())
    print(f"Read {original_len} lines.")

    # 1. Prepend {% layout none %}
    content = "{% layout none %}\n" + content

    # 2. Replace <title>
    if TITLE_PATTERN.search(content):
        content = TITLE_PATTERN.sub(TITLE_LIQUID, content, count=1)
        print("  [ok] <title> tag -> Liquid")
    else:
        print("  [WARN] <title> pattern not found")

    # 3. Replace S1 Hero
    m1 = S1_PATTERN.search(content)
    if m1:
        content = S1_PATTERN.sub(S1_LIQUID, content, count=1)
        print("  [ok] S1 Hero -> Liquid")
    else:
        print("  [WARN] S1 Hero pattern not found — check regex")

    # 4. Replace S17 Final CTA
    m17 = S17_PATTERN.search(content)
    if m17:
        content = S17_PATTERN.sub(S17_LIQUID, content, count=1)
        print("  [ok] S17 Final CTA -> Liquid")
    else:
        print("  [WARN] S17 pattern not found — check regex")

    # 5. Write output
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(content, encoding="utf-8")
    new_len = len(content.splitlines())
    print(f"  [ok] Written: {new_len} lines -> {DEST.name}")

    # 6. Validation checks
    print("\nValidation:")
    checks = [
        ("{%- assign bm_variant",   "bm_variant assign present"),
        ("form 'product', product", "product form present"),
        ("endform",                 "endform closed"),
        ("bm17_variant",            "S17 variant assign present"),
        ("money_without_trailing",  "money filter present"),
        ("layout none",             "layout none present"),
    ]
    for needle, label in checks:
        found = needle in content
        print(f"  {'ok' if found else 'FAIL'} {label}")

    # Negative checks — these should NOT appear in S1/S17 if conversion worked
    neg_checks = [
        ("Reborn Baby Levi 48cm",  "hardcoded prod-name removed"),
        ("₪299",              "hardcoded ₪299 removed (price)"),
    ]
    for needle, label in neg_checks:
        found = needle in content
        print(f"  {'ok' if not found else 'WARN hardcoded still present'} {label}")

    print("\nDone.")


if __name__ == "__main__":
    main()
