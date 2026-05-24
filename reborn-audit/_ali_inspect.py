"""Inspect AliExpress page structure to find where spec data lives."""
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent

URL = "https://he.aliexpress.com/item/1005008896313230.html"  # confirmed match

def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 1366, "height": 900},
        )
        page = ctx.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        time.sleep(8)
        for _ in range(12):
            page.evaluate("window.scrollBy(0, 1200)")
            time.sleep(0.4)
        time.sleep(3)
        html = page.content()
        (ROOT / "_inspect_html.html").write_text(html, encoding="utf-8")
        print(f"len={len(html)}")
        # Locate runParams or alike
        for tag in ["window.runParams", "runParams", "__INIT_DATA__",
                    "specification--prop", "attrName", "propertyName",
                    "skuProperty", "skuProperties", "productProperty",
                    "productInfoModule", "componentData",
                    "tradeStandardSkuMappingModule"]:
            pos = html.find(tag)
            print(f"{tag}: first @ {pos}")
        # Find script tag indices
        scripts = re.findall(r'<script[^>]*>[^<]{0,200}', html)
        for i, s in enumerate(scripts[:15]):
            print(f"  script[{i}] start: {s[:150]}")
        # Now look for a JSON blob containing 'specification'
        for m in re.finditer(r'\{[^{}]{0,80}specification[^{}]{0,400}\}', html):
            print("  spec-snippet:", m.group(0)[:400])
        browser.close()


if __name__ == "__main__":
    run()
