"""
Add 2 new categories to bm-mobile-nav.liquid:
1. אביזרים לתינוק — accordion with 4 sub-links
2. עיצוב וטקסטיל לחדרי ילדים — direct link
Both inserted before קיץ 2026 item.
"""
import requests, sys, time
sys.stdout.reconfigure(encoding='utf-8')

SHOP_URL      = 'a2756c-c0.myshopify.com'
WORKING_THEME = '187183563065'
LIVE_THEME    = '183668179257'

def load_env(path):
    env = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env

ENV = load_env(r'C:/Users/3024e/Desktop/shopify-token/.env')
CLIENT_ID     = ENV.get('SHOPIFY_CLIENT_ID', '896f1f2ea1a949303affac3d2c2a0d09')
CLIENT_SECRET = ENV.get('SHOPIFY_CLIENT_SECRET', '')

resp = requests.post(f'https://{SHOP_URL}/admin/oauth/access_token', data={
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
if resp.status_code != 200 or 'access_token' not in resp.text:
    print(f'AUTH FAILED {resp.status_code}: {resp.text[:200]}')
    sys.exit(1)
token = resp.json()['access_token']
H  = {'X-Shopify-Access-Token': token}
HJ = {**H, 'Content-Type': 'application/json'}

def get_asset(theme_id):
    url = f'https://{SHOP_URL}/admin/api/2024-10/themes/{theme_id}/assets.json'
    return requests.get(url, headers=H, params={'asset[key]': 'snippets/bm-mobile-nav.liquid'}).json()['asset']['value']

def put_asset(theme_id, value):
    url = f'https://{SHOP_URL}/admin/api/2024-10/themes/{theme_id}/assets.json'
    r = requests.put(url, headers=HJ, json={'asset': {'key': 'snippets/bm-mobile-nav.liquid', 'value': value}})
    return r.status_code, r.text

content = get_asset(WORKING_THEME)
print(f'Fetched working: {len(content):,} chars')
changes = 0

# ── 1. Add CSS for new category images ────────────────────────────────────────
OLD_CSS_IMAGES = '''.bm-nav__cat-image--summer { background-image: url(https://cdn.shopify.com/s/files/1/0864/9677/2409/files/menu-summer.png) !important; background-size: cover !important; background-position: center top !important; }'''

NEW_CSS_IMAGES = '''.bm-nav__cat-image--summer       { background-image: url(https://cdn.shopify.com/s/files/1/0864/9677/2409/files/menu-summer.png) !important; background-size: cover !important; background-position: center top !important; }
.bm-nav__cat-image--accessories  { background-image: url(https://cdn.shopify.com/s/files/1/0864/9677/2409/files/menu-accessories.png) !important; background-size: cover !important; background-position: center top !important; }
.bm-nav__cat-image--decor        { background-image: url(https://cdn.shopify.com/s/files/1/0864/9677/2409/files/menu-decor.png) !important; background-size: cover !important; background-position: center top !important; }'''

if OLD_CSS_IMAGES in content:
    content = content.replace(OLD_CSS_IMAGES, NEW_CSS_IMAGES, 1)
    changes += 1
    print('  Fix 1: CSS image classes added for accessories + decor')
else:
    print('  WARN Fix 1: summer CSS line not matched')

# ── 2. Add new nav items before קיץ item ──────────────────────────────────────
OLD_SUMMER_ITEM = '''        {%- comment -%} קיץ {%- endcomment -%}
        <li class="bm-nav__item">
          <a href="{{ routes.collections_url }}/summer-2024" class="bm-nav__cat-link">'''

NEW_ITEMS_PLUS_SUMMER = '''        {%- comment -%} אביזרים לתינוק {%- endcomment -%}
        <li class="bm-nav__item bm-nav__item--has-sub">
          <button class="bm-nav__cat-btn" aria-expanded="false" aria-controls="bm-sub-accessories">
            <div class="bm-nav__cat-inner">
              <div class="bm-nav__cat-image bm-nav__cat-image--accessories" aria-hidden="true"></div>
              <span class="bm-nav__cat-title">אביזרים לתינוק</span>
            </div>
            <span class="bm-nav__chevron">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
            </span>
          </button>
          <ul id="bm-sub-accessories" class="bm-nav__sub" role="list" hidden>
            <li><a href="{{ routes.collections_url }}/שמיכות-עיטוף-ושקי-שינה" class="bm-nav__sub-link">שמיכות עיטוף ושקי שינה</a></li>
            <li><a href="{{ routes.collections_url }}/תיקי-החתלה" class="bm-nav__sub-link">תיקי החתלה</a></li>
            <li><a href="{{ routes.collections_url }}/לידה-ואביזרים-נלווים" class="bm-nav__sub-link">לידה ואביזרים נלווים</a></li>
            <li><a href="{{ routes.collections_url }}/מוצרי-בטיחות" class="bm-nav__sub-link">מוצרי בטיחות</a></li>
          </ul>
        </li>

        {%- comment -%} עיצוב וטקסטיל {%- endcomment -%}
        <li class="bm-nav__item">
          <a href="{{ routes.collections_url }}/עיצוב-וטקסטיל-לחדרי-ילדים" class="bm-nav__cat-link">
            <div class="bm-nav__cat-inner">
              <div class="bm-nav__cat-image bm-nav__cat-image--decor" aria-hidden="true"></div>
              <span class="bm-nav__cat-title">עיצוב וטקסטיל לחדר</span>
            </div>
            <span class="bm-nav__chevron bm-nav__chevron--arrow">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            </span>
          </a>
        </li>

        {%- comment -%} קיץ {%- endcomment -%}
        <li class="bm-nav__item">
          <a href="{{ routes.collections_url }}/summer-2024" class="bm-nav__cat-link">'''

if OLD_SUMMER_ITEM in content:
    content = content.replace(OLD_SUMMER_ITEM, NEW_ITEMS_PLUS_SUMMER, 1)
    changes += 1
    print('  Fix 2: אביזרים + עיצוב items added before קיץ')
else:
    print('  WARN Fix 2: summer item anchor not matched')

print(f'\nTotal changes: {changes}/2')
if changes < 2:
    print('Not all changes applied — aborting')
    sys.exit(1)

# ── Upload to working theme ────────────────────────────────────────────────────
status, text = put_asset(WORKING_THEME, content)
if status in (200, 201):
    print(f'UPLOADED to working: {len(content):,} chars')
else:
    print(f'ERROR working {status}: {text[:200]}')
    sys.exit(1)

# ── Verify working ─────────────────────────────────────────────────────────────
time.sleep(2)
live_w = get_asset(WORKING_THEME)
checks_w = {
    'accessories accordion btn':  'aria-controls="bm-sub-accessories"' in live_w,
    'שמיכות sub-link':            '/שמיכות-עיטוף-ושקי-שינה' in live_w,
    'תיקי החתלה sub-link':       '/תיקי-החתלה' in live_w,
    'לידה sub-link':              '/לידה-ואביזרים-נלווים' in live_w,
    'בטיחות sub-link':            '/מוצרי-בטיחות' in live_w,
    'עיצוב direct link':          '/עיצוב-וטקסטיל-לחדרי-ילדים' in live_w,
    'CSS accessories class':      'bm-nav__cat-image--accessories' in live_w,
    'CSS decor class':            'bm-nav__cat-image--decor' in live_w,
    'קיץ still present':          'summer-2024' in live_w,
    'hookHamburger intact':       'hookHamburger' in live_w,
    'footer grid intact':         'repeat(5, 1fr)' in live_w,
}
all_w = all(checks_w.values())
print('\n── Working theme ──')
for k, v in checks_w.items():
    print(f'  {"V" if v else "X"} {k}')

if not all_w:
    print('Working verify FAILED — aborting before live deploy')
    sys.exit(1)

# ── Upload to LIVE theme ───────────────────────────────────────────────────────
status2, text2 = put_asset(LIVE_THEME, content)
if status2 in (200, 201):
    print(f'\nUPLOADED to LIVE: {len(content):,} chars')
else:
    print(f'ERROR live {status2}: {text2[:200]}')
    sys.exit(1)

time.sleep(2)
live_l = get_asset(LIVE_THEME)
all_l = all([
    'aria-controls="bm-sub-accessories"' in live_l,
    '/שמיכות-עיטוף-ושקי-שינה' in live_l,
    '/עיצוב-וטקסטיל-לחדרי-ילדים' in live_l,
    'hookHamburger' in live_l,
])
print('── Live theme ──')
print(f'  {"V" if all_l else "X"} כל הבדיקות')
print(f'\nSize: {len(live_l):,} chars')
print('\n' + ('הכל עלה — DONE' if all_l else 'LIVE VERIFY FAILED'))
if not all_l:
    sys.exit(1)
