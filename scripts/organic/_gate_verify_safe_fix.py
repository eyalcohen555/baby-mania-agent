"""
Gate verify after safe handle fix — READ ONLY.
Runs validate_product_handles on all 14 affected source articles.
Reports: which handles now pass, which still fail.
NO writes to Shopify, no publish, no commit.
"""
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.organic.bm_html_converter import convert, qa_checks, validate_product_handles

BASE_DIR = Path(r'C:\Projects\baby-mania-agent\output\organic')

ARTICLES = [
    # babysleep-pro fixed (3)
    {'file': 'hub1-extension/HUB1_C5.md',  'hub': 'HUB-1/C5'},
    {'file': 'hub1-extension/HUB1_C6.md',  'hub': 'HUB-1/C6'},
    {'file': 'hub8-extension/HUB8_C6.md',  'hub': 'HUB-8/C6'},
    # toddler-baby-boys-clothes fixed (1)
    {'file': 'hub2-extension/HUB2_C6.md',  'hub': 'HUB-2/C6'},
    # childrens-sandals fixed (9)
    {'file': 'hub16-crocs/HUB16_Pillar.md','hub': 'HUB-16/Pillar'},
    {'file': 'hub16-crocs/HUB16_C1.md',    'hub': 'HUB-16/C1'},
    {'file': 'hub16-crocs/HUB16_C2.md',    'hub': 'HUB-16/C2'},
    {'file': 'hub16-crocs/HUB16_C3.md',    'hub': 'HUB-16/C3'},
    {'file': 'hub16-crocs/HUB16_C4.md',    'hub': 'HUB-16/C4'},
    {'file': 'hub16-crocs/HUB16_C5.md',    'hub': 'HUB-16/C5'},
    {'file': 'hub16-crocs/HUB16_C6.md',    'hub': 'HUB-16/C6'},
    {'file': 'hub13-water-shoes/HUB13_C2.md','hub': 'HUB-13/C2'},
    {'file': 'hub13-water-shoes/HUB13_Pillar.md','hub': 'HUB-13/Pillar'},
    # decision-required — should still fail
    {'file': 'hub13-water-shoes/HUB13_C4.md',  'hub': 'HUB-13/C4'},
    {'file': 'hub13-water-shoes/HUB13_C5.md',  'hub': 'HUB-13/C5'},
    {'file': 'hub13-water-shoes/HUB13_C6.md',  'hub': 'HUB-13/C6'},
    {'file': 'hub13-water-shoes/HUB13_C1.md',  'hub': 'HUB-13/C1'},
    {'file': 'hub13-water-shoes/HUB13_C3.md',  'hub': 'HUB-13/C3'},
    {'file': 'hub16-crocs/HUB16_C6.md',        'hub': 'HUB-16/C6 (re-check)'},
]

# Remove duplicate HUB-16/C6 entry
seen = set()
ARTICLES_DEDUP = []
for a in ARTICLES:
    if a['file'] not in seen:
        seen.add(a['file'])
        ARTICLES_DEDUP.append(a)


def parse_frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ': ' in line:
            k, v = line.split(': ', 1)
            fm[k.strip()] = v.strip()
    return fm, m.group(2).strip()


def main():
    print('=== GATE VERIFY AFTER SAFE HANDLE FIX (READ ONLY) ===\n')
    print(f'Checking {len(ARTICLES_DEDUP)} source files...\n')

    safe_pass  = []
    still_fail = []
    gate_ok    = True

    for item in ARTICLES_DEDUP:
        filepath = BASE_DIR / item['file']
        hub = item['hub']

        if not filepath.exists():
            print(f'[MISSING] {hub} — {filepath}')
            continue

        text = filepath.read_text(encoding='utf-8')
        fm, body_md = parse_frontmatter(text)
        html = convert(fm, body_md)

        failures = validate_product_handles(html)
        # Also check that fixed handles are not present in failure list
        fixed_broken = {
            'babysleep-pro',
            'toddler-baby-boys-clothes',
            'childrens-sandals-summer-casual-eva-lightweight-outdoor-handmade-diy-baby-shoes-anti-slip-',
        }
        gate_failures = [f for f in failures if f.get('handle') not in fixed_broken or True]
        # All failures count as gate failures
        gate_failures = failures

        if not gate_failures:
            icon = '[PASS]'
            safe_pass.append(hub)
        else:
            icon = '[FAIL]'
            still_fail.append({'hub': hub, 'failures': gate_failures})
            # Check if any are the safe-fixed handles (regression detection)
            for f in gate_failures:
                h = f.get('handle', '')
                if h in fixed_broken or h.rstrip('-') in {b.rstrip('-') for b in fixed_broken}:
                    print(f'  !! REGRESSION: {h} should be fixed but still failing')
                    gate_ok = False

        print(f'{icon} {hub}')
        for f in gate_failures:
            reason = f.get('reason', '?')
            handle = f.get('handle', '?')
            sc = f.get('status_code', 'n/a')
            print(f'     BLOCKED: {handle[:70]} [{reason} / HTTP {sc}]')

    print(f'\n=== SUMMARY ===')
    print(f'PASS: {len(safe_pass)}/{len(ARTICLES_DEDUP)} articles clean')
    print(f'FAIL: {len(still_fail)}/{len(ARTICLES_DEDUP)} articles still blocked')

    if still_fail:
        print('\nBlocked handles remaining:')
        seen_handles = set()
        for r in still_fail:
            for f in r['failures']:
                h = f.get('handle', '?')
                if h not in seen_handles:
                    seen_handles.add(h)
                    reason = f.get('reason', '?')
                    print(f'  - {h[:80]} [{reason}]')

    if not gate_ok:
        print('\nREGRESSION DETECTED — a fixed handle is still failing!')
        sys.exit(1)
    else:
        print('\nNo regression in fixed handles.')
        print('NO_SHOPIFY_WRITES: confirmed (read-only run)')
        print('NO_PUBLISH: confirmed')
        print('NO_COMMIT: confirmed')


if __name__ == '__main__':
    main()
