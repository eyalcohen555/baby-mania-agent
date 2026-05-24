"""Dump full HTML of one confirmed item and inspect structure for spec data."""
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_dump"
OUT.mkdir(exist_ok=True)


def run():
    items = [
        ("9690182418745", "1005006863845547"),  # BZDoll 60cm - confirmed
        ("9690182451513", "1005005188539088"),  # Loulou 50cm - confirmed
        ("9689589383481", "1005005317212200"),  # Levi#1 - confirmed
    ]
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 1280, "height": 900},
        )
        page = ctx.new_page()
        for pid, iid in items:
            url = f"https://www.aliexpress.com/item/{iid}.html"
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            time.sleep(6)
            for _ in range(6):
                page.evaluate("window.scrollBy(0, 1500)")
                time.sleep(0.6)
            time.sleep(2)
            html = page.content()
            f = OUT / f"{pid}_{iid}.html"
            f.write_text(html, encoding="utf-8")
            # Look for spec-table indicators
            hits = {
                "specification": html.lower().count("specification"),
                "props_": html.lower().count("props_"),
                "attrName": html.count("attrName"),
                "attrValue": html.count("attrValue"),
                "Brand Name": html.count("Brand Name"),
                "Material": html.count("Material"),
                "__INIT_DATA__": html.count("__INIT_DATA__"),
                "runParams": html.count("runParams"),
                "props ": html.lower().count("\"props\""),
                "<table": html.count("<table"),
            }
            print(f"{iid}: {hits}")
            # Try to find spec block heuristically
            for m in re.finditer(r'<title>.*?</title>', html):
                print(f"  title: {m.group(0)[:200]}")
                break

        browser.close()


if __name__ == "__main__":
    run()
