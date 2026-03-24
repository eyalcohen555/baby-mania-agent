import requests,os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(r"C:/Users/3024e/Desktop/shopify-token/.env"))
T=os.getenv("SHOPIFY_ACCESS_TOKEN")
H={"X-Shopify-Access-Token":T}
for s in ["shoes","clothing","accessories","clothing-test"]:
 r=requests.get(f"https://a2756c-c0.myshopify.com/admin/api/2024-10/products/count.json",headers=H,params={"template_suffix":s})
 print(f"{s}: {r.json()}")
