"""
Deploy bm-desktop-nav.liquid — working theme (187183563065)
Trust bar + sticky topnav + mega menu (RTL, Hebrew)
"""
import requests, os, sys, time, re
sys.stdout.reconfigure(encoding='utf-8')

SHOP_URL      = 'a2756c-c0.myshopify.com'
WORKING_THEME = '187183563065'
CDN = 'https://cdn.shopify.com/s/files/1/0864/9677/2409/files'

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

# ── Fetch header.liquid ────────────────────────────────────────────────────
header_asset = requests.get(BASE, headers=H, params={'asset[key]': 'sections/header.liquid'}).json()['asset']['value']
print(f'header.liquid: {len(header_asset):,} chars')

# ── Snippet content ────────────────────────────────────────────────────────
NAV_CONTENT = f'''{{%- comment -%}}
  bm-desktop-nav.liquid — desktop only (@media min-width: 990px)
  Trust bar + sticky topnav + mega menu with 3-column panels (RTL)
{{%- endcomment -%}}

<style>
/* ── Mobile: hide entire desktop nav ────────────────────────────── */
@media (max-width: 989px) {{
  .bm-deskbar, .bm-topnav-wrap, .bm-mega-overlay {{ display: none !important; }}
}}

@media (min-width: 990px) {{

/* ── Hide Dawn header ───────────────────────────────────────────── */
.header-wrapper {{ display: none !important; }}

/* ── Trust bar ──────────────────────────────────────────────────── */
.bm-deskbar {{
  display: flex; align-items: center; justify-content: center; gap: 20px;
  height: 32px;
  background: #FAF6F1; border-bottom: 1px solid rgba(184,149,106,0.15);
  font-family: 'Heebo', sans-serif; font-size: 13px; color: #555;
  direction: rtl; letter-spacing: 0.2px;
}}
.bm-deskbar__sep {{ color: #B89562; opacity: 0.5; }}

/* ── Sticky topnav wrapper ──────────────────────────────────────── */
.bm-topnav-wrap {{
  position: sticky; top: 0; z-index: 200;
  background: #fff; border-bottom: 1px solid rgba(184,149,106,0.2);
  overflow: visible;
}}
.bm-topnav {{
  direction: rtl;
  max-width: 1400px; margin: 0 auto; padding: 0 32px;
  height: 64px;
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
}}

/* ── Logo ───────────────────────────────────────────────────────── */
.bm-topnav__logo {{
  text-decoration: none; flex-shrink: 0;
  font-family: 'Heebo', sans-serif; font-size: 20px; font-weight: 800; color: #2a2a2a;
}}
.bm-topnav__logo img {{ height: 38px; width: auto; display: block; }}

/* ── Category buttons ───────────────────────────────────────────── */
.bm-topnav__cats {{
  display: flex; align-items: center; gap: 2px;
  list-style: none; margin: 0; padding: 0; flex: 1; justify-content: center;
}}
.bm-topnav__cat-btn {{
  appearance: none; background: none; border: none; cursor: pointer;
  font-family: 'Heebo', sans-serif; font-size: 14px; font-weight: 700; color: #2a2a2a;
  padding: 8px 11px; border-radius: 8px; white-space: nowrap;
  transition: color 0.15s, background 0.15s; text-decoration: none; display: block;
  position: relative;
}}
.bm-topnav__cat-btn::after {{
  content: ''; position: absolute; bottom: 3px; left: 11px; right: 11px;
  height: 2px; background: #B89562; border-radius: 1px;
  opacity: 0; transform: scaleX(0); transition: opacity 0.15s, transform 0.15s;
  transform-origin: center;
}}
.bm-topnav__cat-btn:hover,
.bm-topnav__cat-btn[aria-expanded="true"] {{
  color: #B89562; background: #FAF6F1;
}}
.bm-topnav__cat-btn:hover::after,
.bm-topnav__cat-btn[aria-expanded="true"]::after {{ opacity: 1; transform: scaleX(1); }}

/* ── Icons ──────────────────────────────────────────────────────── */
.bm-topnav__icons {{ display: flex; align-items: center; gap: 4px; flex-shrink: 0; }}
.bm-topnav__icon-btn {{
  appearance: none; background: none; border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  padding: 9px; border-radius: 9px; color: #2a2a2a;
  transition: color 0.15s, background 0.15s; text-decoration: none;
}}
.bm-topnav__icon-btn:hover {{ color: #B89562; background: #FAF6F1; }}

/* ── Overlay ────────────────────────────────────────────────────── */
.bm-mega-overlay {{
  position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 150;
  background: rgba(0,0,0,0.15);
  opacity: 0; pointer-events: none; transition: opacity 0.2s ease;
}}
.bm-mega-overlay--visible {{ opacity: 1; pointer-events: auto; }}

/* ── Mega panel ─────────────────────────────────────────────────── */
.bm-mega {{
  position: absolute; top: 100%; left: 0; right: 0;
  background: #fff;
  border-top: 2px solid #B89562;
  border-bottom: 1px solid rgba(184,149,106,0.18);
  box-shadow: 0 16px 48px rgba(0,0,0,0.1);
  opacity: 0; transform: translateY(8px);
  pointer-events: none;
  transition: opacity 0.2s ease, transform 0.2s ease;
  direction: rtl;
}}
.bm-mega--open {{ opacity: 1; transform: translateY(0); pointer-events: auto; }}
.bm-mega--closing {{
  opacity: 0; transform: translateY(4px);
  transition: opacity 0.15s ease, transform 0.15s ease;
  pointer-events: none;
}}

/* ── Mega panel inner grid ──────────────────────────────────────── */
.bm-mega__panel {{
  display: none;
  max-width: 1400px; margin: 0 auto; padding: 28px 32px 24px;
  grid-template-columns: 200px 1fr 260px;
  gap: 40px; align-items: start;
}}
.bm-mega__panel--active {{ display: grid; }}

/* ── Right col: image links ─────────────────────────────────────── */
.bm-mega__imgs {{ display: flex; flex-direction: column; gap: 10px; }}
.bm-mega__img-link {{
  display: flex; align-items: center; gap: 10px;
  text-decoration: none; color: #2a2a2a;
  font-family: 'Heebo', sans-serif; font-size: 13px; font-weight: 700;
  padding: 7px 9px; border-radius: 10px;
  transition: background 0.13s;
}}
.bm-mega__img-link:hover {{ background: #FAF6F1; color: #B89562; }}
.bm-mega__img-thumb {{
  width: 64px; height: 64px; border-radius: 10px; object-fit: cover; flex-shrink: 0;
  border: 1.5px solid rgba(184,149,106,0.2);
}}

/* ── Middle col: links ──────────────────────────────────────────── */
.bm-mega__links {{ padding-top: 4px; }}
.bm-mega__links-heading {{
  font-family: 'Heebo', sans-serif; font-size: 11px; font-weight: 700;
  color: #bbb; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 12px;
}}
.bm-mega__link-list {{ list-style: none; margin: 0; padding: 0; columns: 2; column-gap: 8px; }}
.bm-mega__link {{
  display: block; font-family: 'Heebo', sans-serif; font-size: 14px; font-weight: 600;
  color: #2a2a2a; text-decoration: none;
  padding: 7px 10px; border-radius: 8px; break-inside: avoid;
  transition: background 0.12s, color 0.12s;
}}
.bm-mega__link:hover {{ background: #FAF6F1; color: #B89562; }}
.bm-mega__link--all {{
  color: #B89562; font-weight: 700; margin-top: 6px; column-span: all;
  display: inline-block;
}}
.bm-mega__link--all:hover {{ text-decoration: underline; background: none; }}

/* ── Left col: CTA banner ───────────────────────────────────────── */
.bm-mega__banner {{
  background: linear-gradient(145deg, #FAF6F1 0%, #fff9f3 100%);
  border: 1.5px solid rgba(184,149,106,0.2); border-radius: 14px;
  padding: 18px; display: flex; flex-direction: column; gap: 12px;
  min-height: 180px;
}}
.bm-mega__banner-img {{
  width: 100%; height: 110px; object-fit: cover; border-radius: 10px;
}}
.bm-mega__banner-title {{
  font-family: 'Heebo', sans-serif; font-size: 15px; font-weight: 800;
  color: #2a2a2a; margin: 0;
}}
.bm-mega__banner-sub {{
  font-family: 'Heebo', sans-serif; font-size: 12px; color: #777; margin: -6px 0 0;
}}
.bm-mega__banner-btn {{
  display: block; background: #B89562; color: #fff;
  font-family: 'Heebo', sans-serif; font-size: 13px; font-weight: 700;
  padding: 9px 16px; border-radius: 9px; text-decoration: none; text-align: center;
  margin-top: auto; transition: background 0.15s;
}}
.bm-mega__banner-btn:hover {{ background: #a07d50; }}

}} /* end @media 990px */
</style>

<!-- Trust Bar -->
<div class="bm-deskbar">
  <span>משלוח חינם מעל 199₪</span>
  <span class="bm-deskbar__sep">•</span>
  <span>30 יום החזרה</span>
  <span class="bm-deskbar__sep">•</span>
  <span>רכישה מאובטחת</span>
</div>

<!-- Desktop Nav -->
<div class="bm-topnav-wrap" id="bm-topnav-wrap">
  <div class="bm-topnav" dir="rtl">

    <!-- Logo -->
    <a href="/" class="bm-topnav__logo" aria-label="{{{{ shop.name }}}}">
      {{%- if settings.logo != blank -%}}
        <img src="{{{{ settings.logo | image_url: width: 200 }}}}" alt="{{{{ settings.logo.alt | default: shop.name | escape }}}}" height="38" loading="eager">
      {{%- else -%}}
        {{{{ shop.name }}}}
      {{%- endif -%}}
    </a>

    <!-- Categories -->
    <ul class="bm-topnav__cats" role="list">
      <li><button class="bm-topnav__cat-btn" data-panel="girls" aria-expanded="false" aria-haspopup="true">בנות</button></li>
      <li><button class="bm-topnav__cat-btn" data-panel="boys"  aria-expanded="false" aria-haspopup="true">בנים</button></li>
      <li><button class="bm-topnav__cat-btn" data-panel="reborn" aria-expanded="false" aria-haspopup="true">בובות ריבורן</button></li>
      <li><button class="bm-topnav__cat-btn" data-panel="shoes" aria-expanded="false" aria-haspopup="true">נעליים</button></li>
      <li><button class="bm-topnav__cat-btn" data-panel="sleep" aria-expanded="false" aria-haspopup="true">שינה טובה לתינוק</button></li>
      <li><button class="bm-topnav__cat-btn" data-panel="gifts" aria-expanded="false" aria-haspopup="true">מתנות ומארזים</button></li>
      <li><a href="/collections/summer-2024" class="bm-topnav__cat-btn">קיץ 2026</a></li>
    </ul>

    <!-- Icons -->
    <div class="bm-topnav__icons">
      <a href="/search" class="bm-topnav__icon-btn" aria-label="חיפוש">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      </a>
      <a href="/account" class="bm-topnav__icon-btn" aria-label="חשבון">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      </a>
      <a href="/cart" class="bm-topnav__icon-btn" aria-label="עגלה">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
      </a>
    </div>
  </div>

  <!-- Mega Menu Panel -->
  <div class="bm-mega" id="bm-mega" role="region">

    <!-- בנות -->
    <div class="bm-mega__panel" data-panel="girls">
      <div class="bm-mega__imgs">
        <a href="/collections/gender-girl" class="bm-mega__img-link">
          <img src="{CDN}/menu-girls.png" alt="בגדי בנות" class="bm-mega__img-thumb" loading="lazy">
          <span>כל בגדי הבנות</span>
        </a>
      </div>
      <div class="bm-mega__links">
        <p class="bm-mega__links-heading">לפי קטגוריה</p>
        <ul class="bm-mega__link-list">
          <li><a href="/collections/nav-girl-rompers" class="bm-mega__link">בגדי גוף ואוברולים</a></li>
          <li><a href="/collections/nav-girl-sets" class="bm-mega__link">סטים ומארזים</a></li>
          <li><a href="/collections/nav-girl-dress" class="bm-mega__link">שמלות וחצאיות</a></li>
          <li><a href="/collections/nav-girl-pajama" class="bm-mega__link">פיג׳מות</a></li>
          <li><a href="/collections/nav-girl-tops" class="bm-mega__link">חולצות וגופיות</a></li>
          <li><a href="/collections/nav-girl-pants" class="bm-mega__link">מכנסיים וטייצים</a></li>
          <li><a href="/collections/nav-girl-swim" class="bm-mega__link">בגדי ים</a></li>
          <li><a href="/collections/nav-girl-winter" class="bm-mega__link">בגדי חורף</a></li>
        </ul>
        <a href="/collections/gender-girl" class="bm-mega__link bm-mega__link--all">כל בגדי הבנות &larr;</a>
      </div>
      <div class="bm-mega__banner">
        <img src="{CDN}/menu-girls.png" alt="" class="bm-mega__banner-img" loading="lazy">
        <p class="bm-mega__banner-title">קולקציית בנות</p>
        <p class="bm-mega__banner-sub">placeholder — לעדכן תוכן</p>
        <a href="/collections/gender-girl" class="bm-mega__banner-btn">לקולקציה המלאה</a>
      </div>
    </div>

    <!-- בנים -->
    <div class="bm-mega__panel" data-panel="boys">
      <div class="bm-mega__imgs">
        <a href="/collections/gender-boy" class="bm-mega__img-link">
          <img src="{CDN}/menu-boys.png" alt="בגדי בנים" class="bm-mega__img-thumb" loading="lazy">
          <span>כל בגדי הבנים</span>
        </a>
      </div>
      <div class="bm-mega__links">
        <p class="bm-mega__links-heading">לפי קטגוריה</p>
        <ul class="bm-mega__link-list">
          <li><a href="/collections/nav-boy-rompers" class="bm-mega__link">בגדי גוף ואוברולים</a></li>
          <li><a href="/collections/nav-boy-sets" class="bm-mega__link">סטים ומארזים</a></li>
          <li><a href="/collections/nav-boy-pajama" class="bm-mega__link">פיג׳מות</a></li>
          <li><a href="/collections/nav-boy-tops" class="bm-mega__link">חולצות וגופיות</a></li>
          <li><a href="/collections/nav-boy-pants" class="bm-mega__link">מכנסיים</a></li>
          <li><a href="/collections/nav-boy-swim" class="bm-mega__link">בגדי ים</a></li>
          <li><a href="/collections/nav-boy-winter" class="bm-mega__link">בגדי חורף</a></li>
        </ul>
        <a href="/collections/gender-boy" class="bm-mega__link bm-mega__link--all">כל בגדי הבנים &larr;</a>
      </div>
      <div class="bm-mega__banner">
        <img src="{CDN}/menu-boys.png" alt="" class="bm-mega__banner-img" loading="lazy">
        <p class="bm-mega__banner-title">קולקציית בנים</p>
        <p class="bm-mega__banner-sub">placeholder — לעדכן תוכן</p>
        <a href="/collections/gender-boy" class="bm-mega__banner-btn">לקולקציה המלאה</a>
      </div>
    </div>

    <!-- ריבורן -->
    <div class="bm-mega__panel" data-panel="reborn">
      <div class="bm-mega__imgs">
        <a href="/collections/reborn" class="bm-mega__img-link">
          <img src="{CDN}/menu-reborn.png" alt="בובות ריבורן" class="bm-mega__img-thumb" loading="lazy">
          <span>בובות ריבורן</span>
        </a>
      </div>
      <div class="bm-mega__links">
        <p class="bm-mega__links-heading">קולקציה</p>
        <ul class="bm-mega__link-list">
          <li><a href="/collections/reborn" class="bm-mega__link">כל הבובות</a></li>
        </ul>
        <a href="/collections/reborn" class="bm-mega__link bm-mega__link--all">לקולקציה המלאה &larr;</a>
      </div>
      <div class="bm-mega__banner">
        <img src="{CDN}/menu-reborn.png" alt="" class="bm-mega__banner-img" loading="lazy">
        <p class="bm-mega__banner-title">בובות ריבורן</p>
        <p class="bm-mega__banner-sub">placeholder — לעדכן תוכן</p>
        <a href="/collections/reborn" class="bm-mega__banner-btn">לקולקציה</a>
      </div>
    </div>

    <!-- נעליים -->
    <div class="bm-mega__panel" data-panel="shoes">
      <div class="bm-mega__imgs">
        <a href="/collections/נעליים" class="bm-mega__img-link">
          <img src="{CDN}/menu-shoes.png" alt="נעליים" class="bm-mega__img-thumb" loading="lazy">
          <span>כל הנעליים</span>
        </a>
      </div>
      <div class="bm-mega__links">
        <p class="bm-mega__links-heading">לפי סוג</p>
        <ul class="bm-mega__link-list">
          <li><a href="/collections/nav-shoes-first-step" class="bm-mega__link">נעלי צעד ראשון</a></li>
          <li><a href="/collections/nav-shoes-sneakers" class="bm-mega__link">סניקרס</a></li>
          <li><a href="/collections/nav-shoes-sandals" class="bm-mega__link">סנדלים</a></li>
          <li><a href="/collections/nav-shoes-lights" class="bm-mega__link">נעלי אורות</a></li>
          <li><a href="/collections/nav-shoes-boots" class="bm-mega__link">מגפיים</a></li>
          <li><a href="/collections/nav-shoes-girl" class="bm-mega__link">נעלי בנות</a></li>
          <li><a href="/collections/nav-shoes-boy" class="bm-mega__link">נעלי בנים</a></li>
        </ul>
        <a href="/collections/נעליים" class="bm-mega__link bm-mega__link--all">כל הנעליים &larr;</a>
      </div>
      <div class="bm-mega__banner">
        <img src="{CDN}/menu-shoes.png" alt="" class="bm-mega__banner-img" loading="lazy">
        <p class="bm-mega__banner-title">נעלי תינוקות</p>
        <p class="bm-mega__banner-sub">placeholder — לעדכן תוכן</p>
        <a href="/collections/נעליים" class="bm-mega__banner-btn">לקולקציה המלאה</a>
      </div>
    </div>

    <!-- שינה -->
    <div class="bm-mega__panel" data-panel="sleep">
      <div class="bm-mega__imgs">
        <a href="/collections/המיוחדים-שלנו" class="bm-mega__img-link">
          <img src="{CDN}/menu-sleep.png" alt="שינה טובה לתינוק" class="bm-mega__img-thumb" loading="lazy">
          <span>שינה טובה לתינוק</span>
        </a>
      </div>
      <div class="bm-mega__links">
        <p class="bm-mega__links-heading">קולקציה</p>
        <ul class="bm-mega__link-list">
          <li><a href="/collections/המיוחדים-שלנו" class="bm-mega__link">כל המוצרים</a></li>
        </ul>
        <a href="/collections/המיוחדים-שלנו" class="bm-mega__link bm-mega__link--all">לקולקציה &larr;</a>
      </div>
      <div class="bm-mega__banner">
        <img src="{CDN}/menu-sleep.png" alt="" class="bm-mega__banner-img" loading="lazy">
        <p class="bm-mega__banner-title">שינה טובה לתינוק</p>
        <p class="bm-mega__banner-sub">placeholder — לעדכן תוכן</p>
        <a href="/collections/המיוחדים-שלנו" class="bm-mega__banner-btn">לקולקציה</a>
      </div>
    </div>

    <!-- מתנות -->
    <div class="bm-mega__panel" data-panel="gifts">
      <div class="bm-mega__imgs">
        <a href="/collections/מארזי-מתנה" class="bm-mega__img-link">
          <img src="{CDN}/menu-gifts.png" alt="מתנות ומארזים" class="bm-mega__img-thumb" loading="lazy">
          <span>מתנות ומארזים</span>
        </a>
      </div>
      <div class="bm-mega__links">
        <p class="bm-mega__links-heading">קולקציה</p>
        <ul class="bm-mega__link-list">
          <li><a href="/collections/מארזי-מתנה" class="bm-mega__link">מארזי מתנה</a></li>
          <li><a href="/collections/occ-gift" class="bm-mega__link">בגדים למתנה</a></li>
        </ul>
        <a href="/collections/מארזי-מתנה" class="bm-mega__link bm-mega__link--all">לקולקציה &larr;</a>
      </div>
      <div class="bm-mega__banner">
        <img src="{CDN}/menu-gifts.png" alt="" class="bm-mega__banner-img" loading="lazy">
        <p class="bm-mega__banner-title">מתנות לתינוק</p>
        <p class="bm-mega__banner-sub">placeholder — לעדכן תוכן</p>
        <a href="/collections/מארזי-מתנה" class="bm-mega__banner-btn">לקולקציה</a>
      </div>
    </div>

  </div><!-- /bm-mega -->
</div><!-- /bm-topnav-wrap -->

<!-- Overlay -->
<div class="bm-mega-overlay" id="bm-mega-overlay"></div>

<script>
(function() {{
  'use strict';
  var wrap    = document.getElementById('bm-topnav-wrap');
  var mega    = document.getElementById('bm-mega');
  var overlay = document.getElementById('bm-mega-overlay');
  var btns    = document.querySelectorAll('.bm-topnav__cat-btn[data-panel]');
  var closeTimer = null;
  var currentPanel = null;

  function openPanel(id) {{
    clearTimeout(closeTimer);
    if (currentPanel === id) return;
    currentPanel = id;
    // Panels
    document.querySelectorAll('.bm-mega__panel').forEach(function(p) {{
      p.classList.toggle('bm-mega__panel--active', p.dataset.panel === id);
    }});
    // Buttons
    btns.forEach(function(b) {{
      b.setAttribute('aria-expanded', b.dataset.panel === id ? 'true' : 'false');
    }});
    // Show
    mega.classList.remove('bm-mega--closing');
    mega.classList.add('bm-mega--open');
    overlay.classList.add('bm-mega-overlay--visible');
  }}

  function closePanel(instant) {{
    clearTimeout(closeTimer);
    if (!currentPanel) return;
    currentPanel = null;
    btns.forEach(function(b) {{ b.setAttribute('aria-expanded', 'false'); }});
    overlay.classList.remove('bm-mega-overlay--visible');
    if (instant) {{
      mega.classList.remove('bm-mega--open', 'bm-mega--closing');
      document.querySelectorAll('.bm-mega__panel').forEach(function(p) {{
        p.classList.remove('bm-mega__panel--active');
      }});
    }} else {{
      mega.classList.remove('bm-mega--open');
      mega.classList.add('bm-mega--closing');
      setTimeout(function() {{
        mega.classList.remove('bm-mega--closing');
        document.querySelectorAll('.bm-mega__panel').forEach(function(p) {{
          p.classList.remove('bm-mega__panel--active');
        }});
      }}, 160);
    }}
  }}

  function scheduleClose() {{
    closeTimer = setTimeout(function() {{
      if (!wrap.matches(':hover')) closePanel(false);
    }}, 300);
  }}

  // Hover
  btns.forEach(function(btn) {{
    btn.addEventListener('mouseenter', function() {{ openPanel(btn.dataset.panel); }});
    btn.addEventListener('mouseleave', scheduleClose);
  }});
  wrap.addEventListener('mouseenter', function() {{ clearTimeout(closeTimer); }});
  wrap.addEventListener('mouseleave', scheduleClose);

  // Click toggle
  btns.forEach(function(btn) {{
    btn.addEventListener('click', function(e) {{
      e.stopPropagation();
      if (currentPanel === btn.dataset.panel) {{ closePanel(false); }} else {{ openPanel(btn.dataset.panel); }}
    }});
  }});

  // Click outside
  overlay.addEventListener('click', function() {{ closePanel(false); }});
  document.addEventListener('click', function(e) {{
    if (currentPanel && !wrap.contains(e.target)) closePanel(false);
  }});

  // ESC
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape' && currentPanel) closePanel(false);
  }});
}})();
</script>
'''

# ── Modify header.liquid ───────────────────────────────────────────────────
RENDER_TAG = "{%- render 'bm-desktop-nav' -%}\n"

# Find insertion point: before <sticky-header or before <header
if '<sticky-header' in header_asset:
    insert_before = header_asset.index('<sticky-header')
elif '<header' in header_asset:
    insert_before = header_asset.index('<header')
else:
    print('ERROR: cannot find header insertion point')
    sys.exit(1)

if RENDER_TAG in header_asset:
    print('  render tag already present — skipping header modification')
    new_header = header_asset
else:
    new_header = header_asset[:insert_before] + RENDER_TAG + header_asset[insert_before:]
    print(f'  render tag inserted before char {insert_before}')

# ── Upload snippet ─────────────────────────────────────────────────────────
r1 = requests.put(BASE, headers=HJ, json={'asset': {'key': 'snippets/bm-desktop-nav.liquid', 'value': NAV_CONTENT}})
if r1.status_code in (200, 201):
    print(f'UPLOADED bm-desktop-nav.liquid: {len(NAV_CONTENT):,} chars')
else:
    print(f'ERROR snippet {r1.status_code}: {r1.text[:300]}')
    sys.exit(1)

# ── Upload header.liquid ───────────────────────────────────────────────────
if new_header != header_asset:
    r2 = requests.put(BASE, headers=HJ, json={'asset': {'key': 'sections/header.liquid', 'value': new_header}})
    if r2.status_code in (200, 201):
        print(f'UPLOADED sections/header.liquid: {len(new_header):,} chars')
    else:
        print(f'ERROR header {r2.status_code}: {r2.text[:300]}')
        sys.exit(1)

# ── Verify ─────────────────────────────────────────────────────────────────
time.sleep(1)
live_nav = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-desktop-nav.liquid'}).json()['asset']['value']
live_hdr = requests.get(BASE, headers=H, params={'asset[key]': 'sections/header.liquid'}).json()['asset']['value']

checks = {
    'snippet uploaded':           len(live_nav) > 5000,
    'trust bar':                  'bm-deskbar' in live_nav,
    'topnav sticky':              'position: sticky' in live_nav,
    'Dawn header hidden':         '.header-wrapper' in live_nav and 'display: none' in live_nav,
    'mega panel':                 'bm-mega' in live_nav,
    'girls panel':                'data-panel="girls"' in live_nav,
    'boys panel':                 'data-panel="boys"' in live_nav,
    'shoes sub-links':            'nav-shoes-first-step' in live_nav,
    'girls sub-links':            'nav-girl-rompers' in live_nav,
    'CDN images':                 'menu-girls.png' in live_nav,
    'overlay':                    'bm-mega-overlay' in live_nav,
    'JS open/close':              'openPanel' in live_nav,
    'ESC close':                  'Escape' in live_nav,
    '300ms hover delay':          '300' in live_nav,
    'render tag in header':       "render 'bm-desktop-nav'" in live_hdr,
}

all_ok = all(checks.values())
for k, v in checks.items():
    print(f'  {"V" if v else "X"} {k}')
print(f'\nSnippet size: {len(live_nav):,} chars')
print('\n' + ('הכל תקין - deploy to working theme DONE' if all_ok else 'SOME FAILED'))
if not all_ok:
    sys.exit(1)
