"""
Fix bm-mobile-nav.liquid:
1. Images — use explicit background-image with !important
2. Footer — compact premium grid with SVG icons
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

content = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-mobile-nav.liquid'}).json()['asset']['value']
print(f'Fetched: {len(content):,} chars')

changes = 0

# ── 1. Fix image CSS: background → background-image !important ─────────────
for name in ['girls', 'boys', 'reborn', 'shoes', 'sleep', 'gifts', 'summer']:
    # Match both the old shorthand style and any existing version
    old = f'.bm-nav__cat-image--{name}'
    # Find the full line and replace it
    lines = content.split('\n')
    new_lines = []
    replaced = False
    for line in lines:
        if line.strip().startswith(f'.bm-nav__cat-image--{name}') and 'background' in line:
            new_lines.append(f'.bm-nav__cat-image--{name.ljust(6)} {{ background-image: url({CDN}/menu-{name}.png) !important; background-size: cover !important; background-position: center top !important; }}')
            replaced = True
        else:
            new_lines.append(line)
    if replaced:
        content = '\n'.join(new_lines)
        changes += 1
        print(f'  OK image: {name}')
    else:
        print(f'  SKIP image (not found): {name}')

# ── 2. Fix base cat-image CSS: add display:block + explicit size ───────────
old_base = '''.bm-nav__cat-image {
  display: block !important;
  width: 56px !important; height: 56px !important; border-radius: 50% !important;
  flex-shrink: 0; overflow: hidden;
  border: 2px solid rgba(184,149,106,0.35);
  box-shadow: 0 2px 10px rgba(184,149,106,0.2);
  background-color: #f5ede3;
  background-size: cover !important;
  background-position: center !important;
  background-repeat: no-repeat !important;
}'''

if 'display: block !important' not in content:
    # Find and replace the existing base rule
    lines = content.split('\n')
    new_lines = []
    in_rule = False
    brace_depth = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if '.bm-nav__cat-image {' in line and 'image--' not in line:
            # Start of base rule — collect until closing brace
            in_rule = True
            brace_depth = line.count('{') - line.count('}')
            # Replace with new
            new_lines.append(old_base)
            while in_rule and i + 1 < len(lines):
                i += 1
                brace_depth += lines[i].count('{') - lines[i].count('}')
                if brace_depth <= 0:
                    in_rule = False
        else:
            new_lines.append(line)
        i += 1
    content = '\n'.join(new_lines)
    changes += 1
    print('  OK base cat-image rule fixed')

# ── 3. Replace footer HTML ─────────────────────────────────────────────────
NEW_FOOTER_HTML = '''    <div class="bm-nav__footer">
      <p class="bm-nav__social-proof">⭐ 8,500+ משפחות כבר בחרו בנו</p>
      <div class="bm-nav__footer-links">
        <a href="/pages/contact" class="bm-nav__footer-link">
          <span class="bm-nav__flink-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.7 11.5 19.79 19.79 0 0 1 1.66 2.84 2 2 0 0 1 3.64 1h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.63a16 16 0 0 0 6 6l.98-.98a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 21.73 16z"/></svg>
          </span>
          <span>צור קשר</span>
        </a>
        <a href="/policies/shipping-policy" class="bm-nav__footer-link">
          <span class="bm-nav__flink-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
          </span>
          <span>משלוחים</span>
        </a>
        <a href="/policies/refund-policy" class="bm-nav__footer-link">
          <span class="bm-nav__flink-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.91"/></svg>
          </span>
          <span>החזרות</span>
        </a>
        <a href="/pages/about" class="bm-nav__footer-link">
          <span class="bm-nav__flink-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><path d="M12 8h.01M12 12v4"/></svg>
          </span>
          <span>אודות</span>
        </a>
        <a href="https://wa.me/972XXXXXXXXX" class="bm-nav__footer-link bm-nav__footer-link--wa" rel="noopener">
          <span class="bm-nav__flink-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>
          </span>
          <span>וואטסאפ</span>
        </a>
      </div>
    </div>'''

# Replace everything between <div class="bm-nav__footer"> and its closing </div>
import re
pattern = r'    <div class="bm-nav__footer">.*?    </div>(?=\s*\n\s*</div>)'
match = re.search(pattern, content, re.DOTALL)
if match:
    content = content[:match.start()] + NEW_FOOTER_HTML + content[match.end():]
    changes += 1
    print('  OK footer HTML replaced')
else:
    print('  WARN footer HTML not matched by regex')

# ── 4. Replace footer CSS ──────────────────────────────────────────────────
NEW_FOOTER_CSS = '''.bm-nav__footer {
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
.bm-nav__footer-link--wa:hover { border-color: #25D366; background: #f0faf4; color: #1a6b35; }'''

# Replace old footer CSS block
old_footer_css_pattern = r'\.bm-nav__footer \{[^}]+\}[\s\S]*?\.bm-nav__payment-icons img \{[^}]+\}'
match2 = re.search(old_footer_css_pattern, content)
if match2:
    content = content[:match2.start()] + NEW_FOOTER_CSS + content[match2.end():]
    changes += 1
    print('  OK footer CSS replaced')
else:
    # Try simpler: just append after existing footer section
    print('  WARN footer CSS not matched — trying line-by-line')
    # At least update the footer display
    content = re.sub(
        r'display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;',
        'display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px;',
        content
    )
    content = re.sub(
        r'display: inline-flex; align-items: center; gap: 4px;\s+padding: 8px 12px;',
        'display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 5px;\n  padding: 10px 4px 8px;',
        content
    )
    changes += 1
    print('  OK footer CSS patched partially')

print(f'\nTotal changes applied: {changes}')

# ── Upload ─────────────────────────────────────────────────────────────────
r2 = requests.put(BASE, headers=HJ, json={'asset': {'key': 'snippets/bm-mobile-nav.liquid', 'value': content}})
if r2.status_code in (200, 201):
    print(f'UPLOADED: {len(content):,} chars')
else:
    print(f'ERROR {r2.status_code}: {r2.text[:300]}')
    sys.exit(1)

# ── Verify ─────────────────────────────────────────────────────────────────
time.sleep(0.5)
live = requests.get(BASE, headers=H, params={'asset[key]': 'snippets/bm-mobile-nav.liquid'}).json()['asset']['value']
checks = {
    'background-image girls':   f'menu-girls.png) !important' in live,
    'background-image boys':    f'menu-boys.png) !important' in live,
    'background-size cover':    'background-size: cover !important' in live,
    'footer grid 5 cols':       'repeat(5, 1fr)' in live,
    'footer flex-direction col': 'flex-direction: column' in live,
    'SVG phone icon':            'M22 16.92' in live,
    'SVG truck icon':            'M16 8 20 8' in live or 'polygon points' in live,
    'SVG whatsapp':              'M17.472' in live,
    'flink-icon class':          'bm-nav__flink-icon' in live,
    'no payment icons':          'payment-icons' not in live,
}
all_ok = all(checks.values())
for k, v in checks.items():
    print(f'  {"✓" if v else "✗"} {k}')
print('\n' + ('ALL PASS' if all_ok else 'SOME FAILED'))
