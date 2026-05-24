"""Debug what AliExpress is actually returning."""
import time
from pathlib import Path
from urllib.parse import quote_plus

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_ali_debug"
OUT.mkdir(exist_ok=True)


def run():
    q = "BZDoll 55cm 22 inch reborn full silicone"
    urls = [
        f"https://www.aliexpress.com/wholesale-product.html?SearchText={quote_plus(q)}",
        f"https://www.aliexpress.com/w/wholesale-{quote_plus(q)}.html",
        f"https://www.aliexpress.com/wholesale?SearchText={quote_plus(q)}",
        "https://www.aliexpress.com/item/1005005317212200.html",  # known item
    ]
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            viewport={"width": 1280, "height": 900},
        )
        page = ctx.new_page()
        for i, url in enumerate(urls):
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
            except Exception as e:
                print(f"[{i}] goto ERR: {e}")
            time.sleep(5)
            html = page.content()
            title = page.title()
            print(f"[{i}] {url}")
            print(f"    title: {title}")
            print(f"    bytes: {len(html)}")
            print(f"    has /item/: {'/item/' in html}")
            print(f"    has captcha: {'captcha' in html.lower() or 'punish' in html.lower()}")
            (OUT / f"page_{i}.html").write_text(html, encoding="utf-8")
            try:
                page.screenshot(path=str(OUT / f"page_{i}.png"), full_page=False)
            except Exception:
                pass
        browser.close()


if __name__ == "__main__":
    run()
