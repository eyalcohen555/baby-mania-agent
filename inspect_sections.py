import sys, io, re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

html2 = Path("output/stage-outputs/10085913231673_blog_article_2.html").read_text(encoding="utf-8")
html3 = Path("output/stage-outputs/10085913231673_blog_article_3.html").read_text(encoding="utf-8")

# C1: dependency section
m = re.search(r'id="dependency".{0,1500}', html2, re.DOTALL)
print("=== C1 #dependency ===")
print(m.group(0)[:900] if m else "NOT FOUND")

# C4: what-is section
print()
m2 = re.search(r'id="what-is".{0,1200}', html3, re.DOTALL)
print("=== C4 #what-is ===")
print(m2.group(0)[:700] if m2 else "NOT FOUND")

# C4: criteria section (first list item)
print()
m3 = re.search(r'id="criteria".{0,2000}', html3, re.DOTALL)
print("=== C4 #criteria (first item) ===")
print(m3.group(0)[:900] if m3 else "NOT FOUND")
