"""
ONLY 3 targeted changes to bm-mobile-nav.liquid:
1. Add bm-fi-* class to each footer icon span
2. Replace about SVG (info circle → pram)
3. INSERT new CSS before @media (no existing CSS touched)
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

original = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-mobile-nav.liquid'}).json()['asset']['value']
content = original
print(f'Fetched: {len(content):,} chars')

changes = 0

# ── Change 1: add bm-fi-* class to each footer span ──────────────────────────
SPAN_FIXES = [
    # contact
    ('<a href="/pages/contact" class="bm-nav__footer-link">\n          <span class="bm-nav__flink-icon">',
     '<a href="/pages/contact" class="bm-nav__footer-link">\n          <span class="bm-nav__flink-icon bm-fi-phone">'),
    # shipping
    ('<a href="/policies/shipping-policy" class="bm-nav__footer-link">\n          <span class="bm-nav__flink-icon">',
     '<a href="/policies/shipping-policy" class="bm-nav__footer-link">\n          <span class="bm-nav__flink-icon bm-fi-truck">'),
    # refund
    ('<a href="/policies/refund-policy" class="bm-nav__footer-link">\n          <span class="bm-nav__flink-icon">',
     '<a href="/policies/refund-policy" class="bm-nav__footer-link">\n          <span class="bm-nav__flink-icon bm-fi-return">'),
    # about
    ('<a href="/pages/about" class="bm-nav__footer-link">\n          <span class="bm-nav__flink-icon">',
     '<a href="/pages/about" class="bm-nav__footer-link">\n          <span class="bm-nav__flink-icon bm-fi-about">'),
    # whatsapp
    ('<span class="bm-nav__flink-icon">\n            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">',
     '<span class="bm-nav__flink-icon bm-fi-wa">\n            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">'),
]

for old, new in SPAN_FIXES:
    if old in content:
        content = content.replace(old, new, 1)
        changes += 1
    else:
        print(f'  WARN span not matched: {old[:60]}')

print(f'  Change 1: {changes} span classes added')

# ── Change 2: replace about SVG (info circle → pram) ─────────────────────────
OLD_ABOUT_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><path d="M12 8h.01M12 12v4"/></svg>'
NEW_ABOUT_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 12h18a9 9 0 0 0-18 0z"/><path d="M3 12v2a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1v-2"/><circle cx="8" cy="20" r="1.5"/><circle cx="16" cy="20" r="1.5"/><path d="M19.5 5.5l2-3"/></svg>'

if OLD_ABOUT_SVG in content:
    content = content.replace(OLD_ABOUT_SVG, NEW_ABOUT_SVG, 1)
    changes += 1
    print('  Change 2: about SVG replaced with pram')
else:
    print('  WARN: about SVG not found exactly')

# ── Change 3: INSERT new CSS block before @media (no existing CSS touched) ────
NEW_CSS = '''/* footer icon circles */
.bm-fi-phone, .bm-fi-truck, .bm-fi-return, .bm-fi-about, .bm-fi-wa {
  width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0;
}
.bm-fi-phone  { background: #E3F2FD; color: #1565C0; }
.bm-fi-truck  { background: #E8F5E9; color: #2E7D32; }
.bm-fi-return { background: #FFF3E0; color: #BF360C; }
.bm-fi-about  { background: #FCE4EC; color: #AD1457; }
.bm-fi-wa     { background: #E8F5E9; color: #1B5E20; }
.bm-nav__footer-link[href="/pages/contact"]:hover        { border-color: #90CAF9; transition: border-color 0.2s ease; }
.bm-nav__footer-link[href="/policies/shipping-policy"]:hover { border-color: #A5D6A7; transition: border-color 0.2s ease; }
.bm-nav__footer-link[href="/policies/refund-policy"]:hover   { border-color: #FFCC80; transition: border-color 0.2s ease; }
.bm-nav__footer-link[href="/pages/about"]:hover          { border-color: #F48FB1; transition: border-color 0.2s ease; }
.bm-nav__footer-link--wa:hover                           { border-color: #A5D6A7; transition: border-color 0.2s ease; }

'''

MEDIA_ANCHOR = '@media screen and (min-width: 990px)'
if MEDIA_ANCHOR in content:
    content = content.replace(MEDIA_ANCHOR, NEW_CSS + MEDIA_ANCHOR, 1)
    changes += 1
    print('  Change 3: CSS inserted before @media')
else:
    print('  WARN: @media anchor not found')

print(f'\nTotal changes: {changes}/4 expected')

# ── Overflow safety check ──────────────────────────────────────────────────
# Make sure no new rule has width/overflow on a non-contained element
danger_words = ['overflow: visible', 'overflow-x', 'min-width: 100vw', 'width: 100vw']
for d in danger_words:
    if d in NEW_CSS:
        print(f'  DANGER: "{d}" found in new CSS — aborting')
        sys.exit(1)
print('  Safety check: OK')

if changes < 4:
    print('  Not all changes applied — aborting upload')
    sys.exit(1)

# ── Upload ─────────────────────────────────────────────────────────────────
r2 = requests.put(BASE, headers=HJ, json={'asset': {'key': 'snippets/bm-mobile-nav.liquid', 'value': content}})
if r2.status_code in (200, 201):
    print(f'\nUPLOADED: {len(content):,} chars (was {len(original):,})')
else:
    print(f'ERROR {r2.status_code}: {r2.text[:300]}')
    sys.exit(1)

# ── Verify ─────────────────────────────────────────────────────────────────
time.sleep(0.5)
live = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-mobile-nav.liquid'}).json()['asset']['value']
checks = {
    'bm-fi-phone in HTML':    'class="bm-nav__flink-icon bm-fi-phone"' in live,
    'bm-fi-truck in HTML':    'class="bm-nav__flink-icon bm-fi-truck"' in live,
    'bm-fi-return in HTML':   'class="bm-nav__flink-icon bm-fi-return"' in live,
    'bm-fi-about in HTML':    'class="bm-nav__flink-icon bm-fi-about"' in live,
    'bm-fi-wa in HTML':       'bm-fi-wa' in live,
    'pram SVG (about)':       'circle cx="8" cy="20"' in live,
    'CSS blue #1565C0':       '#1565C0' in live,
    'CSS green #2E7D32':      '#2E7D32' in live,
    'CSS orange #BF360C':     '#BF360C' in live,
    'CSS pink #AD1457':       '#AD1457' in live,
    'hover #90CAF9':          '#90CAF9' in live,
    'images still OK':        'menu-girls.png' in live,
    'media query intact':     '@media screen and (min-width: 990px)' in live,
    'original size grew':     len(live) > len(original),
}
all_ok = all(checks.values())
for k, v in checks.items():
    print(f'  {"✓" if v else "✗"} {k}')
print('\n' + ('ALL PASS ✓' if all_ok else 'SOME FAILED — review above'))
if not all_ok:
    sys.exit(1)
