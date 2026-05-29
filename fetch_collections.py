"""Fetch smart + custom collection handles to map desktop nav links"""
import requests, os, sys
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
H = {'X-Shopify-Access-Token': token}

smart = requests.get(f'https://{SHOP_URL}/admin/api/2024-10/smart_collections.json', headers=H, params={'limit': 250}).json()['smart_collections']
custom = requests.get(f'https://{SHOP_URL}/admin/api/2024-10/custom_collections.json', headers=H, params={'limit': 250}).json()['custom_collections']

print('=== SMART COLLECTIONS ===')
for c in sorted(smart, key=lambda x: x['title']):
    print(f'  /collections/{c["handle"]}  —  {c["title"]}')

print('\n=== CUSTOM COLLECTIONS ===')
for c in sorted(custom, key=lambda x: x['title']):
    print(f'  /collections/{c["handle"]}  —  {c["title"]}')
