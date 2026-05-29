"""
BabyMania — Crop 7 menu images from grid + upload to Shopify Files API
"""
import sys, os, math, base64, requests, time
sys.stdout.reconfigure(encoding='utf-8')

try:
    from PIL import Image
except ImportError:
    os.system('pip install Pillow -q')
    from PIL import Image

SRC = r'C:\Users\3024e\Downloads\ChatGPT Image May 28, 2026, 07_46_03 PM.png'
OUT = r'C:\Projects\baby-mania-agent\output\menu-images'
os.makedirs(OUT, exist_ok=True)

# ── Open source image ─────────────────────────────────────────────────────────
img = Image.open(SRC).convert('RGBA')
W, H = img.size
print(f'Source: {W} x {H} px')

# ── Grid analysis ──────────────────────────────────────────────────────────────
# Top row: 4 cells | Bottom row: 3 cells
# Small outer padding + gap between cells
# Text label is at the bottom of each cell — estimated 14% of cell height

PAD   = int(W * 0.012)   # outer padding (approx)
GAP   = int(W * 0.012)   # gap between cells
LABEL = 0.16             # fraction of cell height to remove (text label)

row1_h = int(H * 0.50)   # top row occupies ~50% height
row2_h = H - row1_h      # bottom row

# Top row: 4 equal columns
col1_w = (W - 2 * PAD - 3 * GAP) // 4

# Bottom row: 3 equal columns
col2_w = (W - 2 * PAD - 2 * GAP) // 3

def cell_crop(x, y, w, h):
    """Return (x0,y0,x1,y1) with label stripped from bottom."""
    photo_h = int(h * (1 - LABEL))
    return (x, y, x + w, y + photo_h)

# ── Cell coordinates ──────────────────────────────────────────────────────────
# Numbers in image (LTR): 1-בנות 2-בנים 3-ריבורן 4-נעליים | 5-שינה 6-מתנות 7-קיץ
cells = {}

# Row 1 (y starts at PAD)
r1y = PAD
for i, name in enumerate(['girls', 'boys', 'reborn', 'shoes']):
    x0 = PAD + i * (col1_w + GAP)
    cells[f'menu-{name}'] = cell_crop(x0, r1y, col1_w, row1_h - PAD)

# Row 2 (y starts at row1_h + GAP)
r2y = row1_h + GAP
for i, name in enumerate(['sleep', 'gifts', 'summer']):
    x0 = PAD + i * (col2_w + GAP)
    cells[f'menu-{name}'] = cell_crop(x0, r2y, col2_w, row2_h - PAD)

# ── Crop + save ───────────────────────────────────────────────────────────────
print('\n=== Cropping ===')
saved_400 = {}
for fname, box in cells.items():
    cropped = img.crop(box).convert('RGB')
    # Save at 400x400
    r400 = cropped.resize((400, 400), Image.LANCZOS)
    path400 = os.path.join(OUT, f'{fname}.png')
    r400.save(path400, 'PNG', optimize=True)
    saved_400[fname] = path400
    # Save at 200x200
    r200 = cropped.resize((200, 200), Image.LANCZOS)
    path200 = os.path.join(OUT, f'{fname}-2x.png')
    r200.save(path200, 'PNG', optimize=True)
    print(f'  ✓ {fname}.png  box={box}')

# ── Shopify upload ────────────────────────────────────────────────────────────
print('\n=== Uploading to Shopify ===')
SHOP_URL = 'a2756c-c0.myshopify.com'
_env = open(r'C:/Users/3024e/Desktop/shopify-token/.env').read().strip().split('=', 1)
_SECRET = _env[1] if len(_env) > 1 else os.environ.get('SHOPIFY_APP_SECRET', '')
resp = requests.post(f'https://{SHOP_URL}/admin/oauth/access_token', data={
    'grant_type': 'client_credentials',
    'client_id': '896f1f2ea1a949303affac3d2c2a0d09',
    'client_secret': _SECRET,
}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
token = resp.json()['access_token']
HJ = {'X-Shopify-Access-Token': token, 'Content-Type': 'application/json'}

# Shopify Files API — GraphQL stagedUploadsCreate + fileCreate
GRAPHQL = f'https://{SHOP_URL}/admin/api/2024-10/graphql.json'

urls = {}

def upload_file(filepath, filename):
    """Stage + upload + create file in Shopify CDN. Returns CDN URL."""
    filesize = os.path.getsize(filepath)

    # Step 1: stagedUploadsCreate
    stage_q = """
    mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets {
          url
          resourceUrl
          parameters { name value }
        }
        userErrors { field message }
      }
    }"""
    stage_vars = {'input': [{
        'filename':  filename,
        'mimeType':  'image/png',
        'resource':  'FILE',
        'fileSize':  str(filesize),
        'httpMethod': 'POST',
    }]}
    r1 = requests.post(GRAPHQL, headers=HJ, json={'query': stage_q, 'variables': stage_vars})
    targets = r1.json()['data']['stagedUploadsCreate']['stagedTargets']
    if not targets:
        print(f'  ✗ stagedUploadsCreate failed: {r1.text[:200]}')
        return None

    target = targets[0]
    upload_url   = target['url']
    resource_url = target['resourceUrl']
    params       = {p['name']: p['value'] for p in target['parameters']}

    # Step 2: POST to staged URL (Google/S3)
    with open(filepath, 'rb') as f:
        files = {'file': (filename, f, 'image/png')}
        r2 = requests.post(upload_url, data=params, files=files)
    if r2.status_code not in (200, 201, 204):
        print(f'  ✗ Stage upload failed {r2.status_code}: {r2.text[:200]}')
        return None

    # Step 3: fileCreate
    create_q = """
    mutation fileCreate($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files {
          ... on MediaImage { image { url } }
          ... on GenericFile { url }
        }
        userErrors { field message }
      }
    }"""
    create_vars = {'files': [{'originalSource': resource_url, 'contentType': 'IMAGE'}]}
    r3 = requests.post(GRAPHQL, headers=HJ, json={'query': create_q, 'variables': create_vars})
    result = r3.json()
    errors = result.get('data', {}).get('fileCreate', {}).get('userErrors', [])
    if errors:
        print(f'  ✗ fileCreate errors: {errors}')
        return None

    # URL may take a moment — return resourceUrl as fallback
    files_out = result.get('data', {}).get('fileCreate', {}).get('files', [])
    cdn_url = None
    for f_obj in files_out:
        cdn_url = f_obj.get('url') or (f_obj.get('image') or {}).get('url')
        if cdn_url:
            break
    return cdn_url or resource_url

for fname, filepath in saved_400.items():
    filename = f'{fname}.png'
    cdn = upload_file(filepath, filename)
    urls[fname] = cdn or 'UPLOAD_FAILED'
    status = '✓' if cdn else '✗'
    print(f'  {status} {filename}')
    time.sleep(0.5)

# ── Report ────────────────────────────────────────────────────────────────────
print('\n=== CDN URLs ===')
for fname, url in urls.items():
    print(f'{fname}.png → {url}')

# Save to file for reference
with open(os.path.join(OUT, 'urls.txt'), 'w', encoding='utf-8') as f:
    for fname, url in urls.items():
        f.write(f'{fname}.png → {url}\n')

print(f'\nSaved to: {OUT}\\urls.txt')
