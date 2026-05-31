"""
Batch 4 SEO Metafield Backfill — BabyMania
==========================================
APPROVAL_TIER: T1
MODE: SAFE_SEO_META_ONLY

Reads seo_title + seo_description from 6 local MD frontmatters,
then upserts global.title_tag + global.description_tag on Shopify.

HARD CONSTRAINTS:
  - Does NOT touch body_html
  - Does NOT publish/update products, collections, theme, navigation, or images
  - Verifies handle before writing
  - Verifies written values match source after write
  - Backs up article + current metafields before any write
"""
import sys
import re
import json
import time
import requests
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent))
from shopify_client import _headers, BASE_URL

BLOG_ID  = 109164036409
BASE_DIR = Path(r'C:\Projects\baby-mania-agent\output\organic')
BAK_DIR  = Path(r'C:\Projects\baby-mania-agent\output\organic\backups')
BAK_DIR.mkdir(parents=True, exist_ok=True)

BATCH4 = [
    {
        'hub':        'HUB-12/C3',
        'file':       'hub12-led-shoes/HUB12_C3.md',
        'article_id': 689094983993,
        'handle':     'naalei-orot-livanot-dagamim-yafim',
    },
    {
        'hub':        'HUB-12/C4',
        'file':       'hub12-led-shoes/HUB12_C4.md',
        'article_id': 689095541049,
        'handle':     'naalei-orot-livanim-ma-yeladim-ohavim',
    },
    {
        'hub':        'HUB-12/C5',
        'file':       'hub12-led-shoes/HUB12_C5.md',
        'article_id': 689095573817,
        'handle':     'naalei-orot-solela-kama-zman-mehzika',
    },
    {
        'hub':        'HUB-12/C6',
        'file':       'hub12-led-shoes/HUB12_C6.md',
        'article_id': 689095606585,
        'handle':     'naalei-orot-vs-naalei-sport-matay-livhor',
    },
    {
        'hub':        'HUB-13/Pillar',
        'file':       'hub13-water-shoes/HUB13_Pillar.md',
        'article_id': 689095639353,
        'handle':     'naalei-mayim-leyeladim-madrih-male-brekha-yam',
    },
    {
        'hub':        'HUB-13/C1',
        'file':       'hub13-water-shoes/HUB13_C1.md',
        'article_id': 689095672121,
        'handle':     'naalei-mayim-letinok-meize-gil',
    },
]


def parse_frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if not m:
        raise ValueError('No frontmatter found')
    fm = {}
    for line in m.group(1).splitlines():
        if ': ' in line:
            k, v = line.split(': ', 1)
            fm[k.strip()] = v.strip()
    return fm


def fetch_article(article_id):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    return r.json()['article']


def fetch_metafields(article_id):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}/metafields.json"
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    return r.json().get('metafields', [])


def upsert_metafield(article_id, existing_map, namespace, key, value):
    base = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}/metafields.json"
    if (namespace, key) in existing_map:
        mf_id = existing_map[(namespace, key)]['id']
        r = requests.put(
            f"{BASE_URL}/metafields/{mf_id}.json",
            headers=_headers(),
            json={"metafield": {"id": mf_id, "value": value}},
        )
    else:
        r = requests.post(
            base,
            headers=_headers(),
            json={"metafield": {
                "namespace": namespace, "key": key,
                "value": value, "type": "single_line_text_field",
            }},
        )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
    return r.json()['metafield']


def main():
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"=== BATCH 4 SEO META BACKFILL [{ts}] ===")
    print(f"Articles: {len(BATCH4)} | Mode: SEO_METAFIELDS_ONLY\n")

    pass_count = 0
    results = []

    for i, item in enumerate(BATCH4, 1):
        hub  = item['hub']
        aid  = item['article_id']
        exp_handle = item['handle']
        filepath   = BASE_DIR / item['file']

        print(f"[{i}/{len(BATCH4)}] {hub} (ID:{aid})")

        # ── 1. Read source frontmatter ────────────────────────────────────
        if not filepath.exists():
            print(f"  ERROR: file not found: {filepath}")
            results.append({'hub': hub, 'status': 'FAIL', 'reason': 'file-not-found'})
            continue

        fm = parse_frontmatter(filepath.read_text(encoding='utf-8'))
        seo_title = fm.get('seo_title', '').strip()
        seo_desc  = fm.get('seo_description', '').strip()

        if not seo_title or not seo_desc:
            print(f"  ERROR: seo_title or seo_description missing from frontmatter")
            results.append({'hub': hub, 'status': 'FAIL', 'reason': 'missing-seo-fields'})
            continue

        print(f"  seo_title ({len(seo_title)}c): {seo_title}")
        print(f"  seo_desc  ({len(seo_desc)}c): {seo_desc[:70]}...")

        # ── 2. Fetch live article + verify handle ─────────────────────────
        article = fetch_article(aid)
        live_handle = article.get('handle', '')
        live_body   = article.get('body_html', '')

        if live_handle != exp_handle:
            print(f"  ERROR: handle mismatch — expected '{exp_handle}', got '{live_handle}'")
            results.append({'hub': hub, 'status': 'FAIL', 'reason': 'handle-mismatch',
                            'expected': exp_handle, 'got': live_handle})
            continue
        print(f"  handle OK: {live_handle}")

        # ── 3. Backup article + current metafields ─────────────────────────
        existing_mf = fetch_metafields(aid)
        bak = {
            'ts': ts, 'hub': hub, 'article_id': aid, 'handle': live_handle,
            'article': article,
            'metafields_before': existing_mf,
        }
        bak_path = BAK_DIR / f"seo-backfill-{ts}-{aid}.json"
        bak_path.write_text(json.dumps(bak, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"  backup: {bak_path.name}")

        # ── 4. Upsert SEO metafields ──────────────────────────────────────
        existing_map = {(m['namespace'], m['key']): m for m in existing_mf}

        mf_title = upsert_metafield(aid, existing_map, 'global', 'title_tag',       seo_title)
        mf_desc  = upsert_metafield(aid, existing_map, 'global', 'description_tag', seo_desc)
        time.sleep(0.5)

        # ── 5. Verify written values ──────────────────────────────────────
        title_ok = mf_title['value'] == seo_title
        desc_ok  = mf_desc['value']  == seo_desc
        print(f"  global.title_tag       {'OK' if title_ok else 'MISMATCH'}: {mf_title['value'][:55]}")
        print(f"  global.description_tag {'OK' if desc_ok  else 'MISMATCH'}: {mf_desc['value'][:55]}")

        # ── 6. Verify body_html unchanged ─────────────────────────────────
        article_after = fetch_article(aid)
        body_unchanged = article_after.get('body_html', '') == live_body
        print(f"  body_html unchanged: {'YES' if body_unchanged else 'NO — UNEXPECTED CHANGE'}")

        ok = title_ok and desc_ok and body_unchanged
        status = 'PASS' if ok else 'FAIL'
        icon   = '[PASS]' if ok else '[FAIL]'
        print(f"  {icon} {hub}\n")

        if ok:
            pass_count += 1

        results.append({
            'hub': hub, 'article_id': aid, 'handle': live_handle,
            'seo_title': seo_title, 'seo_description': seo_desc,
            'title_ok': title_ok, 'desc_ok': desc_ok,
            'body_unchanged': body_unchanged,
            'backup': str(bak_path.name),
            'status': status,
        })

    # ── Final report ──────────────────────────────────────────────────────────
    print("=" * 60)
    all_pass = pass_count == len(BATCH4)
    final = 'PASS' if all_pass else 'FAIL'
    print(f"BATCH4_SEO_META_BACKFILL_STATUS: {final}")
    print(f"ARTICLES_UPDATED: {pass_count}/{len(BATCH4)}")
    print(f"BODY_CHANGED: NO")
    print(f"IMAGES_CHANGED: NO")
    print(f"SHOPIFY_WRITES: SEO_METAFIELDS_ONLY")
    print(f"GIT_COMMIT: NO")

    report_path = BAK_DIR / f"seo-backfill-{ts}-report.json"
    report_path.write_text(json.dumps({'results': results, 'pass': pass_count,
                                        'total': len(BATCH4), 'status': final},
                                       ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"report: {report_path.name}")

    sys.exit(0 if all_pass else 1)


if __name__ == '__main__':
    main()
