"""
Batch 1 BUG-3 Fix — Phase 3: Update existing articles (body_html ONLY).
PUT to same article IDs. No new articles. No title/slug/tag changes.

Usage:
  python batch1_fix_phase3_update.py          (dry-run)
  python batch1_fix_phase3_update.py --live   (writes to Shopify)
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

BLOG_ID    = 109164036409
RENDER_DIR = Path(r'C:\Projects\baby-mania-agent\output\organic\rendered\batch1-fixed')
SOURCE_DIR = Path(r'C:\Projects\baby-mania-agent\output\organic')

BATCH_1 = [
    {'id': 688897163577, 'hub': 'HUB-1/C5', 'html': 'HUB1_C5.html',
     'file': 'hub1-extension/HUB1_C5.md', 'slug': 'menorat-layla-letinok-ech-livhor'},
    {'id': 688897196345, 'hub': 'HUB-1/C6', 'html': 'HUB1_C6.html',
     'file': 'hub1-extension/HUB1_C6.md', 'slug': 'reash-lavan-letinok-im-ze-batuah'},
    {'id': 688897229113, 'hub': 'HUB-2/C6', 'html': 'HUB2_C6.html',
     'file': 'hub2-extension/HUB2_C6.md', 'slug': 'bgdei-tinokot-lefi-onot-ma-liknot'},
    {'id': 688897261881, 'hub': 'HUB-3/C5', 'html': 'HUB3_C5.html',
     'file': 'hub3-extension/HUB3_C5.md', 'slug': 'temperatura-mayim-ambatya-tinok'},
    {'id': 688897294649, 'hub': 'HUB-3/C6', 'html': 'HUB3_C6.html',
     'file': 'hub3-extension/HUB3_C6.md', 'slug': 'kama-peamim-lirhoz-tinok-beshavua'},
    {'id': 688897327417, 'hub': 'HUB-4/C5', 'html': 'HUB4_C5.html',
     'file': 'hub4-extension/HUB4_C5.md', 'slug': 'pricha-bor-tinok-ma-gorim-ech-lehagib'},
]


def parse_frontmatter_title(text):
    m = re.search(r'^title: (.+)$', text, re.MULTILINE)
    return m.group(1).strip() if m else '?'


def update_body_html_only(article_id, body_html):
    url     = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    payload = {"article": {"id": article_id, "body_html": body_html}}
    r = requests.put(url, headers=_headers(), json=payload)
    r.raise_for_status()
    return r.json()['article']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    live = args.live
    mode = 'LIVE' if live else 'DRY-RUN'

    print(f'=== BATCH 1 BUG-3 FIX — PHASE 3: UPDATE [{mode}] ===\n')
    if not live:
        print('  [DRY-RUN] No Shopify writes. Add --live to update.\n')

    results = []

    for i, item in enumerate(BATCH_1, 1):
        aid      = item['id']
        hub      = item['hub']
        slug     = item['slug']
        html_path = RENDER_DIR / item['html']
        src_path  = SOURCE_DIR / item['file']

        print(f'[{i}/6] {hub} — ID:{aid}')

        if not html_path.exists():
            print(f'  MISSING rendered HTML: {html_path}')
            results.append({'hub': hub, 'status': 'MISSING_HTML'})
            continue

        body_html = html_path.read_text(encoding='utf-8')
        title     = parse_frontmatter_title(src_path.read_text(encoding='utf-8'))

        print(f'  slug:  {slug}')
        print(f'  title: {title[:60]}')
        print(f'  html:  {len(body_html):,} chars')

        if not live:
            results.append({'hub': hub, 'id': aid, 'slug': slug, 'status': 'DRY-RUN-OK'})
            print()
            continue

        article  = update_body_html_only(aid, body_html)
        handle   = article.get('handle', '?')
        pub_at   = article.get('published_at')
        live_url = f"https://babymania-il.com/blogs/news/{handle}"

        # Verify nothing critical changed
        handle_ok = handle == slug
        title_ok  = article.get('title', '') == title

        status = 'UPDATED' if handle_ok else 'UPDATED-HANDLE-MISMATCH'
        print(f'  {status}')
        print(f'  handle: {handle} {"OK" if handle_ok else "MISMATCH!"}')
        print(f'  title unchanged: {"OK" if title_ok else "CHANGED!"}')
        print(f'  published: {pub_at}')
        print(f'  URL: {live_url}')

        results.append({'hub': hub, 'id': aid, 'slug': slug,
                        'url': live_url, 'status': status,
                        'handle_ok': handle_ok, 'title_ok': title_ok})

        if i < len(BATCH_1):
            print('  pause 3s...')
            time.sleep(3)
        print()

    print(f'=== PHASE 3 SUMMARY [{mode}] ===')
    for r in results:
        s    = r['status']
        icon = 'OK' if s in ('UPDATED', 'DRY-RUN-OK') else 'ERR'
        print(f'  [{icon}] {r["hub"]} — {r.get("slug","?")} [{s}]')
        if r.get('url'):
            print(f'       {r["url"]}')

    if live:
        ok = sum(1 for r in results if r['status'] == 'UPDATED')
        print(f'\nTotal: {ok}/6 updated')
        if ok == 6:
            print('NEXT: Phase 4 — deep live verify')
        else:
            print('WARNING: not all articles updated.')
    else:
        ok = sum(1 for r in results if r['status'] == 'DRY-RUN-OK')
        print(f'\nDry-run: {ok}/6 ready')
        print('Run with --live to apply.')


if __name__ == '__main__':
    main()
