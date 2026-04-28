# -*- coding: utf-8 -*-
import sys, os, csv, requests, argparse
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv

# ── CLI args ──────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="BabyMania product report")
parser.add_argument("--category",     default=None,  help="Filter by template_suffix (e.g. shoes)")
parser.add_argument("--sample",       type=int, default=None, help="Limit output to N products")
parser.add_argument("--with-content", action="store_true",    help="Add audit content columns (vendor, type, tags, price, inventory)")
args = parser.parse_args()

# ── Config ────────────────────────────────────────────────────────────────────
load_dotenv(r'C:\Projects\baby-mania-agent\.env')
load_dotenv(r'C:\Users\3024e\Desktop\shopify-token\.env', override=True)

TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOP  = os.environ.get('SHOPIFY_SHOP_URL', 'a2756c-c0.myshopify.com').replace('https://','').rstrip('/')

print(f"Connecting to {SHOP}...")

BASE = f"https://{SHOP}/admin/api/2024-10"
H    = {"X-Shopify-Access-Token": TOKEN}

# ── Collections map ───────────────────────────────────────────────────────────
all_cols = {}
for ep in ['custom_collections', 'smart_collections']:
    r = requests.get(f'{BASE}/{ep}.json', headers=H, params={'limit': 250, 'fields': 'id,title'})
    for c in r.json().get(ep, []):
        all_cols[c['id']] = c['title']

print(f"Collections loaded: {len(all_cols)}")

# ── Collects (product → collection) ──────────────────────────────────────────
product_cols = {}
resp = requests.get(f'{BASE}/collects.json', headers=H, params={'limit': 250})

while True:
    for c in resp.json().get('collects', []):
        product_cols.setdefault(c['product_id'], []).append(
            all_cols.get(c['collection_id'], '?')
        )
    nxt = resp.links.get('next', {}).get('url')
    if not nxt:
        break
    resp = requests.get(nxt, headers=H)

print(f"Collects loaded: {sum(len(v) for v in product_cols.values())}")

# ── Fetch products ────────────────────────────────────────────────────────────
base_fields = 'id,handle,title,template_suffix'
if args.with_content:
    base_fields += ',vendor,product_type,tags,variants,published_at'

all_p = []
r = requests.get(
    f'{BASE}/products.json',
    headers=H,
    params={'limit': 250, 'fields': base_fields, 'status': 'active'}
)

while True:
    all_p += r.json().get('products', [])
    nxt = r.links.get('next', {}).get('url')
    if not nxt:
        break
    r = requests.get(nxt, headers=H)

print(f"Products loaded: {len(all_p)}")

# ── Filter ────────────────────────────────────────────────────────────────────
# Category filter uses template_suffix.
# "shoes" → template_suffix == "shoes"
# No template_suffix (empty string / None) = clothing / other.
if args.category:
    all_p = [p for p in all_p if (p.get('template_suffix') or '') == args.category]
    print(f"After --category '{args.category}' filter: {len(all_p)} products")

# Sort, then sample
all_p = sorted(all_p, key=lambda x: (x.get('template_suffix') or '', x.get('handle', '')))

if args.sample:
    all_p = all_p[:args.sample]
    print(f"After --sample {args.sample}: {len(all_p)} products")

# ── CSV ───────────────────────────────────────────────────────────────────────
out = r'C:\Projects\baby-mania-agent\output\products_template_report.csv'

base_headers   = ['handle', 'title', 'template_suffix', 'collections']
content_headers = ['vendor', 'product_type', 'tags', 'variant_count', 'price', 'inventory', 'published_at']

headers = base_headers + (content_headers if args.with_content else [])

with open(out, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(headers)

    for p in all_p:
        row = [
            p['handle'],
            p['title'],
            p.get('template_suffix') or '',
            ' | '.join(product_cols.get(p['id'], ['—'])),
        ]
        if args.with_content:
            variants = p.get('variants') or []
            first_v  = variants[0] if variants else {}
            row += [
                p.get('vendor') or '',
                p.get('product_type') or '',
                p.get('tags') or '',
                len(variants),
                first_v.get('price') or '',
                first_v.get('inventory_quantity') or '',
                (p.get('published_at') or '')[:10],   # date only
            ]
        w.writerow(row)

print(f"Saved: {out}")

# ── Console summary ───────────────────────────────────────────────────────────
print(f"\n{'─'*60}")
print(f"REPORT SUMMARY")
print(f"  category filter : {args.category or '(all)'}")
print(f"  sample          : {args.sample or '(all)'}")
print(f"  with-content    : {args.with_content}")
print(f"  rows written    : {len(all_p)}")
print(f"  output          : {out}")
if all_p:
    print(f"\nPREVIEW ({min(3, len(all_p))} rows):")
    for p in all_p[:3]:
        suffix = p.get('template_suffix') or '(none)'
        print(f"  [{suffix}] {p['handle']}")
print(f"{'─'*60}")
