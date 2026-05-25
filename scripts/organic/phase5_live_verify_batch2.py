"""
Phase 5 — Deep live verify: fetch each article from Shopify and check HTML structure.
Not just HTTP 200 — checks that all BabyMania structural elements are present.
"""

import sys
import requests
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shopify_client import _headers, BASE_URL
from scripts.organic.bm_html_converter import qa_checks

BLOG_ID = 109164036409

BATCH_2 = [
    {'id': 689005199673,  'hub': 'HUB-7/C6',      'slug': 'sakanot-babayit-letinok-asara-dugmaot'},
    {'id': 689005232441,  'hub': 'HUB-8/C6',       'slug': 'shgarat-erev-letinok-shlabim-leshina'},
    {'id': 689005265209,  'hub': 'HUB-16/Pillar',  'slug': 'crocs-leyeladim-madrih-male-mida-dagamim'},
    {'id': 689005297977,  'hub': 'HUB-16/C1',      'slug': 'crocs-letinok-meeize-gil-ma-livdok'},
    {'id': 689005330745,  'hub': 'HUB-16/C2',      'slug': 'sandalim-lapaut-mita-livhor'},
    {'id': 689005363513,  'hub': 'HUB-16/C3',      'slug': 'crocs-layam-valabreykha-mah-livdok'},
]


def fetch_article(article_id):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    return r.json()['article']


def main():
    print(f'=== PHASE 5 — DEEP LIVE VERIFY [{len(BATCH_2)} articles] ===\n')

    all_pass = True
    results = []

    for i, item in enumerate(BATCH_2, 1):
        aid  = item['id']
        hub  = item['hub']
        slug = item['slug']

        print(f'[{i}/6] {hub} — ID:{aid}')

        article = fetch_article(aid)
        pub_at   = article.get('published_at')
        handle   = article.get('handle', '?')
        body_html = article.get('body_html', '')

        live_url = f"https://babymania-il.com/blogs/news/{handle}"
        pub_ok   = pub_at is not None

        print(f'  published_at: {pub_at or "None (UNPUBLISHED!)"}')
        print(f'  handle:       {handle}')
        print(f'  body length:  {len(body_html):,} chars')

        checks = qa_checks(body_html, source_had_json_ld=True)
        # Also check that article is actually published
        checks.insert(0, ('is-published', pub_ok, '' if pub_ok else 'published_at is None'))

        fails = [(name, detail) for name, passed, detail in checks if not passed]
        passed_count = len(checks) - len(fails)

        status = 'PASS' if not fails else 'FAIL'
        icon   = '[PASS]' if not fails else '[FAIL]'
        print(f'  {icon} {passed_count}/{len(checks)} checks — {live_url}')

        if fails:
            all_pass = False
            for name, detail in fails:
                extra = f' ({detail})' if detail else ''
                print(f'    FAIL: {name}{extra}')

        results.append({'hub': hub, 'status': status, 'fails': fails, 'url': live_url})
        print()

    print('=== PHASE 5 SUMMARY ===')
    for r in results:
        s = r['status']
        print(f'  [{s}] {r["hub"]} — {r["url"]}')
        for name, detail in r.get('fails', []):
            print(f'        FAIL: {name}')

    if all_pass:
        print('\nAll 6/6 live articles PASS deep verify.')
        print('NEXT: Phase 6 — read-only audit of Batch 1')
    else:
        print('\nSome articles FAILED live verify — investigate before proceeding.')
        sys.exit(1)


if __name__ == '__main__':
    main()
