"""
CANONICAL organic article publish script — BabyMania.
Replaces deprecated scripts/publish_batch1.py and scripts/publish_batch2.py.

REQUIRED pipeline:
  1. bm_html_converter.py — converts Markdown to BabyMania HTML structure
  2. Local QA (13 checks) — must ALL pass before any Shopify write
  3. Deep live verify (14 checks) — after publish

HARD BLOCKS (script exits 1 before Shopify write if any article fails):
  - Missing: intro-box, article-body, faq/details, cta-banner, article-tags
  - Present:  ```json  <pre><code>  [IMG_ALT_  alt-placeholder

Usage:
  python scripts/organic/publish_organic_batch.py --batch BATCH_FILE.json
  python scripts/organic/publish_organic_batch.py --batch BATCH_FILE.json --live

Batch JSON format:
  {
    "name": "batch3",
    "articles": [
      {
        "file": "hub16-crocs/HUB16_C4.md",
        "hub":  "HUB-16/C4",
        "article_id": null        <- null = new article, integer = update existing
      }, ...
    ]
  }
"""

import sys
import re
import json
import time
import argparse
import requests
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Hard import — if this fails, the whole script fails loudly
from scripts.organic.bm_html_converter import convert, qa_checks, validate_product_handles
from shopify_client import _headers, BASE_URL

BLOG_ID   = 109164036409
BASE_DIR  = Path(r'C:\Projects\baby-mania-agent\output\organic')
OUT_BASE  = Path(r'C:\Projects\baby-mania-agent\output\organic\rendered')
BAK_DIR   = Path(r'C:\Projects\baby-mania-agent\output\organic\backups')

SEO_TITLE_MIN = 30
SEO_TITLE_MAX = 65
SEO_DESC_MIN  = 100
SEO_DESC_MAX  = 165


# ── SEO meta gate ─────────────────────────────────────────────────────────────

def validate_seo_meta(fm):
    """Validate seo_title and seo_description in frontmatter.
    Returns list of (name, passed, detail). Hard-fails on missing or out-of-range."""
    checks = []
    seo_title = fm.get('seo_title', '').strip()
    seo_desc  = fm.get('seo_description', '').strip()
    keyword   = fm.get('keyword_main', '').strip()

    checks.append(('seo-title-present', bool(seo_title),
                   '' if seo_title else 'seo_title missing from frontmatter'))
    checks.append(('seo-desc-present', bool(seo_desc),
                   '' if seo_desc else 'seo_description missing from frontmatter'))

    if seo_title:
        tlen = len(seo_title)
        checks.append(('seo-title-length',
                        SEO_TITLE_MIN <= tlen <= SEO_TITLE_MAX,
                        f'{tlen} chars (need {SEO_TITLE_MIN}–{SEO_TITLE_MAX})'))
        if keyword:
            kw_ok = keyword.lower() in seo_title.lower()
            checks.append(('seo-title-has-keyword', kw_ok,
                            '' if kw_ok else f'keyword "{keyword}" not found in seo_title'))

    if seo_desc:
        dlen = len(seo_desc)
        checks.append(('seo-desc-length',
                        SEO_DESC_MIN <= dlen <= SEO_DESC_MAX,
                        f'{dlen} chars (need {SEO_DESC_MIN}–{SEO_DESC_MAX})'))

    return checks


# ── Frontmatter ───────────────────────────────────────────────────────────────

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


# ── Shopify helpers ───────────────────────────────────────────────────────────

def article_exists(handle):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json?handle={handle}&limit=1"
    r   = requests.get(url, headers=_headers())
    if r.status_code == 200:
        arts = r.json().get('articles', [])
        return len(arts) > 0 and arts[0].get('handle') == handle
    return False


def create_article(title, handle, body_html, tags):
    url     = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json"
    payload = {"article": {
        "title": title, "handle": handle, "body_html": body_html,
        "published": True, "tags": tags,
    }}
    r = requests.post(url, headers=_headers(), json=payload)
    r.raise_for_status()
    return r.json()['article']


def update_article(article_id, body_html):
    url     = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    payload = {"article": {"id": article_id, "body_html": body_html}}
    r = requests.put(url, headers=_headers(), json=payload)
    r.raise_for_status()
    return r.json()['article']


def fetch_article_by_id(article_id):
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json"
    r   = requests.get(url, headers=_headers())
    r.raise_for_status()
    return r.json()['article']


def upsert_seo_metafields(article_id, seo_title, seo_description):
    """Upsert global.title_tag and global.description_tag for an article.
    Returns list of (namespace, key, saved_value, match_ok)."""
    base = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}/metafields.json"
    r = requests.get(base, headers=_headers())
    r.raise_for_status()
    existing = {(m['namespace'], m['key']): m for m in r.json().get('metafields', [])}

    results = []
    for ns, key, value in [
        ('global', 'title_tag',       seo_title),
        ('global', 'description_tag', seo_description),
    ]:
        if (ns, key) in existing:
            mf_id = existing[(ns, key)]['id']
            r2 = requests.put(f"{BASE_URL}/metafields/{mf_id}.json",
                              headers=_headers(),
                              json={"metafield": {"id": mf_id, "value": value}})
        else:
            r2 = requests.post(base, headers=_headers(),
                               json={"metafield": {"namespace": ns, "key": key,
                                                   "value": value,
                                                   "type": "single_line_text_field"}})
        r2.raise_for_status()
        saved = r2.json()['metafield']['value']
        results.append((ns, key, saved, saved == value))
    return results


def fetch_seo_metafields(article_id):
    """Fetch global.title_tag and global.description_tag for an article.
    Returns dict {key: value} for the two SEO fields."""
    url = f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}/metafields.json"
    r   = requests.get(url, headers=_headers())
    r.raise_for_status()
    out = {}
    for m in r.json().get('metafields', []):
        if m['namespace'] == 'global' and m['key'] in ('title_tag', 'description_tag'):
            out[m['key']] = m['value']
    return out


# ── Phase: local render + QA ──────────────────────────────────────────────────

def phase_render_qa(articles, out_dir, batch_name):
    out_dir.mkdir(parents=True, exist_ok=True)
    results  = []
    all_pass = True

    for i, item in enumerate(articles, 1):
        filepath = BASE_DIR / item['file']
        hub      = item['hub']
        print(f'  [{i}/{len(articles)}] {hub} — {filepath.name}')

        if not filepath.exists():
            print(f'    MISSING: {filepath}')
            results.append({'hub': hub, 'status': 'MISSING', 'fails': [('file-not-found', '')]})
            all_pass = False
            continue

        text = filepath.read_text(encoding='utf-8')
        fm, body_md = parse_frontmatter(text)
        source_has_json = '```json' in body_md or '<script type="application/ld+json">' in body_md

        # ── SEO meta hard gate ───────────────────────────────────────────
        seo_checks = validate_seo_meta(fm)
        seo_fails  = [(n, d) for n, p, d in seo_checks if not p]
        seo_title  = fm.get('seo_title', '').strip()
        seo_desc   = fm.get('seo_description', '').strip()

        def _seo_status(key):
            present = bool(fm.get(key, '').strip())
            if not present:
                return 'MISSING'
            fail_names = [n for n, p, d in seo_checks if not p and key.replace('_', '-') in n]
            return 'INVALID' if fail_names else 'PASS'

        print(f'    SEO_TITLE: {_seo_status("seo_title")}'
              + (f' — {seo_title[:55]}' if seo_title else ''))
        print(f'    SEO_DESC:  {_seo_status("seo_description")}'
              + (f' — {seo_desc[:55]}' if seo_desc else ''))
        for n, d in seo_fails:
            print(f'      SEO-BLOCK: {n} {d}')

        html   = convert(fm, body_md)
        checks = qa_checks(html, source_had_json_ld=source_has_json)

        # ── Product handle hard gate ─────────────────────────────────────
        link_failures = validate_product_handles(html)
        if link_failures:
            print(f'    [PRODUCT-LINK-GATE] {len(link_failures)} broken handle(s):')
            for lf in link_failures:
                sc = lf.get('status_code', 'n/a')
                print(f'      → {lf["url"]}  [{lf["reason"]} / HTTP {sc}]')
        for lf in link_failures:
            chk_name   = f'product-link-{lf["reason"].lower().replace("_", "-")}'
            chk_detail = f'{lf["url"]} [{lf["reason"]}]'
            checks.append((chk_name, False, chk_detail))

        fails  = seo_fails + [(n, d) for n, p, d in checks if not p]

        slug  = fm.get('slug', filepath.stem)
        title = fm.get('title', '?')
        hub_tag = fm.get('hub', '').lower().replace('-', '')
        tags = f"organic,{hub_tag},{batch_name}"

        out_path = out_dir / (filepath.stem + '.html')
        out_path.write_text(html, encoding='utf-8')

        qa_path = out_dir / (filepath.stem + '_qa.json')
        qa_path.write_text(json.dumps({
            'hub': hub, 'slug': slug, 'status': 'PASS' if not fails else 'FAIL',
            'html_len': len(html),
            'checks': [{'name': n, 'pass': p, 'detail': d} for n, p, d in checks],
        }, ensure_ascii=False, indent=2), encoding='utf-8')

        status = 'PASS' if not fails else 'FAIL'
        icon   = '[PASS]' if not fails else '[FAIL]'
        passed = len(checks) - len(fails)
        print(f'    {icon} {passed}/{len(checks)} checks | {len(html):,} chars | {slug}')
        if fails:
            all_pass = False
            for n, d in fails:
                extra = f' ({d})' if d else ''
                print(f'      BLOCK: {n}{extra}')

        results.append({
            'hub': hub, 'slug': slug, 'title': title, 'tags': tags,
            'html': html, 'html_path': out_path,
            'article_id': item.get('article_id'),
            'seo_title': seo_title, 'seo_description': seo_desc,
            'status': status, 'fails': fails,
        })

    return results, all_pass


# ── Phase: live publish ────────────────────────────────────────────────────────

def phase_publish(results):
    published = []
    for i, r in enumerate(results, 1):
        hub  = r['hub']
        slug = r['slug']
        aid  = r.get('article_id')
        html = r['html']
        print(f'  [{i}/{len(results)}] {hub} — {slug}')

        if aid:
            article  = update_article(aid, html)
            action   = 'UPDATED'
        else:
            if article_exists(slug):
                print(f'    SKIP — already exists on Shopify')
                # Fetch existing ID so we can verify later
                url = f"{BASE_URL}/blogs/{BLOG_ID}/articles.json?handle={slug}&limit=1"
                a   = requests.get(url, headers=_headers()).json()['articles'][0]
                published.append({**r, 'article_id': a['id'], 'handle': a['handle'],
                                  'action': 'ALREADY_EXISTS'})
                print()
                continue
            article = create_article(r['title'], slug, html, r['tags'])
            action  = 'CREATED'

        live_url = f"https://babymania-il.com/blogs/news/{article['handle']}"
        print(f'    {action} — ID:{article["id"]} — {live_url}')

        # ── SEO metafields upsert ─────────────────────────────────────────
        art_id    = article['id']
        seo_t     = r.get('seo_title', '')
        seo_d     = r.get('seo_description', '')
        if seo_t and seo_d:
            mf_results = upsert_seo_metafields(art_id, seo_t, seo_d)
            for ns, key, saved, ok in mf_results:
                icon2 = 'OK' if ok else 'MISMATCH'
                print(f'    SEO [{icon2}] {ns}.{key} = {saved[:55]}')

        published.append({**r, 'article_id': art_id,
                          'handle': article['handle'], 'action': action,
                          'url': live_url})
        if i < len(results):
            print('    pause 3s...')
            time.sleep(3)
        print()

    return published


# ── Phase: deep live verify ────────────────────────────────────────────────────

def phase_verify(published):
    all_pass = True
    for item in published:
        aid  = item['article_id']
        hub  = item['hub']
        slug = item['slug']
        local_len = len(item['html'])

        article   = fetch_article_by_id(aid)
        live_html = article.get('body_html', '')
        live_len  = len(live_html)
        pub_at    = article.get('published_at')
        handle    = article.get('handle', '')
        live_url  = f"https://babymania-il.com/blogs/news/{handle}"

        len_ratio = live_len / local_len if local_len else 0
        len_ok    = 0.90 <= len_ratio <= 1.10

        checks = qa_checks(live_html, source_had_json_ld=True)

        # ── SEO metafield live verify ─────────────────────────────────────
        seo_t  = item.get('seo_title', '')
        seo_d  = item.get('seo_description', '')
        seo_live = fetch_seo_metafields(aid)
        seo_title_ok = bool(seo_t) and seo_live.get('title_tag') == seo_t
        seo_desc_ok  = bool(seo_d) and seo_live.get('description_tag') == seo_d

        extra  = [
            ('is-published',       pub_at is not None, ''),
            ('slug-unchanged',     handle == slug,     ''),
            ('length-match-local', len_ok,
             f'live={live_len:,} local={local_len:,} ratio={len_ratio:.2f}'),
            ('seo-title-tag-live', seo_title_ok,
             '' if seo_title_ok else f'expected: {seo_t[:50]}  got: {seo_live.get("title_tag","MISSING")[:50]}'),
            ('seo-desc-tag-live',  seo_desc_ok,
             '' if seo_desc_ok  else f'expected: {seo_d[:50]}  got: {seo_live.get("description_tag","MISSING")[:50]}'),
        ]
        all_checks = extra + [(n, p, d) for n, p, d in checks]
        fails = [(n, d) for n, p, d in all_checks if not p]
        passed = len(all_checks) - len(fails)
        status = 'PASS' if not fails else 'FAIL'
        icon   = '[PASS]' if not fails else '[FAIL]'

        print(f'  {icon} {hub} {passed}/{len(all_checks)} — {live_url}')
        if fails:
            all_pass = False
            for n, d in fails:
                extra_str = f' ({d})' if d else ''
                print(f'      FAIL: {n}{extra_str}')
        item['verify_status'] = status
        item['verify_fails']  = fails

    return all_pass


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Publish BabyMania organic articles (canonical)')
    parser.add_argument('--batch',    required=True, help='Path to batch JSON file')
    parser.add_argument('--live',     action='store_true', help='Write to Shopify')
    parser.add_argument('--dry-run',  action='store_true', default=True)
    args  = parser.parse_args()
    live  = args.live
    mode  = 'LIVE' if live else 'DRY-RUN'

    batch_path = Path(args.batch)
    if not batch_path.exists():
        print(f'ERROR: batch file not found: {batch_path}')
        sys.exit(1)

    batch      = json.loads(batch_path.read_text(encoding='utf-8'))
    batch_name = batch.get('name', batch_path.stem)
    articles   = batch['articles']
    out_dir    = OUT_BASE / batch_name

    print(f'=== PUBLISH ORGANIC BATCH [{batch_name}] [{mode}] — {len(articles)} articles ===')
    print(f'Using: bm_html_converter.py (mandatory)')
    if not live:
        print('DRY-RUN: local render + QA only. Add --live to publish.\n')
    else:
        print()

    # ── Phase 1: render + QA ────────────────────────────────────────────────
    print('--- RENDER + QA ---')
    results, qa_ok = phase_render_qa(articles, out_dir, batch_name)
    print()

    if not qa_ok:
        print('=== BLOCKED: QA FAILED — no Shopify writes performed ===')
        fails_count = sum(1 for r in results if r['status'] != 'PASS')
        print(f'{fails_count}/{len(articles)} articles have QA failures.')
        print('Fix source .md files and re-run.')
        sys.exit(1)

    passes = sum(1 for r in results if r['status'] == 'PASS')
    print(f'QA: {passes}/{len(articles)} PASS')

    if not live:
        print(f'\n=== DRY-RUN COMPLETE — {passes}/{len(articles)} ready ===')
        print('Run with --live after Ayal approval.')
        return

    # ── Phase 2: backup existing IDs before any writes ──────────────────────
    BAK_DIR.mkdir(parents=True, exist_ok=True)
    existing_ids = [r['article_id'] for r in results if r.get('article_id')]
    if existing_ids:
        ts    = datetime.now().strftime('%Y%m%d-%H%M%S')
        bak   = BAK_DIR / f'{batch_name}-before-publish-{ts}.json'
        backs = []
        for aid in existing_ids:
            try:
                backs.append(fetch_article_by_id(aid))
            except Exception as e:
                print(f'  WARNING: could not backup ID:{aid} — {e}')
        bak.write_text(json.dumps(backs, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'Backup: {bak}\n')

    # ── Phase 3: publish ─────────────────────────────────────────────────────
    print('--- PUBLISH ---')
    published = phase_publish(results)

    # ── Phase 4: deep live verify ────────────────────────────────────────────
    print('--- DEEP LIVE VERIFY ---')
    verify_ok = phase_verify(published)
    print()

    # ── Summary ──────────────────────────────────────────────────────────────
    print(f'=== BATCH [{batch_name}] SUMMARY ===')
    for item in published:
        action = item.get('action', '?')
        vst    = item.get('verify_status', '?')
        icon   = 'OK' if vst == 'PASS' else 'FAIL'
        print(f'  [{icon}] {item["hub"]} — {item["slug"]} [{action}] [{vst}]')
        if item.get('url'):
            print(f'       {item["url"]}')

    ok_count = sum(1 for p in published if p.get('verify_status') == 'PASS')
    print(f'\nPublished + verified: {ok_count}/{len(published)}')

    if not verify_ok:
        print('VERIFY FAILED — investigate.')
        sys.exit(1)
    else:
        print('NEXT STEP: submit GSC indexing for each published URL')


if __name__ == '__main__':
    main()
