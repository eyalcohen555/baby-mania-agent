"""
Deploy bm-desktop-nav.liquid to LIVE theme (183668179257)
Copies the fixed snippet from working theme + patches header.liquid on live
"""
import requests, os, sys, time
sys.stdout.reconfigure(encoding='utf-8')

SHOP_URL      = 'a2756c-c0.myshopify.com'
WORKING_THEME = '187183563065'
LIVE_THEME    = '183668179257'

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

BASE_W = f'https://{SHOP_URL}/admin/api/2024-10/themes/{WORKING_THEME}/assets.json'
BASE_L = f'https://{SHOP_URL}/admin/api/2024-10/themes/{LIVE_THEME}/assets.json'

# ── 1. Fetch fixed snippet from working theme ──────────────────────────────
nav_content = requests.get(BASE_W, headers=H, params={'asset[key]': 'snippets/bm-desktop-nav.liquid'}).json()['asset']['value']
print(f'Fetched snippet from working: {len(nav_content):,} chars')

# Sanity check — must have the v2 fixes
assert 'header.header { display: none !important; }' in nav_content, 'Fix 1 missing'
assert 'display: grid !important' in nav_content, 'Fix 2 missing'
assert 'display: flex !important' in nav_content, 'Fix 3 missing'
print('  Sanity: all 3 fixes present')

# ── 2. Fetch header.liquid from LIVE theme ─────────────────────────────────
live_header = requests.get(BASE_L, headers=H, params={'asset[key]': 'sections/header.liquid'}).json()['asset']['value']
print(f'Fetched header.liquid from live: {len(live_header):,} chars')

RENDER_TAG = "{%- render 'bm-desktop-nav' -%}\n"
if RENDER_TAG in live_header:
    print('  render tag already present — skipping header modification')
    new_header = live_header
else:
    # Insert before <header class="header
    if '<header class="header' in live_header:
        insert_before = live_header.index('<header class="header')
    else:
        print('ERROR: cannot find insertion point in live header.liquid')
        sys.exit(1)
    new_header = live_header[:insert_before] + RENDER_TAG + live_header[insert_before:]
    print(f'  render tag inserted at char {insert_before}')

# ── 3. Upload snippet to LIVE ──────────────────────────────────────────────
r1 = requests.put(BASE_L, headers=HJ, json={'asset': {'key': 'snippets/bm-desktop-nav.liquid', 'value': nav_content}})
if r1.status_code in (200, 201):
    print(f'UPLOADED snippet to LIVE: {len(nav_content):,} chars')
else:
    print(f'ERROR snippet {r1.status_code}: {r1.text[:200]}')
    sys.exit(1)

# ── 4. Upload header.liquid to LIVE ───────────────────────────────────────
if new_header != live_header:
    r2 = requests.put(BASE_L, headers=HJ, json={'asset': {'key': 'sections/header.liquid', 'value': new_header}})
    if r2.status_code in (200, 201):
        print(f'UPLOADED header.liquid to LIVE: {len(new_header):,} chars')
    else:
        print(f'ERROR header {r2.status_code}: {r2.text[:200]}')
        sys.exit(1)

# ── 5. Verify ──────────────────────────────────────────────────────────────
time.sleep(2)
live_nav = requests.get(BASE_L, headers=H, params={'asset[key]': 'snippets/bm-desktop-nav.liquid'}).json()['asset']['value']
live_hdr = requests.get(BASE_L, headers=H, params={'asset[key]': 'sections/header.liquid'}).json()['asset']['value']

checks = {
    'snippet on live':               len(live_nav) > 20000,
    'Dawn header hidden (v2 fix)':   'header.header { display: none !important; }' in live_nav,
    'body padding reset':            'padding-top: 0 !important' in live_nav,
    'grid layout':                   'display: grid !important' in live_nav,
    'cats visible !important':       'display: flex !important' in live_nav,
    'CDN images':                    'menu-girls.png' in live_nav,
    'mega panel':                    'bm-mega__panel' in live_nav,
    'JS openPanel':                  'openPanel' in live_nav,
    'render tag in live header':     "render 'bm-desktop-nav'" in live_hdr,
    'mobile nav intact':             'bm-nav__overlay' in requests.get(BASE_L, headers=H, params={'asset[key]': 'snippets/bm-mobile-nav.liquid'}).json()['asset']['value'],
}
all_ok = all(checks.values())
for k, v in checks.items():
    print(f'  {"V" if v else "X"} {k}')
print(f'\nSnippet: {len(live_nav):,} chars')
print('\n' + ('LIVE DEPLOY DONE' if all_ok else 'SOME FAILED'))
if not all_ok:
    sys.exit(1)
