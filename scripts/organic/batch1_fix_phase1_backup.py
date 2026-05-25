"""
Batch 1 BUG-3 Fix — Phase 1: Backup live articles before HTML update.
READ-ONLY: only GETs from Shopify, saves JSON backup locally.
"""

import sys
import json
import requests
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shopify_client import _headers, BASE_URL

BLOG_ID    = 109164036409
BACKUP_DIR = Path(r'C:\Projects\baby-mania-agent\output\organic\backups')

BATCH_1 = [
    {'id': 688897163577, 'hub': 'HUB-1/C5', 'file': 'hub1-extension/HUB1_C5.md',
     'slug': 'menorat-layla-letinok-ech-livhor'},
    {'id': 688897196345, 'hub': 'HUB-1/C6', 'file': 'hub1-extension/HUB1_C6.md',
     'slug': 'reash-lavan-letinok-im-ze-batuah'},
    {'id': 688897229113, 'hub': 'HUB-2/C6', 'file': 'hub2-extension/HUB2_C6.md',
     'slug': 'bgdei-tinokot-lefi-onot-ma-liknot'},
    {'id': 688897261881, 'hub': 'HUB-3/C5', 'file': 'hub3-extension/HUB3_C5.md',
     'slug': 'temperatura-mayim-ambatya-tinok'},
    {'id': 688897294649, 'hub': 'HUB-3/C6', 'file': 'hub3-extension/HUB3_C6.md',
     'slug': 'kama-peamim-lirhoz-tinok-beshavua'},
    {'id': 688897327417, 'hub': 'HUB-4/C5', 'file': 'hub4-extension/HUB4_C5.md',
     'slug': 'pricha-bor-tinok-ma-gorim-ech-lehagib'},
]


def main():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = BACKUP_DIR / f'batch1-live-before-bug3-fix-{ts}.json'

    print(f'=== BATCH 1 BUG-3 FIX — PHASE 1: BACKUP ===')
    print(f'Articles: {len(BATCH_1)}')
    print(f'Backup: {backup_path}\n')

    backups = []
    all_ok = True

    for item in BATCH_1:
        aid  = item['id']
        hub  = item['hub']
        slug = item['slug']

        url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{aid}.json"
        r   = requests.get(url, headers=_headers())

        if r.status_code != 200:
            print(f'  [ERROR] {hub} — ID:{aid} — HTTP {r.status_code}')
            all_ok = False
            continue

        article = r.json()['article']
        backups.append(article)

        handle_ok = article.get('handle') == slug
        pub_at    = article.get('published_at')

        print(f'  [OK] {hub} — ID:{aid}')
        print(f'       handle: {article["handle"]} {"OK" if handle_ok else "MISMATCH!"}')
        print(f'       published: {pub_at}')
        print(f'       body: {len(article.get("body_html","")):,} chars')

    if not all_ok:
        print('\nSOME ARTICLES FAILED — aborting without writing backup.')
        sys.exit(1)

    backup_path.write_text(json.dumps(backups, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\n  Saved {len(backups)} articles -> {backup_path}')
    print(f'\n=== PHASE 1 COMPLETE — backup saved ===')
    print('NEXT: phase2_render_qa')


if __name__ == '__main__':
    main()
