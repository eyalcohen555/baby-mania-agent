"""
Add 2 new nav categories to bm-desktop-nav.liquid:
1. אביזרים לתינוק — mega panel with 4 sub-links
2. עיצוב וטקסטיל לחדרי ילדים — direct link (standalone)
"""
import requests, sys, time
sys.stdout.reconfigure(encoding='utf-8')

SHOP_URL      = 'a2756c-c0.myshopify.com'
WORKING_THEME = '187183563065'

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
BASE = f'https://{SHOP_URL}/admin/api/2024-10/themes/{WORKING_THEME}/assets.json'

content = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-desktop-nav.liquid'}).json()['asset']['value']
print(f'Fetched: {len(content):,} chars')
changes = 0

# ── 1. Add 2 new <li> buttons in the cats list (before closing </ul>) ──────────
OLD_CATS_END = '''      <li><a href="/collections/summer-2024" class="bm-topnav__cat-btn">קיץ 2026</a></li>
    </ul>'''

NEW_CATS_END = '''      <li><button class="bm-topnav__cat-btn" data-panel="accessories" aria-expanded="false" aria-haspopup="true">אביזרים לתינוק</button></li>
      <li><a href="/collections/עיצוב-וטקסטיל-לחדרי-ילדים" class="bm-topnav__cat-btn">עיצוב וטקסטיל</a></li>
      <li><a href="/collections/summer-2024" class="bm-topnav__cat-btn">קיץ 2026</a></li>
    </ul>'''

if OLD_CATS_END in content:
    content = content.replace(OLD_CATS_END, NEW_CATS_END, 1)
    changes += 1
    print('  Fix 1: 2 new category buttons added to topnav')
else:
    print('  WARN Fix 1: cats list end not matched')

# ── 2. Add accessories mega panel (before closing </div><!-- /bm-mega -->) ──────
OLD_MEGA_END = '''  </div><!-- /bm-mega -->
</div><!-- /bm-topnav-wrap -->'''

NEW_ACCESSORIES_PANEL = '''    <!-- אביזרים לתינוק -->
    <div class="bm-mega__panel" data-panel="accessories">
      <div class="bm-mega__imgs">
        <a href="/collections/לידה-ואביזרים-נלווים" class="bm-mega__img-link">
          <img src="https://cdn.shopify.com/s/files/1/0864/9677/2409/files/menu-accessories.png" alt="אביזרים לתינוק" class="bm-mega__img-thumb" loading="lazy">
          <span>אביזרים לתינוק</span>
        </a>
      </div>
      <div class="bm-mega__links">
        <p class="bm-mega__links-heading">לפי קטגוריה</p>
        <ul class="bm-mega__link-list">
          <li><a href="/collections/שמיכות-עיטוף-ושקי-שינה" class="bm-mega__link">שמיכות עיטוף ושקי שינה</a></li>
          <li><a href="/collections/תיקי-החתלה" class="bm-mega__link">תיקי החתלה</a></li>
          <li><a href="/collections/לידה-ואביזרים-נלווים" class="bm-mega__link">לידה ואביזרים נלווים</a></li>
          <li><a href="/collections/מוצרי-בטיחות" class="bm-mega__link">מוצרי בטיחות</a></li>
        </ul>
      </div>
      <div class="bm-mega__banner">
        <img src="https://cdn.shopify.com/s/files/1/0864/9677/2409/files/menu-accessories.png" alt="" class="bm-mega__banner-img" loading="lazy">
        <p class="bm-mega__banner-title">אביזרים לתינוק</p>
        <p class="bm-mega__banner-sub">כל מה שצריך — מלידה ועד הצעד הראשון</p>
        <a href="/collections/לידה-ואביזרים-נלווים" class="bm-mega__banner-btn">לכל האביזרים</a>
      </div>
    </div>

  </div><!-- /bm-mega -->
</div><!-- /bm-topnav-wrap -->'''

if OLD_MEGA_END in content:
    content = content.replace(OLD_MEGA_END, NEW_ACCESSORIES_PANEL, 1)
    changes += 1
    print('  Fix 2: accessories mega panel added')
else:
    print('  WARN Fix 2: mega end not matched')

print(f'\nTotal changes: {changes}/2')
if changes < 2:
    print('Not all changes applied — aborting')
    sys.exit(1)

# ── Upload to working theme ────────────────────────────────────────────────────
r = requests.put(BASE, headers=HJ, json={'asset': {'key': 'snippets/bm-desktop-nav.liquid', 'value': content}})
if r.status_code in (200, 201):
    print(f'UPLOADED: {len(content):,} chars')
else:
    print(f'ERROR {r.status_code}: {r.text[:200]}')
    sys.exit(1)

# ── Verify ─────────────────────────────────────────────────────────────────────
time.sleep(2)
live = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-desktop-nav.liquid'}).json()['asset']['value']
checks = {
    'accessories button in cats':       'data-panel="accessories"' in live,
    'עיצוב וטקסטיל link in cats':      '/collections/עיצוב-וטקסטיל-לחדרי-ילדים' in live,
    'accessories mega panel':           'data-panel="accessories"' in live and 'bm-mega__panel' in live,
    'שמיכות link':                      '/collections/שמיכות-עיטוף-ושקי-שינה' in live,
    'תיקי החתלה link':                  '/collections/תיקי-החתלה' in live,
    'לידה ואביזרים link':               '/collections/לידה-ואביזרים-נלווים' in live,
    'מוצרי בטיחות link':                '/collections/מוצרי-בטיחות' in live,
    'קיץ 2026 still present':           'summer-2024' in live,
    'girls panel intact':               'data-panel="girls"' in live,
    'mega JS intact':                   'openPanel' in live,
    'CDN images intact':                'menu-girls.png' in live,
}
all_ok = all(checks.values())
for k, v in checks.items():
    print(f'  {"V" if v else "X"} {k}')
print(f'\nSize: {len(live):,} chars')
print('\n' + ('כל השינויים עלו' if all_ok else 'SOME FAILED'))
if not all_ok:
    sys.exit(1)
