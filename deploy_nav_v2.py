"""
BabyMania — Nav v2: create shoe-type collections + redeploy bm-mobile-nav.liquid
"""
import requests, os, sys, time
sys.stdout.reconfigure(encoding='utf-8')

SHOP_URL      = 'a2756c-c0.myshopify.com'
WORKING_THEME = '187183563065'

_env = open(r'C:/Users/3024e/Desktop/shopify-token/.env').read().strip().split('=', 1)
_SECRET = _env[1] if len(_env) > 1 else os.environ.get('SHOPIFY_APP_SECRET', '')
resp = requests.post(f'https://{SHOP_URL}/admin/oauth/access_token', data={
    'grant_type': 'client_credentials',
    'client_id': '896f1f2ea1a949303affac3d2c2a0d09',
    'client_secret': _SECRET,
}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
token = resp.json()['access_token']
H  = {'X-Shopify-Access-Token': token}
HJ = {**H, 'Content-Type': 'application/json'}
BASE = f'https://{SHOP_URL}/admin/api/2024-10/themes/{WORKING_THEME}/assets.json'

# ── 1. Create shoe-type smart collections ─────────────────────────────────────
print('=== Step 1: Shoe-type collections ===')

SHOE_COLS = [
    {'title': 'נעלי סניקרס',    'handle': 'nav-shoes-sneakers',   'tag': 'shoes-sneakers'},
    {'title': 'סנדלים',          'handle': 'nav-shoes-sandals',    'tag': 'shoes-sandals'},
    {'title': 'נעלי צעד ראשון', 'handle': 'nav-shoes-first-step', 'tag': 'shoes-first-step'},
    {'title': 'נעלי אורות',      'handle': 'nav-shoes-lights',     'tag': 'shoes-lights'},
    {'title': 'מגפיים',          'handle': 'nav-shoes-boots',      'tag': 'shoes-boots'},
]

# Get existing collections
q = '{ collections(first: 200) { edges { node { handle } } } }'
r = requests.post(f'https://{SHOP_URL}/admin/api/2024-10/graphql.json', headers=HJ, json={'query': q})
existing_handles = {e['node']['handle'] for e in r.json()['data']['collections']['edges']}

for col in SHOE_COLS:
    if col['handle'] in existing_handles:
        print(f'  SKIP (exists): {col["title"]}')
        continue
    payload = {'smart_collection': {
        'title': col['title'],
        'handle': col['handle'],
        'rules': [{'column': 'tag', 'relation': 'equals', 'condition': col['tag']}],
        'disjunctive': False,
    }}
    r2 = requests.post(f'https://{SHOP_URL}/admin/api/2024-10/smart_collections.json', headers=H, json=payload)
    if r2.status_code in (200, 201):
        pc = r2.json()['smart_collection'].get('products_count', 0)
        print(f'  CREATED: {col["title"]}  ({pc} products)')
    else:
        print(f'  ERROR {r2.status_code}: {col["title"]} — {r2.text[:200]}')
    time.sleep(0.4)

# ── 2. Upload updated bm-mobile-nav.liquid ────────────────────────────────────
print('\n=== Step 2: Upload bm-mobile-nav.liquid v2 ===')

NAV_CONTENT = r"""{% comment %} BabyMania — Mobile Nav Overlay v2 (RTL) {% endcomment %}

<div id="bm-mobile-nav" class="bm-nav__overlay" aria-hidden="true" role="dialog" aria-modal="true" aria-label="תפריט ניווט">
  <div class="bm-nav__container">

    {%- comment -%} Header {%- endcomment -%}
    <div class="bm-nav__header">
      <button class="bm-nav__close" id="bm-nav-close" aria-label="סגור תפריט">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
      <a href="{{ routes.root_url }}" class="bm-nav__logo-link" aria-label="דף הבית">
        <span class="bm-nav__logo-text">BabyMania</span>
      </a>
    </div>

    {%- comment -%} Top banner — כל המוצרים {%- endcomment -%}
    <a href="/collections/all" class="bm-nav__top-banner">
      <span>✨ כל המוצרים</span>
      <span class="bm-nav__top-banner-arrow">←</span>
    </a>

    {%- comment -%} Nav List {%- endcomment -%}
    <nav class="bm-nav__content" aria-label="קטגוריות">
      <ul class="bm-nav__list" role="list">

        {%- comment -%} בנות {%- endcomment -%}
        <li class="bm-nav__item bm-nav__item--has-sub">
          <button class="bm-nav__cat-btn" aria-expanded="false" aria-controls="bm-sub-girls">
            <div class="bm-nav__cat-inner">
              <div class="bm-nav__cat-image bm-nav__cat-image--girls" aria-hidden="true"></div>
              <span class="bm-nav__cat-title">בנות</span>
            </div>
            <span class="bm-nav__chevron">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
            </span>
          </button>
          <ul id="bm-sub-girls" class="bm-nav__sub" role="list" hidden>
            <li><a href="{{ routes.collections_url }}/nav-girl-sets" class="bm-nav__sub-link">סטים ומארזים</a></li>
            <li><a href="{{ routes.collections_url }}/nav-girl-rompers" class="bm-nav__sub-link">בגדי גוף ואוברולים</a></li>
            <li><a href="{{ routes.collections_url }}/nav-girl-dress" class="bm-nav__sub-link">שמלות וחצאיות</a></li>
            <li><a href="{{ routes.collections_url }}/nav-girl-tops" class="bm-nav__sub-link">חולצות וגופיות</a></li>
            <li><a href="{{ routes.collections_url }}/nav-girl-pants" class="bm-nav__sub-link">מכנסיים וטייצים</a></li>
            <li><a href="{{ routes.collections_url }}/nav-girl-swim" class="bm-nav__sub-link">בגדי ים</a></li>
            <li><a href="{{ routes.collections_url }}/nav-girl-pajama" class="bm-nav__sub-link">פיג׳מות</a></li>
            <li><a href="{{ routes.collections_url }}/nav-girl-winter" class="bm-nav__sub-link">בגדי חורף</a></li>
            <li><a href="{{ routes.collections_url }}/nav-shoes-girl" class="bm-nav__sub-link">נעליים</a></li>
            <li><a href="{{ routes.collections_url }}/בגדי-בנות" class="bm-nav__sub-link bm-nav__sub-link--all">הכל לבנות ←</a></li>
          </ul>
        </li>

        {%- comment -%} בנים {%- endcomment -%}
        <li class="bm-nav__item bm-nav__item--has-sub">
          <button class="bm-nav__cat-btn" aria-expanded="false" aria-controls="bm-sub-boys">
            <div class="bm-nav__cat-inner">
              <div class="bm-nav__cat-image bm-nav__cat-image--boys" aria-hidden="true"></div>
              <span class="bm-nav__cat-title">בנים</span>
            </div>
            <span class="bm-nav__chevron">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
            </span>
          </button>
          <ul id="bm-sub-boys" class="bm-nav__sub" role="list" hidden>
            <li><a href="{{ routes.collections_url }}/nav-boy-sets" class="bm-nav__sub-link">סטים ומארזים</a></li>
            <li><a href="{{ routes.collections_url }}/nav-boy-rompers" class="bm-nav__sub-link">בגדי גוף ואוברולים</a></li>
            <li><a href="{{ routes.collections_url }}/nav-boy-tops" class="bm-nav__sub-link">חולצות וגופיות</a></li>
            <li><a href="{{ routes.collections_url }}/nav-boy-pants" class="bm-nav__sub-link">מכנסיים</a></li>
            <li><a href="{{ routes.collections_url }}/nav-boy-swim" class="bm-nav__sub-link">בגדי ים</a></li>
            <li><a href="{{ routes.collections_url }}/nav-boy-pajama" class="bm-nav__sub-link">פיג׳מות</a></li>
            <li><a href="{{ routes.collections_url }}/nav-boy-winter" class="bm-nav__sub-link">בגדי חורף</a></li>
            <li><a href="{{ routes.collections_url }}/nav-shoes-boy" class="bm-nav__sub-link">נעליים</a></li>
            <li><a href="{{ routes.collections_url }}/בגדי-בנים" class="bm-nav__sub-link bm-nav__sub-link--all">הכל לבנים ←</a></li>
          </ul>
        </li>

        {%- comment -%} ריבורן {%- endcomment -%}
        <li class="bm-nav__item">
          <a href="{{ routes.collections_url }}/reborn" class="bm-nav__cat-link">
            <div class="bm-nav__cat-inner">
              <div class="bm-nav__cat-image bm-nav__cat-image--reborn" aria-hidden="true"></div>
              <span class="bm-nav__cat-title">
                בובות ריבורן
                <span class="bm-nav__badge bm-nav__badge--new">✨ חדש</span>
              </span>
            </div>
            <span class="bm-nav__chevron bm-nav__chevron--arrow">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            </span>
          </a>
        </li>

        {%- comment -%} נעליים {%- endcomment -%}
        <li class="bm-nav__item bm-nav__item--has-sub">
          <button class="bm-nav__cat-btn" aria-expanded="false" aria-controls="bm-sub-shoes">
            <div class="bm-nav__cat-inner">
              <div class="bm-nav__cat-image bm-nav__cat-image--shoes" aria-hidden="true"></div>
              <span class="bm-nav__cat-title">נעליים</span>
            </div>
            <span class="bm-nav__chevron">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
            </span>
          </button>
          <ul id="bm-sub-shoes" class="bm-nav__sub" role="list" hidden>
            <li><a href="{{ routes.collections_url }}/nav-shoes-sneakers" class="bm-nav__sub-link">סניקרס</a></li>
            <li><a href="{{ routes.collections_url }}/nav-shoes-sandals" class="bm-nav__sub-link">סנדלים</a></li>
            <li><a href="{{ routes.collections_url }}/nav-shoes-first-step" class="bm-nav__sub-link">צעד ראשון</a></li>
            <li><a href="{{ routes.collections_url }}/nav-shoes-lights" class="bm-nav__sub-link">נעלי אורות</a></li>
            <li><a href="{{ routes.collections_url }}/nav-shoes-boots" class="bm-nav__sub-link">מגפיים</a></li>
            <li><a href="{{ routes.collections_url }}/נעליים" class="bm-nav__sub-link bm-nav__sub-link--all">כל הנעליים ←</a></li>
          </ul>
        </li>

        {%- comment -%} שינה {%- endcomment -%}
        <li class="bm-nav__item">
          <a href="{{ routes.collections_url }}/המיוחדים-שלנו" class="bm-nav__cat-link">
            <div class="bm-nav__cat-inner">
              <div class="bm-nav__cat-image bm-nav__cat-image--sleep" aria-hidden="true"></div>
              <span class="bm-nav__cat-title">
                שינה טובה לתינוק
                <span class="bm-nav__badge bm-nav__badge--rec">🌟 מומלץ</span>
              </span>
            </div>
            <span class="bm-nav__chevron bm-nav__chevron--arrow">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            </span>
          </a>
        </li>

        {%- comment -%} מתנות {%- endcomment -%}
        <li class="bm-nav__item">
          <a href="{{ routes.collections_url }}/מארזי-מתנה" class="bm-nav__cat-link">
            <div class="bm-nav__cat-inner">
              <div class="bm-nav__cat-image bm-nav__cat-image--gifts" aria-hidden="true"></div>
              <span class="bm-nav__cat-title">מתנות ומארזים</span>
            </div>
            <span class="bm-nav__chevron bm-nav__chevron--arrow">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            </span>
          </a>
        </li>

        {%- comment -%} קיץ {%- endcomment -%}
        <li class="bm-nav__item">
          <a href="{{ routes.collections_url }}/summer-2024" class="bm-nav__cat-link">
            <div class="bm-nav__cat-inner">
              <div class="bm-nav__cat-image bm-nav__cat-image--summer" aria-hidden="true"></div>
              <span class="bm-nav__cat-title">
                קיץ 2026
                <span class="bm-nav__badge bm-nav__badge--sale">SALE</span>
              </span>
            </div>
            <span class="bm-nav__chevron bm-nav__chevron--arrow">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            </span>
          </a>
        </li>

      </ul>
    </nav>

    {%- comment -%} Footer {%- endcomment -%}
    <div class="bm-nav__footer">
      <p class="bm-nav__social-proof">⭐ 8,500+ משפחות כבר בחרו בנו</p>
      <div class="bm-nav__footer-links">
        <a href="/pages/contact" class="bm-nav__footer-link">📞 צור קשר</a>
        <a href="/policies/shipping-policy" class="bm-nav__footer-link">📋 מדיניות משלוחים</a>
        <a href="/policies/refund-policy" class="bm-nav__footer-link">🔄 מדיניות החזרות</a>
        <a href="/pages/about" class="bm-nav__footer-link">ℹ️ אודות Baby Mania</a>
        <a href="https://wa.me/972XXXXXXXXX" class="bm-nav__footer-link bm-nav__footer-link--whatsapp" rel="noopener">💬 וואטסאפ</a>
      </div>
      <div class="bm-nav__payment-icons" aria-label="אמצעי תשלום">
        <img src="{{ 'visa.svg' | asset_url }}" alt="Visa" width="38" height="24" loading="lazy" onerror="this.style.display='none'">
        <img src="{{ 'mastercard.svg' | asset_url }}" alt="Mastercard" width="38" height="24" loading="lazy" onerror="this.style.display='none'">
        <img src="{{ 'paypal.svg' | asset_url }}" alt="PayPal" width="38" height="24" loading="lazy" onerror="this.style.display='none'">
        <img src="{{ 'apple-pay.svg' | asset_url }}" alt="Apple Pay" width="38" height="24" loading="lazy" onerror="this.style.display='none'">
        <img src="{{ 'bit.svg' | asset_url }}" alt="Bit" width="38" height="24" loading="lazy" onerror="this.style.display='none'">
      </div>
    </div>

  </div>
</div>

<div id="bm-nav-backdrop" class="bm-nav__backdrop" aria-hidden="true"></div>


<style>
/* ── BabyMania Mobile Nav v2 — RTL ──────────────────────────────────── */
:root {
  --bm-gold:        #B8956A;
  --bm-gold-dark:   #9A7B55;
  --bm-brown:       #340c00;
  --bm-cream:       #FAF6F1;
  --bm-cream-mid:   #F0E8DD;
  --bm-text:        #1A1A1A;
  --bm-sub-text:    #555555;
  --bm-sep:         rgba(184,149,106,0.15);
  --bm-nav-w:       375px;
  --bm-ease:        0.32s cubic-bezier(0.4,0,0.2,1);
}

.bm-nav__overlay {
  position: fixed; inset: 0; z-index: 9999;
  display: flex; justify-content: flex-end;
  direction: rtl; pointer-events: none;
}
.bm-nav__overlay.is-open { pointer-events: auto; }

.bm-nav__backdrop {
  position: fixed; inset: 0; z-index: 9998;
  background: rgba(0,0,0,0.45);
  opacity: 0; transition: opacity var(--bm-ease); pointer-events: none;
}
.bm-nav__backdrop.is-open { opacity: 1; pointer-events: auto; }

.bm-nav__container {
  position: relative; z-index: 9999;
  width: min(var(--bm-nav-w), 100vw);
  height: 100%; background: #ffffff;
  display: flex; flex-direction: column;
  transform: translateX(-100%);
  transition: transform var(--bm-ease);
  overflow: hidden;
  box-shadow: -4px 0 32px rgba(52,12,0,0.18);
}
.bm-nav__overlay.is-open .bm-nav__container { transform: translateX(0); }

/* ── Header ─────────────────────────────────────────────────────────── */
.bm-nav__header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 20px;
  background: linear-gradient(135deg, var(--bm-gold), var(--bm-gold-dark));
  flex-shrink: 0;
}
.bm-nav__close {
  display: flex; align-items: center; justify-content: center;
  width: 40px; height: 40px;
  background: rgba(255,255,255,0.15); border: none; border-radius: 50%;
  color: #fff; cursor: pointer; transition: background 0.2s; flex-shrink: 0;
}
.bm-nav__close:hover { background: rgba(255,255,255,0.25); }
.bm-nav__logo-text {
  font-family: 'Heebo', sans-serif; font-weight: 900; font-size: 22px;
  color: #fff; letter-spacing: 1px;
}

/* ── Top banner ──────────────────────────────────────────────────────── */
.bm-nav__top-banner {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  padding: 14px 20px;
  background: linear-gradient(135deg, var(--bm-gold), var(--bm-gold-dark));
  color: #fff; text-decoration: none;
  font-family: 'Heebo', sans-serif; font-size: 15px; font-weight: 700;
  border-radius: 0 0 16px 16px;
  flex-shrink: 0;
  transition: opacity 0.2s;
}
.bm-nav__top-banner:hover { opacity: 0.9; color: #fff; }
.bm-nav__top-banner-arrow { font-size: 18px; font-weight: 900; }

/* ── Nav content ─────────────────────────────────────────────────────── */
.bm-nav__content { flex: 1; overflow-y: auto; overscroll-behavior: contain; -webkit-overflow-scrolling: touch; }
.bm-nav__list { list-style: none; margin: 0; padding: 0; }

/* ── Category item ──────────────────────────────────────────────────── */
.bm-nav__item { border-bottom: 1px solid var(--bm-sep); }
.bm-nav__item:last-child { border-bottom: none; }

.bm-nav__cat-btn,
.bm-nav__cat-link {
  display: flex; align-items: center; justify-content: space-between;
  width: 100%; padding: 14px 20px;
  background: none; border: none; cursor: pointer;
  text-decoration: none; color: var(--bm-text);
  transition: background 0.15s;
}
.bm-nav__cat-btn:hover, .bm-nav__cat-link:hover { background: var(--bm-cream); }

.bm-nav__cat-inner { display: flex; align-items: center; gap: 14px; }

/* ── Circular images ────────────────────────────────────────────────── */
.bm-nav__cat-image {
  width: 64px; height: 64px; border-radius: 50%; flex-shrink: 0;
  border: 2px solid rgba(184,149,106,0.3);
  box-shadow: 0 2px 8px rgba(184,149,106,0.15);
}
.bm-nav__cat-image--girls  { background: radial-gradient(circle at 35% 35%, #FFE4EC 0%, #FFC1D6 100%); }
.bm-nav__cat-image--boys   { background: radial-gradient(circle at 35% 35%, #E0F0FF 0%, #B8D8F8 100%); }
.bm-nav__cat-image--reborn { background: radial-gradient(circle at 35% 35%, #FAF0E4 0%, #E8D5C0 100%); }
.bm-nav__cat-image--shoes  { background: radial-gradient(circle at 35% 35%, #E8F5E9 0%, #C8E6C9 100%); }
.bm-nav__cat-image--sleep  { background: radial-gradient(circle at 35% 35%, #EDE7F6 0%, #D1C4E9 100%); }
.bm-nav__cat-image--gifts  { background: radial-gradient(circle at 35% 35%, #FFF8E1 0%, #FFE082 100%); }
.bm-nav__cat-image--summer { background: radial-gradient(circle at 35% 35%, #FFF3E0 0%, #FFCC80 100%); }

/* ── Category title ─────────────────────────────────────────────────── */
.bm-nav__cat-title {
  font-family: 'Heebo', 'Assistant', sans-serif; font-weight: 700; font-size: 16px;
  color: var(--bm-text); display: flex; align-items: center; gap: 8px; text-align: right;
}

/* ── Badges ──────────────────────────────────────────────────────────── */
.bm-nav__badge {
  display: inline-block; padding: 2px 8px; font-size: 10px;
  font-weight: 700; border-radius: 8px; font-family: 'Heebo', sans-serif; white-space: nowrap;
}
.bm-nav__badge--new  { background: var(--bm-gold); color: #fff; }
.bm-nav__badge--rec  { background: #7B1FA2; color: #fff; }
.bm-nav__badge--sale { background: #E65100; color: #fff; }

/* ── Chevron ──────────────────────────────────────────────────────────── */
.bm-nav__chevron {
  display: flex; align-items: center;
  color: var(--bm-gold);
  transition: transform 0.3s ease;
  flex-shrink: 0;
}
.bm-nav__cat-btn[aria-expanded="true"] .bm-nav__chevron { transform: rotate(180deg); }
.bm-nav__chevron--arrow { transform: none !important; }

/* ── Subcategories ──────────────────────────────────────────────────── */
.bm-nav__sub {
  list-style: none; margin: 0; padding: 4px 0 8px;
  background: var(--bm-cream);
  border-top: 1px solid var(--bm-sep);
}
.bm-nav__sub[hidden] { display: none; }
.bm-nav__sub li { border-bottom: 1px solid var(--bm-sep); }
.bm-nav__sub li:last-child { border-bottom: none; }

.bm-nav__sub-link {
  display: block; padding: 11px 20px 11px 20px; padding-right: 82px;
  font-family: 'Heebo', 'Assistant', sans-serif; font-size: 14px; font-weight: 500;
  color: var(--bm-sub-text); text-decoration: none; transition: background 0.15s, color 0.15s;
}
.bm-nav__sub-link:hover { background: var(--bm-cream-mid); color: var(--bm-brown); }
.bm-nav__sub-link--all { font-weight: 700; color: var(--bm-gold); }

/* ── Footer ──────────────────────────────────────────────────────────── */
.bm-nav__footer {
  flex-shrink: 0; padding: 16px 20px;
  background: var(--bm-cream);
  border-top: 1px solid var(--bm-sep);
}

.bm-nav__social-proof {
  text-align: center; font-family: 'Heebo', sans-serif; font-size: 13px; font-weight: 700;
  color: var(--bm-gold); margin: 0 0 12px; letter-spacing: 0.3px;
}

.bm-nav__footer-links {
  display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;
}

.bm-nav__footer-link {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 8px 12px;
  background: #ffffff; border: 1px solid #eeeeee; border-radius: 8px;
  color: #555555; font-family: 'Heebo', sans-serif; font-size: 13px; font-weight: 600;
  text-decoration: none; white-space: nowrap;
  transition: background 0.15s, border-color 0.15s;
}
.bm-nav__footer-link:hover { background: var(--bm-cream); border-color: var(--bm-gold); color: var(--bm-brown); }
.bm-nav__footer-link--whatsapp:hover { border-color: #25D366; }

.bm-nav__payment-icons {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  opacity: 0.55;
}
.bm-nav__payment-icons img { height: 20px; width: auto; object-fit: contain; }

@media screen and (min-width: 990px) {
  .bm-nav__overlay, .bm-nav__backdrop { display: none !important; }
}
</style>


<script>
(function() {
  'use strict';
  var overlay  = document.getElementById('bm-mobile-nav');
  var backdrop = document.getElementById('bm-nav-backdrop');
  var closeBtn = document.getElementById('bm-nav-close');
  var hamburger = null;

  function openNav() {
    overlay.classList.add('is-open');
    backdrop.classList.add('is-open');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    if (closeBtn) closeBtn.focus();
  }

  function closeNav() {
    overlay.classList.remove('is-open');
    backdrop.classList.remove('is-open');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (hamburger) hamburger.focus();
  }

  if (closeBtn) closeBtn.addEventListener('click', closeNav);
  if (backdrop) backdrop.addEventListener('click', closeNav);
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && overlay.classList.contains('is-open')) closeNav();
  });

  // Accordion
  var catBtns = overlay.querySelectorAll('.bm-nav__cat-btn');
  catBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var expanded = btn.getAttribute('aria-expanded') === 'true';
      var sub = document.getElementById(btn.getAttribute('aria-controls'));
      catBtns.forEach(function(b) {
        if (b !== btn) {
          b.setAttribute('aria-expanded', 'false');
          var os = document.getElementById(b.getAttribute('aria-controls'));
          if (os) os.hidden = true;
        }
      });
      if (sub) {
        sub.hidden = expanded;
        btn.setAttribute('aria-expanded', String(!expanded));
      }
    });
  });

  // Hook Dawn hamburger
  function hookHamburger() {
    var summary = document.querySelector('#Details-menu-drawer-container > summary')
                || document.querySelector('.header__icon--menu');
    if (summary) {
      hamburger = summary;
      summary.addEventListener('click', function(e) {
        if (window.innerWidth >= 990) return;
        e.preventDefault();
        e.stopImmediatePropagation();
        openNav();
      }, true);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hookHamburger);
  } else {
    hookHamburger();
  }
})();
</script>
"""

r = requests.put(BASE, headers=HJ, json={'asset': {'key': 'snippets/bm-mobile-nav.liquid', 'value': NAV_CONTENT}})
if r.status_code in (200, 201):
    print(f'  ✓ UPLOADED: snippets/bm-mobile-nav.liquid  ({len(NAV_CONTENT):,} chars)')
else:
    print(f'  ✗ ERROR {r.status_code}: {r.text[:300]}')
    sys.exit(1)

# ── 3. Verify ─────────────────────────────────────────────────────────────────
print('\n=== Step 3: Verify ===')
time.sleep(0.5)
rv = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-mobile-nav.liquid'})
live = rv.json()['asset']['value']

checks = {
    '"בנות" (not תינוקות בנות)': '>בנות<' in live and 'תינוקות בנות' not in live,
    '"בנים" (not תינוקות בנים)': '>בנים<' in live and 'תינוקות בנים' not in live,
    'shoes-sneakers sub': 'nav-shoes-sneakers' in live,
    'shoes-sandals sub':  'nav-shoes-sandals'  in live,
    'shoes-first-step sub': 'nav-shoes-first-step' in live,
    'shoes-lights sub':   'nav-shoes-lights'   in live,
    'shoes-boots sub':    'nav-shoes-boots'    in live,
    'top banner present': 'bm-nav__top-banner' in live,
    'badge new reborn':   'badge--new' in live,
    'badge rec sleep':    'badge--rec' in live,
    'badge sale summer':  'badge--sale' in live,
    'footer links':       'bm-nav__footer-links' in live,
    'no account link':    'החשבון שלי' not in live,
    'gold gradient header': 'linear-gradient(135deg, var(--bm-gold)' in live,
    'chevron 22px':       'width="22"' in live,
}

all_pass = True
for label, result in checks.items():
    print(f'  {"✓" if result else "✗"} {label}')
    if not result: all_pass = False

print()
print('=== ALL PASS ===' if all_pass else '=== SOME FAILED ===')
if not all_pass: sys.exit(1)
