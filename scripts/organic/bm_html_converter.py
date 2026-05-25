"""
BabyMania Markdown -> Structured HTML Converter  (v2)
Phase 2 fix — handles 2 source formats (HUB-7/8 vs HUB-16).

Bugs fixed:
  1. ```json blocks → extracted and wrapped in <script type="application/ld+json">
  2. [IMG_ALT_N: ...] markers → stripped
  3. Plain markdown → BabyMania HTML class wrappers (intro-box, toc, article-body, cta-banner, faq, article-tags)

Format A (HUB-7, HUB-8):
  - FAQ: ### H3 question headers
  - JSON-LD: ```json code fence

Format B (HUB-16):
  - FAQ: **Bold question** text format
  - JSON-LD: <script type="application/ld+json"> already in source
  - CTA: ## CTA explicit section
  - Internal links: **Internal links:** block (editorial — strip)
"""

import re
import markdown as _md


# ── Artifact stripping ──────────────────────────────────────────────────────

def _strip_artifacts(body):
    body = re.sub(r'^#\s+.+\n?', '', body, count=1)
    body = re.sub(
        r'!\[[^\]]*\]\((?:alt-placeholder|images/)[^\)]*\)\n?(?:\*alt:.*?\*)?\n?',
        '', body
    )
    body = re.sub(r'^\*alt:.*?\*[ \t]*\n?', '', body, flags=re.MULTILINE)
    body = re.sub(r'\[IMG_ALT_\d+:[^\]]*\]', '', body)
    # Strip editorial **Internal links:** section (everything from that point)
    body = re.sub(r'\n\*\*Internal links:\*\*.*', '', body, flags=re.DOTALL)
    return body


def _extract_json_ld(body):
    """Extract JSON-LD from either ```json fences or <script> tags."""
    json_ld_tag = None

    # Format A: ```json ... ``` fence
    pat_fence = r'```json\s*\n([\s\S]*?)\n```'
    m = re.search(pat_fence, body)
    if m:
        json_text = m.group(1).strip()
        json_ld_tag = f'<script type="application/ld+json">\n{json_text}\n</script>'
        body = re.sub(pat_fence, '', body)

    # Format B: <script type="application/ld+json">...</script> already present
    pat_script = r'<script type="application/ld\+json">[\s\S]*?</script>'
    m2 = re.search(pat_script, body)
    if m2 and json_ld_tag is None:
        json_ld_tag = m2.group(0)
        body = re.sub(pat_script, '', body)

    return body, json_ld_tag


# ── Helpers ──────────────────────────────────────────────────────────────────

def _to_html(md_text):
    return _md.markdown(md_text.strip(), extensions=['extra', 'nl2br'])


def _split_h2(body):
    parts = re.split(r'^## (.+)$', body, flags=re.MULTILINE)
    sections = []
    if parts[0].strip():
        sections.append(('', parts[0]))
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        content = parts[i + 1] if i + 1 < len(parts) else ''
        sections.append((title, content))
    return sections


# ── HTML block builders ───────────────────────────────────────────────────────

def _build_intro_box(content):
    paragraphs = [p.strip() for p in content.strip().split('\n\n') if p.strip()]
    if not paragraphs:
        return ''
    intro_html = _to_html(paragraphs[0])
    return f'<div class="intro-box" dir="rtl">\n{intro_html}\n</div>\n'


def _build_toc(entries, has_faq):
    items = [f'    <li><a href="#{aid}">{title}</a></li>' for aid, title in entries]
    if has_faq:
        items.append('    <li><a href="#faq">שאלות נפוצות</a></li>')
    return (
        '<nav class="toc" dir="rtl">\n'
        '  <p class="toc-title">תוכן המאמר</p>\n'
        '  <ol>\n'
        + '\n'.join(items) +
        '\n  </ol>\n</nav>\n'
    )


def _build_section(anchor_id, title, content):
    return f'<h2 id="{anchor_id}">{title}</h2>\n{_to_html(content)}\n'


def _build_cta_from_content(content):
    """CTA from ## CTA section content (Format B)."""
    body_html = _to_html(content)
    return (
        '<div class="cta-banner" dir="rtl">\n'
        f'{body_html}\n'
        '</div>\n'
    )


def _build_cta_from_fm(fm):
    """CTA generated from frontmatter (Format A — no explicit CTA section)."""
    handle = fm.get('target_product_handle', '/collections/all')
    keyword = fm.get('keyword_main', 'מוצרי תינוק')
    url = f"https://babymania-il.com{handle}"
    return (
        '<div class="cta-banner" dir="rtl">\n'
        f'  <h3>מחפשים {keyword}?</h3>\n'
        '  <p>ב-BabyMania תמצאו מבחר איכותי של מוצרי תינוקות — בגדים, נעליים ואביזרים לגיל 0–4.</p>\n'
        '  <div class="cta-buttons">\n'
        f'    <a class="cta-btn" href="{url}">לצפייה בחנות</a>\n'
        '  </div>\n'
        '</div>\n'
    )


def _build_faq(content, json_ld_tag):
    """Build FAQ section — auto-detects H3 vs Bold format."""
    has_h3 = bool(re.search(r'^### .+$', content, re.MULTILINE))
    has_bold = bool(re.search(r'(?:^|\n)\*\*[^*\n]+\*\*\n', content))

    details_items = []

    if has_h3:
        # Format A: ### Question\nAnswer
        parts = re.split(r'^### (.+)$', content, flags=re.MULTILINE)
        for i in range(1, len(parts), 2):
            question = parts[i].strip()
            answer_md = (parts[i + 1] if i + 1 < len(parts) else '').strip()
            if question and answer_md:
                answer_html = _to_html(answer_md)
                details_items.append(
                    f'  <details>\n    <summary>{question}</summary>\n    <div>{answer_html}</div>\n  </details>'
                )
    elif has_bold:
        # Format B: **Question**\nAnswer
        # Strip horizontal rules and leading blank lines from content
        content_clean = re.sub(r'^---\s*$', '', content, flags=re.MULTILINE)
        parts = re.split(r'(?:^|\n)\*\*([^*\n]+)\*\*\n', content_clean)
        for i in range(1, len(parts), 2):
            question = parts[i].strip()
            answer_md = (parts[i + 1] if i + 1 < len(parts) else '').strip()
            # Remove any nested --- that slipped in
            answer_md = re.sub(r'^---\s*$', '', answer_md, flags=re.MULTILINE).strip()
            if question and answer_md:
                answer_html = _to_html(answer_md)
                details_items.append(
                    f'  <details>\n    <summary>{question}</summary>\n    <div>{answer_html}</div>\n  </details>'
                )

    items_str = '\n'.join(details_items)
    script = f'\n{json_ld_tag}' if json_ld_tag else ''

    return (
        '<section id="faq" class="faq" dir="rtl">\n'
        '  <h2 class="faq-title">שאלות נפוצות</h2>\n'
        f'{items_str}\n'
        '</section>\n'
        f'{script}\n'
    )


def _build_tags(fm):
    main = fm.get('keyword_main', '')
    secondary = fm.get('keyword_secondary', '')
    raw = (main + ',' + secondary) if secondary else main
    tags = [t.strip() for t in raw.split(',') if t.strip()][:7]
    pills = ''.join(f'<span class="tag">{t}</span>' for t in tags)
    return f'<div class="article-tags" dir="rtl">{pills}</div>\n'


# ── Main entry ────────────────────────────────────────────────────────────────

def convert(fm, body_md):
    """Convert BabyMania organic markdown body to structured body_html."""
    body_md = _strip_artifacts(body_md)
    body_md, json_ld_tag = _extract_json_ld(body_md)

    sections = _split_h2(body_md)

    intro_html = ''
    toc_entries = []
    body_sections = []
    faq_content = None
    cta_content = None
    faq_present = False
    idx = 0

    for title, content in sections:
        if title in ('', 'מבוא'):
            intro_html = _build_intro_box(content)
        elif title == 'שאלות נפוצות':
            faq_content = content
            faq_present = True
        elif title == 'CTA':
            cta_content = content
        else:
            idx += 1
            anchor_id = f'h2-{idx}'
            toc_entries.append((anchor_id, title))
            body_sections.append(_build_section(anchor_id, title, content))

    # Fallback: no מבוא section — use first paragraph of first body section
    if not intro_html and body_sections:
        m = re.search(r'<p>(.*?)</p>', body_sections[0], re.DOTALL)
        if m:
            intro_html = f'<div class="intro-box" dir="rtl">\n<p>{m.group(1)}</p>\n</div>\n'

    toc_html = _build_toc(toc_entries, has_faq=faq_present)
    article_body = (
        '<div class="article-body" dir="rtl">\n'
        + '\n'.join(body_sections)
        + '\n</div>\n'
    )

    if cta_content:
        cta_html = _build_cta_from_content(cta_content)
    else:
        cta_html = _build_cta_from_fm(fm)

    faq_html = _build_faq(faq_content or '', json_ld_tag) if faq_present else ''
    tags_html = _build_tags(fm)

    return intro_html + toc_html + article_body + cta_html + faq_html + tags_html


# ── QA checks ─────────────────────────────────────────────────────────────────

def qa_checks(html, source_had_json_ld=True):
    """13 QA checks. Returns list of (name, passed, detail)."""
    checks = []

    def chk(name, passed, detail=''):
        checks.append((name, passed, detail))

    chk('no-json-fence',    '```json' not in html)
    chk('no-img-alt-n',     '[IMG_ALT_' not in html)
    chk('no-placeholder',   'alt-placeholder' not in html)
    chk('no-images-path',   'src="images/' not in html and '](images/' not in html)
    chk('has-intro-box',    'class="intro-box"' in html)
    chk('has-toc',          'class="toc"' in html)
    chk('has-article-body', 'class="article-body"' in html)
    chk('has-cta-banner',   'class="cta-banner"' in html)
    chk('has-faq-section',  'id="faq"' in html)
    chk('has-details',      '<details>' in html)
    chk('has-json-ld',
        'application/ld+json' in html,
        '' if source_had_json_ld else '(source had no JSON-LD)')
    chk('no-pre-code-leak', '<pre><code>' not in html)
    chk('min-length',       len(html) >= 3000, f'{len(html):,} chars')

    return checks
