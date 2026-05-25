"""
Organic Article Image Agent — BabyMania
Generates 2-3 premium images per article via Stitch (Imagen).
Default mode: --dry-run (no actual generation, no article modification).

Usage:
  python scripts/organic/generate_article_images.py --dry-run --batch 2
  python scripts/organic/generate_article_images.py --dry-run --article output/organic/hub16-crocs/HUB16_C1.md
  python scripts/organic/generate_article_images.py --generate --article output/organic/hub16-crocs/HUB16_C1.md

SAFETY: --generate and --update-md require explicit flags. Never runs live by default.
"""

import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).parent.parent.parent
ORGANIC_DIR = BASE_DIR / "output" / "organic"
MANIFEST_DIR = ORGANIC_DIR / "image-manifests"
SCHEDULE_FILE = ORGANIC_DIR / "publish-schedule-43.md"

# ─────────────────────────────────────────────────────────────
# PROMPT BUILDER — BabyMania Visual Contract v2.0
# ─────────────────────────────────────────────────────────────

def build_brand_style():
    return (
        "Premium Israeli baby boutique campaign photography. "
        "Warm luxury baby ecommerce aesthetic. "
        "Color palette: soft cream, warm beige, muted gold accents. "
        "Elegant, calm, nurturing atmosphere. Israeli home or garden setting."
    )


def build_quality_rules():
    return (
        "Ultra sharp professional editorial photography. "
        "Premium ecommerce campaign quality. "
        "Crisp details, realistic skin tones. "
        "Clean natural light — soft morning or late afternoon golden hour. "
        "High-end 85mm portrait lens look with gentle background bokeh. "
        "Polished commercial photography, not a casual snapshot. "
        "Main subject in sharp focus."
    )


def build_composition_rules(image_type):
    if image_type == "hero":
        return (
            "Wide landscape article hero image, approximately 16:9 ratio. "
            "Clean premium composition. "
            "Main subject centered or rule-of-thirds placement. "
            "Leave empty negative space on one side for potential text overlay. "
            "Child and product both sharp and clearly visible in frame. "
            "Background softly blurred — not distracting."
        )
    elif image_type == "product":
        return (
            "Product-focused lifestyle photograph. "
            "Product is the clear visual hero. "
            "Shot from a flattering 3/4 angle, product sharp and prominent. "
            "Minimal, clean background — neutral surface or softly blurred outdoor setting."
        )
    else:  # body / explanatory
        return (
            "Supporting editorial body image, 4:3 or portrait ratio. "
            "Focused tightly on the specific detail or moment from the scene description. "
            "Not generic — clear visual purpose aligned to the article context. "
            "Secondary elements support the story without clutter."
        )


# Maps hub folder → article product/topic in English
HUB_TOPIC_MAP = {
    "hub16-crocs":      "clog-style children's sandals",
    "hub12-led-shoes":  "LED light-up sneakers for kids",
    "hub13-water-shoes":"water shoes and aqua sandals for kids",
    "hub14-baby-carrier":"baby carrier and wrap",
    "hub15-breast-pump":"breast pump for nursing mothers",
    "hub7-extension":   "baby home safety",
    "hub8-extension":   "baby bedtime evening routine",
    "hub1-extension":   "baby night light",
    "hub2-extension":   "seasonal baby clothing",
    "hub3-extension":   "baby bath time",
    "hub4-extension":   "baby skin rash",
}

FOOTWEAR_HUBS = {"hub16-crocs", "hub12-led-shoes", "hub13-water-shoes"}

# Curated English scene descriptions per hub × placeholder_id
# Overrides generic Hebrew→English conversion for known combinations.
CURATED_SCENES = {
    ("hub16-crocs", "hero"): (
        "A toddler aged 2-3 walking barefoot-style on clean green grass in a beautiful Israeli garden, "
        "wearing powder-blue EVA clog sandals clearly visible on both feet. "
        "The clogs are round-toed, have a classic ventilation-hole pattern, an adjustable back strap, "
        "and a small colorful cartoon charm (excavator or truck shape) on the front — "
        "matching the actual store product style exactly. "
        "The child's feet and shoes fill roughly one third of the frame — shoes are sharp and unmissable. "
        "The child has a calm, natural expression — not over-posed. "
        "Golden morning light filtering softly through trees, warm and premium Israeli garden setting. "
        "This is a hero campaign shot: both child and shoes prominent, background beautifully blurred. "
        "ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS, NO WATERMARKS anywhere in this image."
    ),
    ("hub16-crocs", "pool"): (
        "A pair of colorful pastel clog-style children's sandals placed intentionally and neatly "
        "in the foreground on clean stone pool tiling, sharp and prominent. "
        "Two toddlers standing in soft focus in the background near a bright, clean backyard pool. "
        "Children are secondary — the sandals are the focal point. "
        "Warm afternoon summer light, safe shallow pool edge, calm and premium atmosphere."
    ),
    ("hub16-crocs", "fit"): (
        "Close-up of a toddler sitting on outdoor steps adjusting the back strap of pastel "
        "clog-style sandals on their foot. Tight crop on feet and hands. "
        "Natural afternoon light, clean stone steps, warm tones."
    ),
    ("hub16-crocs", "bench"): (
        "A toddler girl sitting relaxed on a wooden garden bench, looking down at her new "
        "light summer sandals with curiosity. Candid, warm afternoon garden light. "
        "Clean garden background softly blurred."
    ),
    ("hub16-crocs", "care"): (
        "Two pairs of colorful children's sandals hanging neatly to dry on a shaded terrace railing "
        "after a beach day. Beach bucket and toys softly visible in the background. "
        "Clean, warm, summer lifestyle feel. Shoes are sharp and prominent."
    ),
    ("hub8-extension", "crib"): (
        "A baby aged 5-6 months sleeping peacefully in a natural wood crib, wearing a white cotton "
        "sleep sack. Fitted beige sheet beneath, empty crib — no blanket, no pillow, no toys. "
        "A soft warm night light glows gently on a small bedside table. Calm, safe, premium nursery."
    ),
    ("hub7-extension", "hero"): (
        "A parent kneeling on a clean kitchen floor inserting a safety cover into a low electrical "
        "outlet. A baby (7 months old) crawls peacefully on a soft grey rug in the background. "
        "Warm natural home light, Israeli-style clean home interior."
    ),
    ("hub7-extension", "floor"): (
        "A baby aged 8 months crawling happily on a soft beige-grey rug in a clean Israeli living room. "
        "In the background: a sofa with cushions, a low table with corner protectors, "
        "a bookshelf anchored to the wall. Safe, warm, premium home setting."
    ),
    ("hub8-extension", "hero"): (
        "A parent wrapping a freshly bathed baby in a soft white towel after bath time. "
        "Warm amber night-light glow from a small lamp. "
        "Wall tiles in a natural wood-beige pattern. Calm, gentle, premium nursery atmosphere."
    ),
}


def build_product_rules(hub_folder, placeholder_id, image_type):
    """Inject footwear-specific visual guidance for shoe articles."""
    if hub_folder not in FOOTWEAR_HUBS:
        return ""
    if image_type == "hero":
        return (
            "FOOTWEAR RULE: The children's sandals must be clearly visible on the child's feet — "
            "not tiny background props. Show feet and shoes prominently. "
            "Use generic clog-style or sandal-style children's shoes. "
            "No visible brand name, trademark, or logo on the shoes."
        )
    if placeholder_id in ("pool", "beach", "care", "pair", "products"):
        return (
            "FOOTWEAR RULE: The sandals/shoes are the primary visual focus — "
            "placed intentionally in the foreground, sharp and clearly visible. "
            "Children or other elements are secondary, softly blurred. "
            "No brand logos or trademark text on shoes."
        )
    return "FOOTWEAR RULE: Children's footwear clearly visible. No brand logos."


def build_negative_rules():
    return (
        "STRICT NO TEXT RULE: absolutely zero text, zero words, zero letters, zero numbers, "
        "zero watermarks, zero captions, zero labels anywhere in this image — not on objects, "
        "not on clothing, not in the background, not floating in the scene. "
        "AVOID: low resolution, blurry main subject, amateur snapshot, "
        "generic stock photo look, over-smiling stock model children, "
        "distorted faces, distorted hands, extra fingers, extra limbs, "
        "logo, brand name visible on products, "
        "messy or cluttered background, plastic cheap colors, "
        "harsh direct sunlight, washed-out overexposed areas, "
        "dark dramatic shadows, uncomfortable or frightened expressions, "
        "unsafe baby sleep setup, baby in any danger."
    )


def build_scene(alt_text, detailed_alt, hub_folder, placeholder_id):
    """
    Returns an English scene description.
    Priority: curated scene > English construction from detailed_alt > wrapped Hebrew.
    """
    key = (hub_folder, placeholder_id)
    if key in CURATED_SCENES:
        return CURATED_SCENES[key]

    topic = HUB_TOPIC_MAP.get(hub_folder, "baby and toddler lifestyle")
    source = detailed_alt if detailed_alt else alt_text

    # Wrap Hebrew in strong English framing
    return (
        f"Scene for a {topic} article: {source}. "
        "Ensure the main subject is clear, intentional, and prominently composed. "
        "Israeli premium home or outdoor setting."
    )


def build_prompt(alt_text, detailed_alt, image_type, article_title, placeholder_id, rel_path,
                 hub_folder=""):
    brand       = build_brand_style()
    quality     = build_quality_rules()
    composition = build_composition_rules(image_type)
    product     = build_product_rules(hub_folder, placeholder_id, image_type)
    scene       = build_scene(alt_text, detailed_alt, hub_folder, placeholder_id)
    negative    = build_negative_rules()

    # Sleep safety override
    sleep_articles = UNSAFE_SLEEP_PLACEHOLDERS.get(rel_path, [])
    if placeholder_id in sleep_articles:
        scene = CURATED_SCENES.get((hub_folder, placeholder_id), scene)

    parts = [brand, quality, composition]
    if product:
        parts.append(product)
    parts.append(f"SCENE: {scene}")
    parts.append(negative)

    return " | ".join(parts)


# Safety modifier kept for reference (now embedded in CURATED_SCENES)
SLEEP_SAFETY_MODIFIER = (
    "Baby sleeping safely: no blankets, no pillows, no stuffed animals, "
    "fitted sheet only, empty sleep space."
)

# Batch 2 articles from publish-schedule-43.md
BATCH_MAP = {
    1: [
        "hub1-extension/HUB1_C5.md",
        "hub1-extension/HUB1_C6.md",
        "hub2-extension/HUB2_C6.md",
        "hub3-extension/HUB3_C5.md",
        "hub3-extension/HUB3_C6.md",
        "hub4-extension/HUB4_C5.md",
    ],
    2: [
        "hub7-extension/HUB7_C6.md",
        "hub8-extension/HUB8_C6.md",
        "hub16-crocs/HUB16_Pillar.md",
        "hub16-crocs/HUB16_C1.md",
        "hub16-crocs/HUB16_C2.md",
        "hub16-crocs/HUB16_C3.md",
    ],
    3: [
        "hub16-crocs/HUB16_C4.md",
        "hub16-crocs/HUB16_C5.md",
        "hub16-crocs/HUB16_C6.md",
        "hub12-led-shoes/HUB12_Pillar.md",
        "hub12-led-shoes/HUB12_C1.md",
        "hub12-led-shoes/HUB12_C2.md",
    ],
    4: [
        "hub12-led-shoes/HUB12_C3.md",
        "hub12-led-shoes/HUB12_C4.md",
        "hub12-led-shoes/HUB12_C5.md",
        "hub12-led-shoes/HUB12_C6.md",
        "hub13-water-shoes/HUB13_Pillar.md",
        "hub13-water-shoes/HUB13_C1.md",
    ],
    5: [
        "hub13-water-shoes/HUB13_C2.md",
        "hub13-water-shoes/HUB13_C3.md",
        "hub13-water-shoes/HUB13_C4.md",
        "hub13-water-shoes/HUB13_C5.md",
        "hub13-water-shoes/HUB13_C6.md",
        "hub14-baby-carrier/HUB14_Pillar.md",
    ],
    6: [
        "hub14-baby-carrier/HUB14_C1.md",
        "hub14-baby-carrier/HUB14_C2.md",
        "hub14-baby-carrier/HUB14_C3.md",
        "hub14-baby-carrier/HUB14_C4.md",
        "hub14-baby-carrier/HUB14_C5.md",
        "hub14-baby-carrier/HUB14_C6.md",
    ],
    7: [
        "hub15-breast-pump/HUB15_Pillar.md",
        "hub15-breast-pump/HUB15_C1.md",
        "hub15-breast-pump/HUB15_C2.md",
        "hub15-breast-pump/HUB15_C3.md",
        "hub15-breast-pump/HUB15_C4.md",
        "hub15-breast-pump/HUB15_C5.md",
        "hub15-breast-pump/HUB15_C6.md",
    ],
}

# Known unsafe sleep placeholders — must inject sleep safety modifier
UNSAFE_SLEEP_PLACEHOLDERS = {
    "hub8-extension/HUB8_C6.md": ["crib"],
}


def parse_frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not match:
        return {}, text
    fm_raw, body = match.group(1), match.group(2)
    fm = {}
    for line in fm_raw.splitlines():
        if ": " in line:
            k, v = line.split(": ", 1)
            fm[k.strip()] = v.strip()
    return fm, body


def detect_image_type(placeholder_id):
    """Classify placeholder into image type."""
    pid = placeholder_id.lower()
    if pid == "hero":
        return "hero"
    if pid in ("product", "pair", "products"):
        return "product"
    if pid in ("ticks-visual", "diagram", "carrier-vs-stroller-travel"):
        return "explanatory"
    return "body"


def extract_detailed_alt(body, placeholder_id):
    """Extract the *alt: ...* line that follows the placeholder."""
    pattern = rf"!\[.*?\]\(alt-placeholder-{re.escape(placeholder_id)}\)\n\*alt: (.*?)\*"
    match = re.search(pattern, body)
    if match:
        return match.group(1).strip()
    return None


def extract_placeholders(filepath):
    """Parse article and return list of placeholder dicts."""
    rel_path = str(filepath.relative_to(ORGANIC_DIR)).replace("\\", "/")
    text = filepath.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    slug = fm.get("slug", filepath.stem.lower())
    title = fm.get("title", "")
    hub_folder = filepath.parent.name

    placeholders = []
    pattern = r"!\[(.*?)\]\(alt-placeholder-(\S+?)\)"
    for match in re.finditer(pattern, body):
        alt_text = match.group(1).strip()
        placeholder_id = match.group(2).strip(")")

        image_type = detect_image_type(placeholder_id)
        detailed_alt = extract_detailed_alt(body, placeholder_id)
        prompt = build_prompt(alt_text, detailed_alt, image_type, title, placeholder_id, rel_path,
                             hub_folder)

        output_filename = f"{slug}-{placeholder_id}.jpg"
        output_path = filepath.parent / "images" / output_filename

        safety_flag = None
        sleep_articles = UNSAFE_SLEEP_PLACEHOLDERS.get(rel_path, [])
        if placeholder_id in sleep_articles:
            safety_flag = "SLEEP_SAFETY_OVERRIDE — removed blanket from prompt"

        placeholders.append({
            "placeholder_id": placeholder_id,
            "alt_text": alt_text,
            "detailed_alt": detailed_alt,
            "image_type": image_type,
            "prompt": prompt,
            "output_filename": output_filename,
            "output_path": str(output_path),
            "status": "PLANNED",
            "safety_flag": safety_flag,
        })

    return {
        "file": rel_path,
        "hub_folder": hub_folder,
        "slug": slug,
        "title": title,
        "images": placeholders,
        "images_count": len(placeholders),
        "qa_pass": len(placeholders) >= 2,
    }


def run_dry_run(article_data_list):
    """Print dry-run report without generating anything."""
    total_images = sum(a["images_count"] for a in article_data_list)
    print(f"\n{'='*60}")
    print(f"DRY RUN — {len(article_data_list)} articles | {total_images} images planned")
    print(f"{'='*60}")

    for art in article_data_list:
        qa_icon = "[OK]" if art["qa_pass"] else "[WARN]"
        print(f"\n{qa_icon} {art['file']}")
        print(f"   title: {art['title'][:60]}")
        print(f"   slug:  {art['slug']}")
        print(f"   images planned: {art['images_count']}")

        for img in art["images"]:
            flag_str = f" *** {img['safety_flag']} ***" if img["safety_flag"] else ""
            print(f"\n   [{img['image_type'].upper()}] alt-placeholder-{img['placeholder_id']}{flag_str}")
            print(f"   alt:    {img['alt_text'][:80]}")
            print(f"   save:   {Path(img['output_path']).relative_to(ORGANIC_DIR)}")
            print(f"   prompt: {img['prompt'][:120]}...")

    issues = [a for a in article_data_list if not a["qa_pass"]]
    if issues:
        print(f"\n[WARN] Articles with < 2 images: {[a['file'] for a in issues]}")
    else:
        print(f"\n[OK] All articles have >= 2 images planned.")


def save_manifest(article_data_list, batch_id, mode):
    """Save JSON manifest to output/organic/image-manifests/."""
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "batch": batch_id,
        "generated_at": datetime.now().isoformat(),
        "mode": mode,
        "articles_count": len(article_data_list),
        "images_total": sum(a["images_count"] for a in article_data_list),
        "articles": article_data_list,
    }
    filename = f"batch-{batch_id}-manifest.json" if batch_id else "single-article-manifest.json"
    out_path = MANIFEST_DIR / filename
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[MANIFEST] Saved: {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="BabyMania Organic Article Image Agent")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Print planned prompts and manifest only (default: ON)")
    parser.add_argument("--generate", action="store_true", default=False,
                        help="Actually generate images via Stitch (requires explicit flag)")
    parser.add_argument("--update-md", action="store_true", default=False,
                        help="Update article Markdown with real image paths (requires --generate + approval)")
    parser.add_argument("--batch", type=int, default=None,
                        help="Run on all articles in batch N (1-7)")
    parser.add_argument("--article", type=str, default=None,
                        help="Run on a single article file path")
    args = parser.parse_args()

    # Safety: prevent accidental live generation
    if args.generate:
        print("[NOTICE] --generate flag detected. Images will be created via Stitch.")
        print("[NOTICE] This is a LIVE operation. Press Ctrl+C within 3 seconds to abort.")
        import time
        time.sleep(3)
    elif not args.dry_run:
        args.dry_run = True

    # Resolve article list
    article_paths = []
    batch_id = args.batch

    if args.article:
        p = Path(args.article)
        if not p.is_absolute():
            p = BASE_DIR / p
        if not p.exists():
            print(f"[ERROR] Article not found: {p}")
            sys.exit(1)
        article_paths = [p]
        batch_id = None

    elif args.batch:
        if args.batch not in BATCH_MAP:
            print(f"[ERROR] Unknown batch: {args.batch}. Valid: 1-7")
            sys.exit(1)
        article_paths = [ORGANIC_DIR / rel for rel in BATCH_MAP[args.batch]]

    else:
        print("[ERROR] Provide --batch N or --article PATH")
        parser.print_help()
        sys.exit(1)

    # Parse all articles
    article_data_list = []
    for path in article_paths:
        if not path.exists():
            print(f"[WARN] File not found: {path}")
            continue
        data = extract_placeholders(path)
        article_data_list.append(data)

    if not article_data_list:
        print("[ERROR] No articles found.")
        sys.exit(1)

    # Dry-run: print + save manifest
    if not args.generate:
        run_dry_run(article_data_list)
        save_manifest(article_data_list, batch_id, "dry-run")
        print("\n[DRY RUN COMPLETE] No files were modified.")
        print("[NEXT STEP] Review prompts above, then run with --generate on one article for approval.")
        return

    # Generate mode (future — requires Stitch MCP integration)
    print("[GENERATE MODE] Stitch integration not yet wired.")
    print("To generate: call mcp__stitch__generate_screen_from_text for each prompt.")
    print("This will be implemented in Phase 2 after dry-run approval.")


if __name__ == "__main__":
    main()
