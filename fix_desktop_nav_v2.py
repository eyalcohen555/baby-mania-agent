"""
Fix bm-desktop-nav.liquid — 3 targeted CSS fixes:
1. Hide Dawn's actual header element: header.header (was wrong: .header-wrapper)
2. Topnav layout: CSS grid (logo left | cats center | icons right), no RTL on container
3. Body padding reset + explicit visibility on cats
"""
import requests, os, sys, time
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

content = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-desktop-nav.liquid'}).json()['asset']['value']
print(f'Fetched: {len(content):,} chars')
changes = 0

# ── Fix 1: Wrong Dawn header selector ──────────────────────────────────────
OLD_HIDE = '/* ── Hide Dawn header ───────────────────────────────────────────── */\n.header-wrapper { display: none !important; }'
NEW_HIDE = '''/* ── Hide Dawn header ───────────────────────────────────────────── */
header.header { display: none !important; }
body { padding-top: 0 !important; }'''

if OLD_HIDE in content:
    content = content.replace(OLD_HIDE, NEW_HIDE, 1)
    changes += 1
    print('  Fix 1: Dawn header selector corrected + body padding reset')
else:
    print('  WARN Fix 1: old selector not matched')

# ── Fix 2: Topnav layout — RTL flex → CSS grid (logo left, cats center, icons right) ──
OLD_TOPNAV_CSS = '''.bm-topnav {
  direction: rtl;
  max-width: 1400px; margin: 0 auto; padding: 0 32px;
  height: 64px;
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
}'''

NEW_TOPNAV_CSS = '''.bm-topnav {
  max-width: 1400px; margin: 0 auto; padding: 0 32px;
  height: 64px;
  display: grid !important;
  grid-template-columns: auto 1fr auto;
  align-items: center; gap: 16px;
}'''

if OLD_TOPNAV_CSS in content:
    content = content.replace(OLD_TOPNAV_CSS, NEW_TOPNAV_CSS, 1)
    changes += 1
    print('  Fix 2: Topnav layout → CSS grid (logo left | cats center | icons right)')
else:
    print('  WARN Fix 2: old topnav CSS not matched')

# ── Fix 3: Cats display — add explicit visibility + justify-content ─────────
OLD_CATS_CSS = '''.bm-topnav__cats {
  display: flex; align-items: center; gap: 2px;
  list-style: none; margin: 0; padding: 0; flex: 1; justify-content: center;
}'''

NEW_CATS_CSS = '''.bm-topnav__cats {
  display: flex !important; align-items: center; gap: 2px;
  list-style: none !important; margin: 0; padding: 0;
  justify-content: center; visibility: visible !important;
}
.bm-topnav__cats li { display: block !important; list-style: none !important; }'''

if OLD_CATS_CSS in content:
    content = content.replace(OLD_CATS_CSS, NEW_CATS_CSS, 1)
    changes += 1
    print('  Fix 3: Cats visibility + justify-content fixed')
else:
    print('  WARN Fix 3: old cats CSS not matched')

# ── Fix 4: Cat button — add !important to ensure Dawn doesn't override ──────
OLD_BTN_CSS = '''.bm-topnav__cat-btn {
  appearance: none; background: none; border: none; cursor: pointer;
  font-family: 'Heebo', sans-serif; font-size: 14px; font-weight: 700; color: #2a2a2a;
  padding: 8px 11px; border-radius: 8px; white-space: nowrap;
  transition: color 0.15s, background 0.15s; text-decoration: none; display: block;
  position: relative;
}'''

NEW_BTN_CSS = '''.bm-topnav__cat-btn {
  appearance: none !important; background: none !important; border: none !important; cursor: pointer;
  font-family: 'Heebo', sans-serif !important; font-size: 14px !important; font-weight: 700 !important;
  color: #2a2a2a !important; padding: 8px 11px; border-radius: 8px; white-space: nowrap;
  transition: color 0.15s, background 0.15s; text-decoration: none !important;
  display: block !important; visibility: visible !important; opacity: 1 !important;
  position: relative; line-height: 1.2;
}'''

if OLD_BTN_CSS in content:
    content = content.replace(OLD_BTN_CSS, NEW_BTN_CSS, 1)
    changes += 1
    print('  Fix 4: Cat buttons — !important overrides added')
else:
    print('  WARN Fix 4: old button CSS not matched')

print(f'\nTotal fixes: {changes}/4')
if changes < 3:
    print('Too few fixes applied — aborting')
    sys.exit(1)

# ── Upload ────────────────────────────────────────────────────────────────
r = requests.put(BASE, headers=HJ, json={'asset': {'key': 'snippets/bm-desktop-nav.liquid', 'value': content}})
if r.status_code in (200, 201):
    print(f'UPLOADED: {len(content):,} chars')
else:
    print(f'ERROR {r.status_code}: {r.text[:200]}')
    sys.exit(1)

# ── Verify ────────────────────────────────────────────────────────────────
time.sleep(1)
live = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-desktop-nav.liquid'}).json()['asset']['value']
checks = {
    'header.header hidden':          'header.header { display: none !important; }' in live,
    'no .header-wrapper (old bug)':  '.header-wrapper { display: none' not in live,
    'body padding reset':            'padding-top: 0 !important' in live,
    'topnav grid layout':            'display: grid !important' in live,
    'grid-template-columns':         'grid-template-columns: auto 1fr auto' in live,
    'cats display flex !important':  'display: flex !important' in live,
    'cats li display block':         '.bm-topnav__cats li { display: block' in live,
    'btn color !important':          'color: #2a2a2a !important' in live,
    'btn display block !important':  'display: block !important' in live,
    'CDN images intact':             'menu-girls.png' in live,
    'mega panel intact':             'bm-mega__panel' in live,
    'JS intact':                     'openPanel' in live,
}
all_ok = all(checks.values())
for k, v in checks.items():
    print(f'  {"V" if v else "X"} {k}')
print('\n' + ('כל התיקונים עלו' if all_ok else 'SOME FAILED'))
if not all_ok:
    sys.exit(1)
