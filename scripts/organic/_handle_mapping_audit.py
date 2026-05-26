"""
Handle mapping audit — READ ONLY.
Phase 2: find correct Shopify handles for 8 broken handles.
NO writes to any file or Shopify.
"""
import sys
import re
import requests
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
load_dotenv(r'C:\Users\3024e\Desktop\shopify-token\.env')
from shopify_client import _headers, BASE_URL

BLOG_ID = 109164036409

BROKEN_HANDLES = [
    'babysleep-pro',
    'baby-swimsuit',
    'baby-boy-swim-set',
    'baby-beach-essentials',
    'toddler-baby-boys-clothes',
    'childrens-sandals-summer-casual-eva-lightweight-outdoor-handmade-diy-baby-shoes-anti-slip-',
    'boys-sandals-summer-casual-eva-baby-shoes-anti-slip-soft-sole-infant-',
    '1-4t-baby-sandals-mesh-breathable-summer-beach-cartoon-outdoor-anti-slip-soft-sole-',
]

# Known candidate from Agent 10 docs
CANDIDATE_BABYSLEEP = 'baby-white-noise-machine-kids-sleep-sound-player-night-light-timer-noise-player-rechargeable-timed-shutdown-usb-sleep-machine'


def http_check(handle):
    url = f'https://babymania-il.com/products/{handle}'
    try:
        r = requests.get(url, timeout=12, allow_redirects=True,
                         headers={'User-Agent': 'BabyMania-PipelineQA/1.0'})
        return r.status_code, r.url
    except Exception as e:
        return None, str(e)


def fetch_all_products():
    """Paginate all products from Shopify REST."""
    products = []
    url = f'{BASE_URL}/products.json?limit=250&fields=id,title,handle,status'
    while url:
        r = requests.get(url, headers=_headers())
        if r.status_code != 200:
            print(f'  ERROR fetching products: HTTP {r.status_code}')
            break
        page = r.json().get('products', [])
        products.extend(page)
        # Check Link header for next page
        link = r.headers.get('Link', '')
        next_url = None
        for part in link.split(','):
            part = part.strip()
            if 'rel="next"' in part:
                m = re.search(r'<([^>]+)>', part)
                if m:
                    next_url = m.group(1)
        url = next_url
    return products


def search_by_handle(products, fragment):
    """Find products whose handle contains fragment."""
    return [p for p in products if fragment.lower() in p['handle'].lower()]


def search_by_title(products, keywords):
    """Find products whose title contains any keyword (case-insensitive)."""
    results = []
    for p in products:
        t = p['title'].lower()
        if any(kw.lower() in t for kw in keywords):
            results.append(p)
    return results


def main():
    print('=== HANDLE MAPPING AUDIT — PHASE 2 (READ ONLY) ===\n')

    # --- Step 1: Test known babysleep-pro candidate ---
    print('--- STEP 1: Test known babysleep-pro candidate ---')
    code, final_url = http_check(CANDIDATE_BABYSLEEP)
    print(f'  Handle: {CANDIDATE_BABYSLEEP[:60]}...')
    print(f'  HTTP {code} — {final_url[:100]}')
    print()

    # --- Step 2: Test trailing-dash handles without trailing dash ---
    print('--- STEP 2: Trailing-dash handles — strip dash test ---')
    trailing_dash = [h for h in BROKEN_HANDLES if h.endswith('-')]
    for h in trailing_dash:
        stripped = h.rstrip('-')
        code, final_url = http_check(stripped)
        print(f'  [{code}] {stripped[:70]}')
    print()

    # --- Step 3: Fetch all products from Shopify ---
    print('--- STEP 3: Fetch all Shopify products ---')
    products = fetch_all_products()
    print(f'  Total products: {len(products)}')
    print()

    if not products:
        print('  No products found — cannot proceed with mapping.')
        return

    # Show all product handles/titles for reference
    print('  All products:')
    for p in products:
        print(f'    [{p["status"]}] {p["handle"]}')
        print(f'          {p["title"]}')
    print()

    # --- Step 4: Match broken handles to store products ---
    print('--- STEP 4: Match broken handles ---')

    search_map = {
        'babysleep-pro':           (['white noise', 'sleep', 'sound', 'noise machine'], ['noise', 'sleep']),
        'baby-swimsuit':           (['swimsuit', 'swim', 'bathing suit'], ['swim', 'בגד ים']),
        'baby-boy-swim-set':       (['swim set', 'swim', 'boys swim'], ['swim', 'בגד ים']),
        'baby-beach-essentials':   (['beach', 'essentials'], ['beach', 'חוף']),
        'toddler-baby-boys-clothes': (['boys clothes', 'baby clothes', 'toddler'], ['בגדים', 'clothes']),
    }

    for broken_handle, (title_kws, handle_frags) in search_map.items():
        print(f'  Broken: {broken_handle}')
        # Try title keywords
        by_title = search_by_title(products, title_kws)
        # Try handle fragments
        by_handle = []
        for frag in handle_frags:
            by_handle.extend(search_by_handle(products, frag))
        combined = {p['handle']: p for p in by_title + by_handle}.values()
        if combined:
            for p in combined:
                code, _ = http_check(p['handle'])
                print(f'    CANDIDATE [{code}] {p["handle"]}')
                print(f'              "{p["title"]}"')
        else:
            print(f'    NO MATCH FOUND')
        print()

    # --- Step 5: Trailing-dash — find live version ---
    print('--- STEP 5: Trailing-dash handles — find store match ---')
    trailing_keywords = {
        'childrens-sandals-summer-casual-eva-lightweight-outdoor-handmade-diy-baby-shoes-anti-slip-':
            (['sandal', 'סנדל', 'eva', 'childrens'], ['sandal', 'crocs']),
        'boys-sandals-summer-casual-eva-baby-shoes-anti-slip-soft-sole-infant-':
            (['boys sandal', 'sandal', 'סנדל'], ['sandal']),
        '1-4t-baby-sandals-mesh-breathable-summer-beach-cartoon-outdoor-anti-slip-soft-sole-':
            (['baby sandal', 'mesh', 'breathable'], ['sandal', 'mesh']),
    }
    for broken_handle, (title_kws, handle_frags) in trailing_keywords.items():
        print(f'  Broken: {broken_handle[:65]}...')
        by_title = search_by_title(products, title_kws)
        by_handle = []
        for frag in handle_frags:
            by_handle.extend(search_by_handle(products, frag))
        combined = list({p['handle']: p for p in by_title + by_handle}.values())
        if combined:
            for p in combined:
                code, _ = http_check(p['handle'])
                print(f'    CANDIDATE [{code}] {p["handle"]}')
                print(f'              "{p["title"]}"')
        else:
            print(f'    NO MATCH FOUND in store')
        print()

    print('=== AUDIT COMPLETE ===')


if __name__ == '__main__':
    main()
