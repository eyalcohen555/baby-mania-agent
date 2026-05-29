"""
Revert fix_footer_icons.py — remove bm-icon color classes, restore plain footer CSS
"""
import requests, os, sys, re
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

content = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-mobile-nav.liquid'}).json()['asset']['value']
print(f'Fetched: {len(content):,} chars')

# ── 1. Remove bm-icon-- classes from HTML ─────────────────────────────────
for name in ['phone', 'truck', 'return', 'about', 'wa']:
    content = content.replace(f' bm-icon--{name}', '')
print('  OK: removed bm-icon-- classes from HTML')

# ── 2. Replace new footer CSS with old clean version ──────────────────────
NEW_CSS_BLOCK = re.search(
    r'\.bm-nav__footer \{.*?@media screen',
    content, re.DOTALL
)

OLD_FOOTER_CSS = '''.bm-nav__footer {
  flex-shrink: 0; padding: 14px 16px 18px;
  background: #fff; border-top: 1px solid var(--bm-sep);
}
.bm-nav__social-proof {
  text-align: center; font-family: 'Heebo', sans-serif; font-size: 12px; font-weight: 700;
  color: var(--bm-gold); margin: 0 0 10px; letter-spacing: 0.4px;
}
.bm-nav__footer-links {
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px;
}
.bm-nav__footer-link {
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 5px;
  padding: 10px 4px 8px;
  background: var(--bm-cream); border: 1px solid rgba(184,149,106,0.2); border-radius: 12px;
  color: #3a3a3a; font-family: 'Heebo', sans-serif; font-size: 10px; font-weight: 700;
  text-decoration: none; text-align: center; line-height: 1.2;
  transition: background 0.15s, border-color 0.15s, transform 0.15s;
}
.bm-nav__footer-link:hover {
  background: #fff0e6; border-color: var(--bm-gold); color: var(--bm-brown); transform: translateY(-2px);
}
.bm-nav__flink-icon {
  color: var(--bm-gold); display: flex; align-items: center; justify-content: center;
}
.bm-nav__footer-link--wa .bm-nav__flink-icon { color: #25D366; }
.bm-nav__footer-link--wa:hover { border-color: #25D366; background: #f0faf4; color: #1a6b35; }

@media screen'''

if NEW_CSS_BLOCK:
    content = content[:NEW_CSS_BLOCK.start()] + OLD_FOOTER_CSS + content[NEW_CSS_BLOCK.end():]
    print('  OK: footer CSS reverted')
else:
    print('  WARN: footer CSS block not matched')

# ── Upload ─────────────────────────────────────────────────────────────────
import time
r2 = requests.put(BASE, headers=HJ, json={'asset': {'key': 'snippets/bm-mobile-nav.liquid', 'value': content}})
if r2.status_code in (200, 201):
    print(f'UPLOADED: {len(content):,} chars')
else:
    print(f'ERROR {r2.status_code}: {r2.text[:300]}')
    sys.exit(1)

time.sleep(0.5)
live = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-mobile-nav.liquid'}).json()['asset']['value']
checks = {
    'no bm-icon-- classes':        'bm-icon--' not in live,
    'no colored circles CSS':      '#1565C0' not in live and '#2E7D32' not in live,
    'footer still has SVG icons':  'M22 16.92' in live,
    'grid 5 cols intact':          'repeat(5, 1fr)' in live,
    'images still connected':      'menu-girls.png' in live,
    'media query intact':          '@media screen and (min-width: 990px)' in live,
    'JS hook intact':              'hookHamburger' in live,
}
all_ok = all(checks.values())
for k, v in checks.items():
    print(f'  {"✓" if v else "✗"} {k}')
print('\n' + ('REVERTED OK ✓' if all_ok else 'SOME ISSUES'))
