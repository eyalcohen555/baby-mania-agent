"""
Phase 6 — READ-ONLY audit of Batch 1 (6 live articles) for the same 3 pipeline bugs.

NO writes to Shopify.
Reports: which bugs are present in each article.

Bug definitions:
  BUG-1: <pre><code> blocks — JSON-LD code fence rendered as visible text
  BUG-2: [IMG_ALT_N: ...] markers — visible as text
  BUG-3: No BabyMania HTML structure (no intro-box, toc, article-body, cta-banner, faq)
"""

import sys
import requests
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shopify_client import _headers, BASE_URL

BLOG_ID  = 109164036409
BASE_DIR = Path(r'C:\Projects\baby-mania-agent\output\organic')

BATCH_1 = [
    {'file': 'hub1-extension/HUB1_C5.md', 'hub': 'HUB-1/C5'},
    {'file': 'hub1-extension/HUB1_C6.md', 'hub': 'HUB-1/C6'},
    {'file': 'hub2-extension/HUB2_C6.md', 'hub': 'HUB-2/C6'},
    {'file': 'hub3-extension/HUB3_C5.md', 'hub': 'HUB-3/C5'},
    {'file': 'hub3-extension/HUB3_C6.md', 'hub': 'HUB-3/C6'},
    {'file': 'hub4-extension/HUB4_C5.md', 'hub': 'HUB-4/C5'},
]


def parse_frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ': ' in line:
            k, v = line.split(': ', 1)
            fm[k.strip()] = v.strip()
    return fm


def fetch_by_handle(handle):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json?handle={handle}&limit=1"
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    articles = r.json().get('articles', [])
    if articles and articles[0].get('handle') == handle:
        return articles[0]
    return None


def audit_html(html):
    bugs = []
    if '<pre><code>' in html:
        count = html.count('<pre><code>')
        bugs.append(f'BUG-1 <pre><code> blocks: {count}')
    if '[IMG_ALT_' in html:
        count = len(re.findall(r'\[IMG_ALT_\d+:', html))
        bugs.append(f'BUG-2 [IMG_ALT_N: markers: {count}')
    structure_missing = []
    for cls in ('intro-box', 'toc', 'article-body', 'cta-banner'):
        if f'class="{cls}"' not in html:
            structure_missing.append(cls)
    if 'id="faq"' not in html:
        structure_missing.append('faq')
    if structure_missing:
        bugs.append(f'BUG-3 missing structure: {", ".join(structure_missing)}')
    return bugs


def main():
    print(f'=== PHASE 6 — BATCH 1 AUDIT (READ-ONLY) [{len(BATCH_1)} articles] ===\n')

    results = []

    for i, item in enumerate(BATCH_1, 1):
        filepath = BASE_DIR / item['file']
        hub = item['hub']

        print(f'[{i}/6] {hub} — {filepath.name}')

        if not filepath.exists():
            print(f'  MISSING source: {filepath}')
            results.append({'hub': hub, 'status': 'NO_SOURCE'})
            continue

        fm = parse_frontmatter(filepath.read_text(encoding='utf-8'))
        handle = fm.get('slug', '')

        if not handle:
            print(f'  no slug in frontmatter')
            results.append({'hub': hub, 'status': 'NO_SLUG'})
            continue

        article = fetch_by_handle(handle)

        if not article:
            print(f'  NOT FOUND on Shopify (handle: {handle})')
            results.append({'hub': hub, 'status': 'NOT_ON_SHOPIFY', 'handle': handle})
            continue

        body_html = article.get('body_html', '')
        pub_at = article.get('published_at')
        live_url = f"https://babymania-il.com/blogs/news/{handle}"

        print(f'  ID:        {article["id"]}')
        print(f'  published: {pub_at or "UNPUBLISHED"}')
        print(f'  body len:  {len(body_html):,} chars')

        bugs = audit_html(body_html)

        if not bugs:
            print(f'  [CLEAN] No bugs detected — {live_url}')
            results.append({'hub': hub, 'status': 'CLEAN', 'url': live_url, 'id': article['id']})
        else:
            print(f'  [BUGS FOUND] {len(bugs)} issues:')
            for b in bugs:
                print(f'    - {b}')
            print(f'  URL: {live_url}')
            results.append({'hub': hub, 'status': 'BUGS', 'bugs': bugs,
                            'url': live_url, 'id': article['id']})
        print()

    # Summary
    print('=== PHASE 6 SUMMARY ===')
    clean = [r for r in results if r['status'] == 'CLEAN']
    buggy = [r for r in results if r['status'] == 'BUGS']

    for r in results:
        s = r['status']
        print(f'  [{s}] {r["hub"]}')
        for b in r.get('bugs', []):
            print(f'        {b}')

    print(f'\nClean: {len(clean)}/6  |  Bugs found: {len(buggy)}/6')
    if buggy:
        print('\nACTION REQUIRED: Batch 1 articles have same pipeline bugs.')
        print('Recommend scheduling Batch 1 fix using same bm_html_converter pipeline.')
    else:
        print('\nBatch 1 is clean — no action needed.')


if __name__ == '__main__':
    main()
