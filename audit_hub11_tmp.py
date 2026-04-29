import re
from pathlib import Path

hub11_dir = Path('C:/Projects/baby-mania-agent/output/hub11-summer-clothing')
articles = [
    ('HUB-11-Pillar', 'HUB11_Pillar_blog_article.html'),
    ('HUB-11-C1',     'HUB11_C1_blog_article.html'),
    ('HUB-11-C2',     'HUB11_C2_blog_article.html'),
    ('HUB-11-C3',     'HUB11_C3_blog_article.html'),
    ('HUB-11-C4',     'HUB11_C4_blog_article.html'),
    ('HUB-11-C5',     'HUB11_C5_blog_article.html'),
    ('HUB-11-C6',     'HUB11_C6_blog_article.html'),
]

PAT_PROD = re.compile(r'href=["\'](?:https?://[^/]+)?/products/([^"\'#?]+)["\']')
PAT_BLOG = re.compile(r'href=["\'](?:https?://[^/]+)?/blogs/news/([^"\'#?]+)["\']')

for cluster_id, fname in articles:
    html = (hub11_dir / fname).read_text(encoding='utf-8')
    prods = list(dict.fromkeys(PAT_PROD.findall(html)))
    blogs = list(dict.fromkeys(PAT_BLOG.findall(html)))
    print(cluster_id)
    for p in prods:
        print("  PROD:", p)
    for b in blogs:
        print("  BLOG:", b)
    print()
