"""
BabyMania — Create smart collections for nav menu
Creates 17 gender+type intersection collections + renames existing collection
"""
import requests, os, sys, time, json
sys.stdout.reconfigure(encoding='utf-8')

SHOP_URL = 'a2756c-c0.myshopify.com'
_env = open(r'C:/Users/3024e/Desktop/shopify-token/.env').read().strip().split('=', 1)
_SECRET = _env[1] if len(_env) > 1 else os.environ.get('SHOPIFY_APP_SECRET', '')
resp = requests.post(f'https://{SHOP_URL}/admin/oauth/access_token', data={
    'grant_type': 'client_credentials',
    'client_id': '896f1f2ea1a949303affac3d2c2a0d09',
    'client_secret': _SECRET,
}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
token = resp.json()['access_token']
H  = {'X-Shopify-Access-Token': token}
HJ = {**H, 'Content-Type': 'application/json'}

def make_rules(tags):
    """AND logic between all tags"""
    return [{'column': 'tag', 'relation': 'equals', 'condition': t} for t in tags]

# ── Collections to create ─────────────────────────────────────────────────────
TO_CREATE = [
    # Girls subcategories
    {'title': 'בנות — סטים ומארזים',       'handle': 'nav-girl-sets',    'tags': ['gender-girl', 'type-set']},
    {'title': 'בנות — בגדי גוף ואוברולים', 'handle': 'nav-girl-rompers', 'tags': ['gender-girl', 'type-romper']},
    {'title': 'בנות — שמלות וחצאיות',      'handle': 'nav-girl-dress',   'tags': ['gender-girl', 'type-dress']},
    {'title': 'בנות — חולצות וגופיות',     'handle': 'nav-girl-tops',    'tags': ['gender-girl', 'type-top']},
    {'title': 'בנות — מכנסיים וטייצים',    'handle': 'nav-girl-pants',   'tags': ['gender-girl', 'type-pants']},
    {'title': 'בנות — בגדי ים',            'handle': 'nav-girl-swim',    'tags': ['gender-girl', 'type-swim']},
    {'title': 'בנות — פיג׳מות',            'handle': 'nav-girl-pajama',  'tags': ['gender-girl', 'type-pajama']},
    {'title': 'בנות — בגדי חורף',          'handle': 'nav-girl-winter',  'tags': ['gender-girl', 'season-winter']},
    # Boys subcategories
    {'title': 'בנים — סטים ומארזים',       'handle': 'nav-boy-sets',     'tags': ['gender-boy', 'type-set']},
    {'title': 'בנים — בגדי גוף ואוברולים', 'handle': 'nav-boy-rompers',  'tags': ['gender-boy', 'type-romper']},
    {'title': 'בנים — חולצות וגופיות',     'handle': 'nav-boy-tops',     'tags': ['gender-boy', 'type-top']},
    {'title': 'בנים — מכנסיים',            'handle': 'nav-boy-pants',    'tags': ['gender-boy', 'type-pants']},
    {'title': 'בנים — בגדי ים',            'handle': 'nav-boy-swim',     'tags': ['gender-boy', 'type-swim']},
    {'title': 'בנים — פיג׳מות',            'handle': 'nav-boy-pajama',   'tags': ['gender-boy', 'type-pajama']},
    {'title': 'בנים — בגדי חורף',          'handle': 'nav-boy-winter',   'tags': ['gender-boy', 'season-winter']},
    # Shoes
    {'title': 'נעלי בנות',                 'handle': 'nav-shoes-girl',   'tags': ['gender-girl', 'type-shoes']},
    {'title': 'נעלי בנים',                 'handle': 'nav-shoes-boy',    'tags': ['gender-boy',  'type-shoes']},
]

# ── Get existing handles ──────────────────────────────────────────────────────
q = '{ collections(first: 100) { edges { node { id title handle } } } }'
r = requests.post(f'https://{SHOP_URL}/admin/api/2024-10/graphql.json',
    headers=HJ, json={'query': q})
existing = {e['node']['handle']: e['node'] for e in r.json()['data']['collections']['edges']}
print(f'Existing collections: {len(existing)}')

# ── Create missing smart collections ─────────────────────────────────────────
print('\n=== Creating smart collections ===')
created = {}
for col in TO_CREATE:
    handle = col['handle']
    if handle in existing:
        print(f'  SKIP (exists): {col["title"]}')
        created[handle] = existing[handle]['id']
        continue

    payload = {
        'smart_collection': {
            'title':       col['title'],
            'handle':      handle,
            'rules':       make_rules(col['tags']),
            'disjunctive': False,
        }
    }
    r2 = requests.post(
        f'https://{SHOP_URL}/admin/api/2024-10/smart_collections.json',
        headers=H, json=payload
    )
    if r2.status_code in (200, 201):
        sc = r2.json()['smart_collection']
        created[handle] = f'gid://shopify/Collection/{sc["id"]}'
        pc = sc.get('products_count', 0)
        print(f'  CREATED: {col["title"]}  ({pc} products)  id={sc["id"]}')
    else:
        print(f'  ERROR {r2.status_code}: {col["title"]}  → {r2.text[:200]}')
    time.sleep(0.5)

# ── Rename "המיוחדים שלנו" → "שינה טובה לתינוק" ────────────────────────────
print('\n=== Renaming collection ===')
old_handle = 'המיוחדים-שלנו'
if old_handle in existing:
    col_id_gid = existing[old_handle]['id']
    numeric_id = col_id_gid.split('/')[-1]

    # Try smart_collections first, then custom_collections
    renamed = False
    for endpoint in ['smart_collections', 'custom_collections']:
        r3 = requests.put(
            f'https://{SHOP_URL}/admin/api/2024-10/{endpoint}/{numeric_id}.json',
            headers=H,
            json={endpoint[:-1]: {'id': int(numeric_id), 'title': 'שינה טובה לתינוק'}}
        )
        if r3.status_code == 200:
            print(f'  RENAMED via {endpoint}: "המיוחדים שלנו" → "שינה טובה לתינוק"')
            renamed = True
            break
        time.sleep(0.3)
    if not renamed:
        print(f'  ERROR renaming: {r3.status_code} {r3.text[:200]}')
else:
    print(f'  NOT FOUND: {old_handle}')

# ── Summary ───────────────────────────────────────────────────────────────────
print(f'\n=== Done: {len(created)}/{len(TO_CREATE)} collections ready ===')
