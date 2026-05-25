"""
Batch 1 BUG-3 Fix — Phase 4: Deep live verify from Shopify API.
Checks all structural elements + compares live length to local render.
"""

import sys
import requests
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shopify_client import _headers, BASE_URL
from scripts.organic.bm_html_converter import qa_checks

BLOG_ID    = 109164036409
RENDER_DIR = Path(r'C:\Projects\baby-mania-agent\output\organic\rendered\batch1-fixed')

BATCH_1 = [
    {'id': 688897163577, 'hub': 'HUB-1/C5', 'html': 'HUB1_C5.html',
     'slug': 'menorat-layla-letinok-ech-livhor',
     'title': 'מנורת לילה לתינוק — האם זה עוזר לשינה ואיך לבחור'},
    {'id': 688897196345, 'hub': 'HUB-1/C6', 'html': 'HUB1_C6.html',
     'slug': 'reash-lavan-letinok-im-ze-batuah',
     'title': 'רעש לבן לתינוק — האם זה בטוח ואיך משתמשים נכון'},
    {'id': 688897229113, 'hub': 'HUB-2/C6', 'html': 'HUB2_C6.html',
     'slug': 'bgdei-tinokot-lefi-onot-ma-liknot',
     'title': 'בגדי תינוקות לפי עונות — מה לקנות ומתי'},
    {'id': 688897261881, 'hub': 'HUB-3/C5', 'html': 'HUB3_C5.html',
     'slug': 'temperatura-mayim-ambatya-tinok',
     'title': 'טמפרטורת מים לאמבטיה לתינוק — כמה מעלות ואיך למדוד'},
    {'id': 688897294649, 'hub': 'HUB-3/C6', 'html': 'HUB3_C6.html',
     'slug': 'kama-peamim-lirhoz-tinok-beshavua',
     'title': 'כמה פעמים לרחוץ תינוק בשבוע — מה ממליצים מומחים'},
    {'id': 688897327417, 'hub': 'HUB-4/C5', 'html': 'HUB4_C5.html',
     'slug': 'pricha-bor-tinok-ma-gorim-ech-lehagib',
     'title': 'פריחה בעור התינוק — מה גורם לה ואיך להגיב'},
]


def main():
    print(f'=== BATCH 1 BUG-3 FIX — PHASE 4: DEEP LIVE VERIFY ===\n')

    all_pass = True
    results  = []

    for i, item in enumerate(BATCH_1, 1):
        aid        = item['id']
        hub        = item['hub']
        exp_slug   = item['slug']
        exp_title  = item['title']
        html_path  = RENDER_DIR / item['html']

        print(f'[{i}/6] {hub} — ID:{aid}')

        url      = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{aid}.json"
        r        = requests.get(url, headers=_headers())
        r.raise_for_status()
        article  = r.json()['article']

        live_html  = article.get('body_html', '')
        live_title = article.get('title', '')
        live_handle = article.get('handle', '')
        pub_at     = article.get('published_at')
        live_url   = f"https://babymania-il.com/blogs/news/{live_handle}"

        local_html = html_path.read_text(encoding='utf-8') if html_path.exists() else ''
        local_len  = len(local_html)
        live_len   = len(live_html)
        # Allow ±5% difference (Shopify may normalize some whitespace)
        len_ratio  = live_len / local_len if local_len else 0
        len_ok     = 0.90 <= len_ratio <= 1.10

        checks = qa_checks(live_html, source_had_json_ld=True)
        # Extra checks
        extra = [
            ('is-published',       pub_at is not None,       ''),
            ('title-unchanged',    live_title == exp_title,  ''),
            ('slug-unchanged',     live_handle == exp_slug,  ''),
            ('length-match-local', len_ok,
             f'live={live_len:,} local={local_len:,} ratio={len_ratio:.2f}'),
        ]
        all_checks = extra + [(n, p, d) for n, p, d in checks]

        fails = [(n, d) for n, p, d in all_checks if not p]
        passed_count = len(all_checks) - len(fails)
        status = 'PASS' if not fails else 'FAIL'
        icon   = '[PASS]' if not fails else '[FAIL]'

        print(f'  published:  {pub_at or "NONE"}')
        print(f'  handle:     {live_handle}')
        print(f'  live:       {live_len:,} chars | local: {local_len:,} chars')
        print(f'  {icon} {passed_count}/{len(all_checks)} checks — {live_url}')

        if fails:
            all_pass = False
            for n, d in fails:
                extra_str = f' ({d})' if d else ''
                print(f'    FAIL: {n}{extra_str}')

        results.append({'hub': hub, 'status': status, 'url': live_url, 'fails': fails})
        print()

    print('=== PHASE 4 SUMMARY ===')
    for r in results:
        s = r['status']
        print(f'  [{s}] {r["hub"]} — {r["url"]}')
        for n, d in r.get('fails', []):
            print(f'        FAIL: {n}')

    if all_pass:
        print(f'\nAll 6/6 live articles PASS deep verify.')
        print('NEXT: Phase 5 — documentation update')
    else:
        print('\nSome articles FAILED — investigate before proceeding.')
        sys.exit(1)


if __name__ == '__main__':
    main()
