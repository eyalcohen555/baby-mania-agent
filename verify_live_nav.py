import requests, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SHOP_URL = 'a2756c-c0.myshopify.com'
LIVE_THEME = '183668179257'

_env = open(r'C:/Users/3024e/Desktop/shopify-token/.env').read().strip().split('=', 1)
_SECRET = _env[1] if len(_env) > 1 else os.environ.get('SHOPIFY_APP_SECRET', '')
resp = requests.post(f'https://{SHOP_URL}/admin/oauth/access_token', data={
    'grant_type': 'client_credentials',
    'client_id': '896f1f2ea1a949303affac3d2c2a0d09',
    'client_secret': _SECRET,
}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
token = resp.json()['access_token']
H = {'X-Shopify-Access-Token': token}
BASE = f'https://{SHOP_URL}/admin/api/2024-10/themes/{LIVE_THEME}/assets.json'

nav = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-mobile-nav.liquid'}).json()['asset']['value']
drawer = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/header-drawer.liquid'}).json()['asset']['value']

checks = {
    'bm-mobile-nav.liquid קיים':        len(nav) > 1000,
    'גודל סביר >20k':                   len(nav) > 20000,
    'render tag ב-header-drawer':       "render 'bm-mobile-nav'" in drawer,
    'CDN תמונות menu-girls.png':        'menu-girls.png' in nav,
    'background-image !important':      'background-image' in nav and '!important' in nav,
    'footer grid 5 עמודות':             'repeat(5, 1fr)' in nav,
    'footer SVG phone':                 'M22 16.92' in nav,
    'footer SVG whatsapp':              'M17.472' in nav,
    'צבעי אייקונים #1565C0':            '#1565C0' in nav,
    'pram SVG אודות':                   'M3 12h18' in nav,
    'media query 990px':                'min-width: 990px' in nav,
    'hookHamburger JS':                 'hookHamburger' in nav,
    'direction rtl':                    'direction: rtl' in nav,
    'no overflow-x issues':             'overflow-x: hidden' not in nav or 'bm-nav__overlay' in nav,
}

all_ok = all(checks.values())
for k, v in checks.items():
    print(f'  {"V" if v else "X"} {k}')
print(f'\nגודל קובץ: {len(nav):,} chars')
print('\n' + ('הכל תקין' if all_ok else 'יש בעיות — ראה למעלה'))
