# -*- coding: utf-8 -*-
import sys, os, csv, requests
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv(r'C:\Projects\baby-mania-agent\.env')
load_dotenv(r'C:\Users\3024e\Desktop\shopify-token\.env', override=True)

TOKEN = os.environ.get('SHOPIFY_ACCESS_TOKEN','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')
SHOP  = os.environ.get('SHOPIFY_SHOP_URL','a2756c-c0.myshopify.com').replace('https://','').rstrip('/')
BASE  = f'https://{SHOP}/admin/api/2024-10'
H = {'X-Shopify-Access-Token': TOKEN}

print(f"Connecting to {SHOP}...")

# Collections map
all_cols = {}
for ep in ['custom_collections','smart_collections']:
    r = requests.get(f'{BASE}/{ep}.json', headers=H, params={'limit':250,'fields':'id,title'})
    for c in r.json().get(ep,[]):
        all_cols[c['id']] = c['title']
print(f"Collections loaded: {len(all_cols)}")

# Collects (product->collection)
product_cols = {}
r = requests.get(f'{BASE}/collects.json', headers=H, params={'limit':250})
while True:
    data = r.json().get('collects',[])
    for c in data:
        product_cols.setdefault(c['product_id'],[]).append(all_cols.get(c['collection_id'],'?'))
    nxt = r.links.get('next',{}).get('url')
    if not nxt: break
    r = requests.get(nxt, headers=H)
print(f"Collects loaded: {sum(len(v) for v in product_cols.values())}")

# All products
all_p = []
r = requests.get(f'{BASE}/products.json', headers=H,
    params={'limit':250,'fields':'id,handle,title,template_suffix','status':'any'})
while True:
    batch = r.json().get('products',[])
    all_p += batch
    nxt = r.links.get('next',{}).get('url')
    if not nxt: break
    r = requests.get(nxt, headers=H)
print(f"Products loaded: {len(all_p)}")

# Write CSV
out = r'C:\Projects\baby-mania-agent\output\products_template_report.csv'
with open(out,'w',newline='',encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['handle','title','template_suffix','collections'])
    for p in sorted(all_p, key=lambda x: (x.get('template_suffix') or '')):
        w.writerow([
            p['handle'],
            p['title'],
            p.get('template_suffix') or '',
            ' | '.join(product_cols.get(p['id'],['—']))
        ])
print(f"Saved: {out}")
