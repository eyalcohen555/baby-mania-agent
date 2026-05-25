"""
Batch 1 BUG-3 Fix — Phase 2: Render HTML locally + run QA.
No Shopify writes. Saves rendered HTML to output/organic/rendered/batch1-fixed/.
"""

import sys
import re
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.organic.bm_html_converter import convert, qa_checks

BASE_DIR = Path(r'C:\Projects\baby-mania-agent\output\organic')
OUT_DIR  = Path(r'C:\Projects\baby-mania-agent\output\organic\rendered\batch1-fixed')

BATCH_1 = [
    {'file': 'hub1-extension/HUB1_C5.md', 'hub': 'HUB-1/C5', 'id': 688897163577},
    {'file': 'hub1-extension/HUB1_C6.md', 'hub': 'HUB-1/C6', 'id': 688897196345},
    {'file': 'hub2-extension/HUB2_C6.md', 'hub': 'HUB-2/C6', 'id': 688897229113},
    {'file': 'hub3-extension/HUB3_C5.md', 'hub': 'HUB-3/C5', 'id': 688897261881},
    {'file': 'hub3-extension/HUB3_C6.md', 'hub': 'HUB-3/C6', 'id': 688897294649},
    {'file': 'hub4-extension/HUB4_C5.md', 'hub': 'HUB-4/C5', 'id': 688897327417},
]


def parse_frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    if not m:
        raise ValueError('No frontmatter')
    fm = {}
    for line in m.group(1).splitlines():
        if ': ' in line:
            k, v = line.split(': ', 1)
            fm[k.strip()] = v.strip()
    return fm, m.group(2).strip()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f'=== BATCH 1 BUG-3 FIX — PHASE 2: RENDER + QA [{len(BATCH_1)} articles] ===\n')

    all_pass = True
    results = []

    for i, item in enumerate(BATCH_1, 1):
        filepath = BASE_DIR / item['file']
        hub = item['hub']
        print(f'[{i}/{len(BATCH_1)}] {hub} — {filepath.name}')

        if not filepath.exists():
            print(f'  MISSING: {filepath}')
            results.append({'hub': hub, 'status': 'MISSING'})
            all_pass = False
            continue

        text = filepath.read_text(encoding='utf-8')
        fm, body_md = parse_frontmatter(text)

        source_has_json = '```json' in body_md or '<script type="application/ld+json">' in body_md

        html = convert(fm, body_md)

        out_name = filepath.stem + '.html'
        out_path = OUT_DIR / out_name
        out_path.write_text(html, encoding='utf-8')

        checks = qa_checks(html, source_had_json_ld=source_has_json)
        fails  = [(name, detail) for name, passed, detail in checks if not passed]

        status = 'PASS' if not fails else 'FAIL'
        icon   = '[PASS]' if not fails else '[FAIL]'
        slug   = fm.get('slug', '?')
        title  = fm.get('title', '?')

        print(f'  slug:  {slug}')
        print(f'  title: {title[:60]}')
        print(f'  html:  {len(html):,} chars')
        print(f'  {icon} {len(checks) - len(fails)}/{len(checks)} checks')
        print(f'  saved -> {out_path.name}')

        if fails:
            all_pass = False
            for name, detail in fails:
                extra = f' ({detail})' if detail else ''
                print(f'    FAIL: {name}{extra}')

        # Save QA JSON
        qa_path = OUT_DIR / (filepath.stem + '_qa.json')
        qa_path.write_text(
            json.dumps({
                'hub': hub, 'slug': slug, 'status': status,
                'html_len': len(html),
                'checks': [{'name': n, 'pass': p, 'detail': d}
                           for n, p, d in checks],
            }, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        results.append({'hub': hub, 'slug': slug, 'status': status,
                        'fails': fails, 'html_len': len(html)})
        print()

    print('=== PHASE 2 SUMMARY ===')
    for r in results:
        s = r['status']
        print(f'  [{s}] {r["hub"]} — {r.get("slug","?")} ({r.get("html_len",0):,} chars)')
        for name, detail in r.get('fails', []):
            print(f'        FAIL: {name}')

    if all_pass:
        print(f'\nAll {len(BATCH_1)}/6 articles PASS QA.')
        print('NEXT: run batch1_fix_phase3_update.py')
    else:
        print('\nQA FAILED — do NOT proceed to Phase 3.')
        sys.exit(1)


if __name__ == '__main__':
    main()
