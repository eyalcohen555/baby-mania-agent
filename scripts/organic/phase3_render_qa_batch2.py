"""
Phase 3 — Render corrected HTML locally + run QA for all 6 Batch 2 articles.

Reads source .md files, runs bm_html_converter, saves HTML to
output/organic/rendered/batch2-fixed/, then runs 13 QA checks per article.

STOP condition: any single QA check failure → exit 1.
No Shopify writes in this phase.
"""

import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.organic.bm_html_converter import convert, qa_checks

BASE_DIR = Path(r'C:\Projects\baby-mania-agent\output\organic')
OUT_DIR  = Path(r'C:\Projects\baby-mania-agent\output\organic\rendered\batch2-fixed')

BATCH_2 = [
    {'file': 'hub7-extension/HUB7_C6.md',    'hub': 'HUB-7/C6'},
    {'file': 'hub8-extension/HUB8_C6.md',    'hub': 'HUB-8/C6'},
    {'file': 'hub16-crocs/HUB16_Pillar.md',  'hub': 'HUB-16/Pillar'},
    {'file': 'hub16-crocs/HUB16_C1.md',      'hub': 'HUB-16/C1'},
    {'file': 'hub16-crocs/HUB16_C2.md',      'hub': 'HUB-16/C2'},
    {'file': 'hub16-crocs/HUB16_C3.md',      'hub': 'HUB-16/C3'},
]


def parse_frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    if not m:
        raise ValueError('No frontmatter found')
    fm = {}
    for line in m.group(1).splitlines():
        if ': ' in line:
            k, v = line.split(': ', 1)
            fm[k.strip()] = v.strip()
    return fm, m.group(2).strip()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f'=== PHASE 3 — RENDER + QA [{len(BATCH_2)} articles] ===\n')

    all_pass = True
    results = []

    for i, item in enumerate(BATCH_2, 1):
        filepath = BASE_DIR / item['file']
        hub = item['hub']
        print(f'[{i}/{len(BATCH_2)}] {hub} — {filepath.name}')

        if not filepath.exists():
            print(f'  MISSING: {filepath}')
            results.append({'hub': hub, 'status': 'MISSING'})
            all_pass = False
            continue

        text = filepath.read_text(encoding='utf-8')
        fm, body_md = parse_frontmatter(text)

        source_has_json = '```json' in body_md

        html = convert(fm, body_md)

        out_name = filepath.stem + '.html'
        out_path = OUT_DIR / out_name
        out_path.write_text(html, encoding='utf-8')

        checks = qa_checks(html, source_had_json_ld=source_has_json)
        fails = [(name, detail) for name, passed, detail in checks if not passed]

        status = 'PASS' if not fails else 'FAIL'
        icon = '[PASS]' if not fails else '[FAIL]'
        print(f'  {icon} {len(checks) - len(fails)}/{len(checks)} checks  |  {len(html):,} chars')
        print(f'  saved -> {out_path.name}')

        if fails:
            all_pass = False
            for name, detail in fails:
                extra = f' ({detail})' if detail else ''
                print(f'    FAIL: {name}{extra}')

        results.append({'hub': hub, 'status': status, 'fails': fails, 'path': out_path})
        print()

    print('=== PHASE 3 SUMMARY ===')
    for r in results:
        s = r['status']
        print(f'  [{s}] {r["hub"]}')
        if r.get('fails'):
            for name, detail in r['fails']:
                print(f'        FAIL: {name}')

    if all_pass:
        print(f'\nAll {len(BATCH_2)}/6 articles PASS QA.')
        print('NEXT: run phase4_republish_batch2.py')
    else:
        print('\nQA FAILED — do NOT proceed to Phase 4.')
        sys.exit(1)


if __name__ == '__main__':
    main()
