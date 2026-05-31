"""
One-shot fix: convert HUB13_C1.md and update Shopify article 689095672121.
Runs full QA, backs up live HTML before write, verifies after.
"""
import sys
import json
import re
import requests
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT   = Path(r'C:\Projects\baby-mania-agent')
sys.path.insert(0, str(ROOT))

from scripts.organic.bm_html_converter import convert, qa_checks, validate_product_handles
from shopify_client import _headers, BASE_URL

BLOG_ID    = 109164036409
ARTICLE_ID = 689095672121
MD_FILE    = ROOT / 'output/organic/hub13-water-shoes/HUB13_C1.md'
BAK_DIR    = ROOT / 'output/organic/backups'

# ── Parse frontmatter ─────────────────────────────────────────────────────────
def parse_fm(text):
    m = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    if not m:
        raise ValueError('No frontmatter')
    fm = {}
    for line in m.group(1).splitlines():
        if ': ' in line:
            k, v = line.split(': ', 1)
            fm[k.strip()] = v.strip()
    return fm, m.group(2).strip()

# ── Step 1: convert ───────────────────────────────────────────────────────────
print('=== FIX HUB-13/C1 inline links ===\n')
print(f'Reading: {MD_FILE}')
text = MD_FILE.read_text(encoding='utf-8')
fm, body_md = parse_fm(text)
source_has_json = '<script type="application/ld+json">' in body_md

html = convert(fm, body_md)
checks = qa_checks(html, source_had_json_ld=source_has_json)

# Product handle gate
link_failures = validate_product_handles(html)
for lf in link_failures:
    checks.append((f'product-link-{lf["reason"].lower()}', False, lf['url']))

fails = [(n, d) for n, p, d in checks if not p]
passed = len(checks) - len(fails)
print(f'\nQA: {passed}/{len(checks)} checks')
if fails:
    for n, d in fails:
        print(f'  BLOCK: {n} {d}')
    print('\n=== BLOCKED — fix QA failures first ===')
    sys.exit(1)

# Verify inline links present
for slug in [
    'naalei-mayim-leyeladim-madrih-male-brekha-yam',
    'naal-tsaad-rishon-ma-kol-horeh-tzarich-ladaat',
    'brekha-im-tinok-bitakhon-tsiyud-ushahot-hamumlatsot',
]:
    if f'/blogs/news/{slug}' not in html:
        print(f'  MISSING inline link: {slug}')
        sys.exit(1)
print('  inline links: 3/3 PRESENT')

# ── Step 2: backup live HTML ──────────────────────────────────────────────────
print('\nBacking up live article...')
BAK_DIR.mkdir(parents=True, exist_ok=True)
url = f'{BASE_URL}/blogs/{BLOG_ID}/articles/{ARTICLE_ID}.json'
r = requests.get(url, headers=_headers())
r.raise_for_status()
live = r.json()['article']
bak = BAK_DIR / f'fix-c1-before-{ARTICLE_ID}.json'
bak.write_text(json.dumps(live, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'  Backup: {bak}')

# ── Step 3: update ────────────────────────────────────────────────────────────
print('\nUpdating article...')
payload = {'article': {'id': ARTICLE_ID, 'body_html': html}}
r = requests.put(url, headers=_headers(), json=payload)
r.raise_for_status()
updated = r.json()['article']
print(f'  UPDATED — ID:{updated["id"]} handle:{updated["handle"]}')

# ── Step 4: verify ────────────────────────────────────────────────────────────
print('\nVerifying live...')
r = requests.get(url, headers=_headers())
r.raise_for_status()
live_html = r.json()['article'].get('body_html', '')

live_checks = qa_checks(live_html, source_had_json_ld=True)
live_fails = [(n, d) for n, p, d in live_checks if not p]
live_passed = len(live_checks) - len(live_fails)
ratio = len(live_html) / len(html) if html else 0
len_ok = 0.90 <= ratio <= 1.10

print(f'  QA: {live_passed}/{len(live_checks)} | len ratio: {ratio:.2f} {"OK" if len_ok else "FAIL"}')
for slug in [
    'naalei-mayim-leyeladim-madrih-male-brekha-yam',
    'naal-tsaad-rishon-ma-kol-horeh-tzarich-ladaat',
    'brekha-im-tinok-bitakhon-tsiyud-ushahot-hamumlatsot',
]:
    present = f'/blogs/news/{slug}' in live_html
    print(f'  {"OK" if present else "MISSING"}: {slug}')

if live_fails or not len_ok:
    print('\n=== VERIFY FAILED ===')
    for n, d in live_fails:
        print(f'  FAIL: {n} {d}')
    sys.exit(1)

print(f'\n=== DONE — https://babymania-il.com/blogs/news/{updated["handle"]} ===')
