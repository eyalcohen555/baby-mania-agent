"""
Phase 4 — Re-publish corrected Batch 2 HTML to SAME article IDs.

SAFETY:
  - UPDATE only (PUT) — no new articles created
  - Only operates on the 6 known Batch 2 article IDs
  - Requires rendered HTML from Phase 3 to exist
  - Dry-run by default; --live required to write

Usage:
  python scripts/organic/phase4_republish_batch2.py          (dry-run)
  python scripts/organic/phase4_republish_batch2.py --live   (writes to Shopify)
"""

import sys
import re
import time
import argparse
import requests
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shopify_client import _headers, BASE_URL

BLOG_ID   = 109164036409
RENDER_DIR = Path(r'C:\Projects\baby-mania-agent\output\organic\rendered\batch2-fixed')
SOURCE_DIR = Path(r'C:\Projects\baby-mania-agent\output\organic')

BATCH_2 = [
    {'file': 'hub7-extension/HUB7_C6.md',   'html': 'HUB7_C6.html',    'id': 689005199673,  'hub': 'HUB-7/C6'},
    {'file': 'hub8-extension/HUB8_C6.md',   'html': 'HUB8_C6.html',    'id': 689005232441,  'hub': 'HUB-8/C6'},
    {'file': 'hub16-crocs/HUB16_Pillar.md', 'html': 'HUB16_Pillar.html','id': 689005265209,  'hub': 'HUB-16/Pillar'},
    {'file': 'hub16-crocs/HUB16_C1.md',     'html': 'HUB16_C1.html',    'id': 689005297977,  'hub': 'HUB-16/C1'},
    {'file': 'hub16-crocs/HUB16_C2.md',     'html': 'HUB16_C2.html',    'id': 689005330745,  'hub': 'HUB-16/C2'},
    {'file': 'hub16-crocs/HUB16_C3.md',     'html': 'HUB16_C3.html',    'id': 689005363513,  'hub': 'HUB-16/C3'},
]


def parse_frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m:
        raise ValueError('No frontmatter')
    fm = {}
    for line in m.group(1).splitlines():
        if ': ' in line:
            k, v = line.split(': ', 1)
            fm[k.strip()] = v.strip()
    return fm


def update_article(article_id, body_html, published=True):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    payload = {"article": {
        "id": article_id,
        "body_html": body_html,
        "published": published,
    }}
    r = requests.put(url, headers=_headers(), json=payload)
    r.raise_for_status()
    return r.json()['article']


def verify_article(article_id):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    return r.json()['article']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    live = args.live
    mode = 'LIVE' if live else 'DRY-RUN'

    print(f'=== PHASE 4 — RE-PUBLISH BATCH 2 [{mode}] ===\n')
    if not live:
        print('  [DRY-RUN] No Shopify writes. Add --live to publish.\n')

    results = []

    for i, item in enumerate(BATCH_2, 1):
        hub = item['hub']
        aid = item['id']
        html_path = RENDER_DIR / item['html']
        src_path  = SOURCE_DIR / item['file']

        print(f'[{i}/6] {hub} — ID:{aid}')

        if not html_path.exists():
            print(f'  MISSING rendered HTML: {html_path}')
            results.append({'hub': hub, 'status': 'MISSING_HTML'})
            continue

        body_html = html_path.read_text(encoding='utf-8')
        fm = parse_frontmatter(src_path.read_text(encoding='utf-8'))

        slug  = fm.get('slug', '?')
        title = fm.get('title', '?')

        print(f'  slug:  {slug}')
        print(f'  title: {title[:60]}')
        print(f'  html:  {len(body_html):,} chars')

        if not live:
            results.append({'hub': hub, 'id': aid, 'slug': slug, 'status': 'DRY-RUN-OK'})
            print()
            continue

        article = update_article(aid, body_html, published=True)
        pub_at  = article.get('published_at')
        live_url = f"https://babymania-il.com/blogs/news/{article['handle']}"
        status = 'UPDATED' if pub_at else 'UPDATE-NOT-PUBLISHED'
        print(f'  {status} — handle: {article["handle"]}')
        print(f'  URL: {live_url}')
        results.append({'hub': hub, 'id': aid, 'slug': slug,
                        'url': live_url, 'status': status})

        if i < len(BATCH_2):
            print('  pause 3s...')
            time.sleep(3)
        print()

    print(f'=== PHASE 4 SUMMARY [{mode}] ===')
    for r in results:
        s = r['status']
        icon = 'OK' if s in ('UPDATED', 'DRY-RUN-OK') else 'ERR'
        print(f'  [{icon}] {r["hub"]} — {r.get("slug","?")} [{s}]')
        if r.get('url'):
            print(f'       {r["url"]}')

    if live:
        ok = sum(1 for r in results if r['status'] == 'UPDATED')
        print(f'\nTotal: {ok}/6 updated')
        if ok == 6:
            print('NEXT: Phase 5 — deep live verify')
        else:
            print('WARNING: not all articles updated — check errors above')
    else:
        ok = sum(1 for r in results if r['status'] == 'DRY-RUN-OK')
        print(f'\nDry-run: {ok}/6 ready')
        print('Run with --live after confirming QA results.')


if __name__ == '__main__':
    main()
