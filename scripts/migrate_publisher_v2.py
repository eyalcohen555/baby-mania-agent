#!/usr/bin/env python3
"""
BabyMania — publisher.json V1 → V2 Migration
=============================================
V1 (old):  { "fabric": {...}, "benefits": [...], "care": [...], "faq": [...] }
V2 (new):  { "metafields": { "hero_eyebrow": ..., "fabric_title": ..., ... } }

Usage:
  python scripts/migrate_publisher_v2.py [--dry-run] [--pid 12345]
"""
import argparse
import json
import re
import sys
from pathlib import Path

BASE_DIR      = Path(__file__).parent.parent
STAGE_OUT_DIR = BASE_DIR / "output" / "stage-outputs"

# ── Parsers ────────────────────────────────────────────────────────────────────

def _first_line(text: str) -> str:
    """Return first non-empty line of text."""
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def parse_fabric_story(text: str) -> dict:
    """
    Parse fabric_story.txt — handles both formats:
      NEW: hero_eyebrow / hero_headline / hero_subheadline at top + whats_special at bottom
      OLD: fabric_story: block only
    Returns dict with all available keys.
    """
    result = {}
    lines  = text.strip().splitlines()

    # Detect format: new format starts with 'hero_eyebrow:'
    is_new = any(l.strip().startswith("hero_eyebrow:") for l in lines)

    if is_new:
        for line in lines:
            line = line.strip()
            for key in ("hero_eyebrow", "hero_headline", "hero_subheadline", "whats_special"):
                if line.startswith(f"{key}:"):
                    result[key] = line.split(":", 1)[1].strip()
            if line.startswith("title:"):
                result["fabric_title"] = line.split(":", 1)[1].strip()
            elif line.startswith("body_2:"):
                result["fabric_body_2"] = line.split(":", 1)[1].strip()
            elif line.startswith("body:"):
                result["fabric_body"] = line.split(":", 1)[1].strip()
            elif line.startswith("highlight_quote:"):
                result["fabric_highlight"] = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("tags:"):
                raw = line.split(":", 1)[1].strip()
                result["fabric_tags"] = [t.strip().strip("[]") for t in raw.split("|") if t.strip()]
    else:
        # OLD format — parse inside fabric_story: block
        in_block = False
        for line in lines:
            stripped = line.strip()
            if stripped == "fabric_story:":
                in_block = True
                continue
            if not in_block:
                continue
            if stripped.startswith("title:"):
                result["fabric_title"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("body_2:"):
                result["fabric_body_2"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("body:"):
                result["fabric_body"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("highlight_quote:"):
                result["fabric_highlight"] = stripped.split(":", 1)[1].strip().strip('"')
            elif stripped.startswith("tags:"):
                raw = stripped.split(":", 1)[1].strip()
                result["fabric_tags"] = [t.strip() for t in raw.split("|") if t.strip()]

    return result


def parse_benefits(text: str) -> list:
    """
    Parse benefits.txt lines: `- 🌟 | title | description`
    Returns list of {icon, title, description}.
    """
    items = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue
        parts = [p.strip() for p in line.lstrip("-").split("|")]
        if len(parts) >= 3:
            items.append({"icon": parts[0], "title": parts[1], "description": parts[2]})
        elif len(parts) == 2:
            items.append({"icon": "", "title": parts[0], "description": parts[1]})
    return items


def parse_faq(text: str) -> list:
    """
    Parse faq.txt: Q: / A: pairs.
    Returns list of {question, answer}.
    """
    items = []
    current_q = None
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("Q:"):
            current_q = line[2:].strip()
        elif line.startswith("A:") and current_q is not None:
            items.append({"question": current_q, "answer": line[2:].strip()})
            current_q = None
    return items


def parse_care(text: str) -> list:
    """
    Parse care_instructions.txt: `- icon_type | card_title | card_text`
    Returns list of {icon_type, card_title, card_text}.
    """
    items = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue
        parts = [p.strip() for p in line.lstrip("-").split("|")]
        if len(parts) >= 3:
            items.append({"icon_type": parts[0], "card_title": parts[1], "card_text": parts[2]})
    return items


def load_analyzer(pid: str) -> dict:
    """Load analyzer.yaml for a product. Returns {} if missing."""
    import yaml
    path = STAGE_OUT_DIR / f"{pid}_analyzer.yaml"
    if not path.exists():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def read_stage(pid: str, suffix: str) -> str:
    """Read a stage output file. Returns '' if missing."""
    path = STAGE_OUT_DIR / f"{pid}_{suffix}"
    return path.read_text(encoding="utf-8") if path.exists() else ""


# ── Hero field derivation (for OLD format without hero fields) ─────────────────

def derive_hero_fields(analyzer: dict, fabric: dict, benefits: list) -> dict:
    """
    Derive hero_eyebrow / hero_headline / hero_subheadline / whats_special /
    emotional_reassurance from available data when fabric_story.txt is OLD format.
    """
    title       = analyzer.get("product_title", "")
    target_age  = analyzer.get("target_age", "")
    main_use    = analyzer.get("main_use", "")
    fabric_body = fabric.get("fabric_body", "")
    fab_title   = fabric.get("fabric_title", "")

    # hero_eyebrow: age + short category
    if target_age:
        eyebrow = f"לתינוקות {target_age}"
    elif "0-18" in title or "0-18" in fabric_body:
        eyebrow = "לתינוקות 0–18 חודשים"
    else:
        eyebrow = "ביגוד לתינוקות"

    # hero_headline: brand/product name + short hook
    # Clean title from ™ and long handles
    clean_title = re.sub(r"™|®|–\s*", "", title).strip()
    clean_title = clean_title[:40]
    headline = clean_title if clean_title else fab_title

    # hero_subheadline: first sentence of fabric_body
    if fabric_body:
        first_sent = fabric_body.split("—")[0].split(".")[0].strip()
        subheadline = first_sent[:80] if first_sent else fab_title
    else:
        subheadline = fab_title

    # whats_special: most distinctive benefit (first one)
    if benefits:
        b = benefits[0]
        whats_special = f"{b['title']} — {b['description']}"
    elif fabric_body:
        whats_special = fabric_body[:100]
    else:
        whats_special = fab_title

    # emotional_reassurance: generic contextual reassurance
    if main_use and "חורף" in main_use:
        reassurance = "כשהתינוק חם ושקט — גם ההורים יכולים לנשום. הבחירה שלכם בדיוק נכונה."
    elif main_use and "קיץ" in main_use:
        reassurance = "בקיץ הישראלי, נוחות היא לא פינוק — היא צורך. בחרתם נכון."
    else:
        reassurance = "כשהתינוק נוח ושמח, כולם מנצחים. הבחירה שלכם בדיוק נכונה."

    return {
        "hero_eyebrow":         eyebrow,
        "hero_headline":        headline,
        "hero_subheadline":     subheadline,
        "whats_special":        whats_special,
        "emotional_reassurance": reassurance,
    }


# ── V1 migration ───────────────────────────────────────────────────────────────

def is_v1(data: dict) -> bool:
    return "metafields" not in data or not data.get("metafields")


def migrate_v1_to_v2(pid: str, v1: dict) -> dict:
    """
    Convert V1 publisher.json to V2.
    Reads stage files when available; falls back to V1 data otherwise.
    """
    # ── Load stage files ───────────────────────────────────────────────────────
    analyzer = load_analyzer(pid)

    fabric_story_txt = read_stage(pid, "fabric_story.txt")
    benefits_txt     = read_stage(pid, "benefits.txt")
    faq_txt          = read_stage(pid, "faq.txt")
    care_txt         = read_stage(pid, "care.txt")

    # ── Parse stage files (if present) ────────────────────────────────────────
    has_stage_files = bool(fabric_story_txt or benefits_txt or faq_txt or care_txt)

    if fabric_story_txt:
        fabric = parse_fabric_story(fabric_story_txt)
    else:
        # Fall back to V1 fabric block
        v1_fab = v1.get("fabric", {})
        fabric = {
            "fabric_title":    v1_fab.get("title", ""),
            "fabric_body":     v1_fab.get("body", ""),
            "fabric_body_2":   v1_fab.get("body_2", ""),
            "fabric_highlight": v1_fab.get("highlight_quote", "").strip('"'),
            "fabric_tags":     v1_fab.get("tags", []),
        }

    benefits = parse_benefits(benefits_txt) if benefits_txt else v1.get("benefits", [])
    faq      = parse_faq(faq_txt)           if faq_txt     else v1.get("faq", [])
    care     = parse_care(care_txt)         if care_txt    else [
        {"icon_type": c.get("icon_type",""), "card_title": c.get("card_title",""), "card_text": c.get("card_text","")}
        for c in v1.get("care", [])
    ]

    # ── Hero fields ────────────────────────────────────────────────────────────
    # If fabric_story.txt had hero fields already, they're in `fabric`
    has_hero = "hero_eyebrow" in fabric

    if not has_hero:
        derived = derive_hero_fields(analyzer, fabric, benefits)
        hero_eyebrow         = derived["hero_eyebrow"]
        hero_headline        = derived["hero_headline"]
        hero_subheadline     = derived["hero_subheadline"]
        whats_special        = derived["whats_special"]
        emotional_reassurance = derived["emotional_reassurance"]
    else:
        hero_eyebrow         = fabric.get("hero_eyebrow", "")
        hero_headline        = fabric.get("hero_headline", "")
        hero_subheadline     = fabric.get("hero_subheadline", "")
        whats_special        = fabric.get("whats_special", "")
        emotional_reassurance = v1.get("metafields", {}).get("emotional_reassurance", "")
        if not emotional_reassurance:
            derived = derive_hero_fields(analyzer, fabric, benefits)
            emotional_reassurance = derived["emotional_reassurance"]

    # ── Assemble V2 ────────────────────────────────────────────────────────────
    return {
        "product_id":            v1.get("product_id", pid),
        "product_handle":        v1.get("product_handle", analyzer.get("product_handle", "")),
        "product_template_type": v1.get("product_template_type", "clothing"),
        "template_action":       "set_suffix_clothing",
        "body_html_clear":       True,
        "metafields": {
            "hero_eyebrow":         hero_eyebrow,
            "hero_headline":        hero_headline,
            "hero_subheadline":     hero_subheadline,
            "fabric_title":         fabric.get("fabric_title", ""),
            "fabric_body":          fabric.get("fabric_body", ""),
            "fabric_body_2":        fabric.get("fabric_body_2", ""),
            "fabric_highlight":     fabric.get("fabric_highlight", ""),
            "fabric_tags":          fabric.get("fabric_tags", []),
            "whats_special":        whats_special,
            "benefits":             benefits,
            "emotional_reassurance": emotional_reassurance,
            "size_note":            v1.get("metafields", {}).get("size_note", ""),
            "care_instructions":    care,
            "faq":                  faq,
        },
    }


# ── Main ───────────────────────────────────────────────────────────────────────

def run(dry_run: bool = False, target_pid: str = None):
    publisher_files = sorted(STAGE_OUT_DIR.glob("*_publisher.json"))

    v1_files  = []
    v2_files  = []
    for f in publisher_files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        pid = f.stem.replace("_publisher", "")
        if target_pid and pid != target_pid:
            continue
        if is_v1(data):
            v1_files.append((pid, f, data))
        else:
            v2_files.append(pid)

    print(f"V2 (already correct): {len(v2_files)}")
    print(f"V1 (needs migration): {len(v1_files)}")
    if not v1_files:
        print("Nothing to migrate.")
        return []

    migrated = []
    errors   = []
    print()
    for pid, path, v1_data in v1_files:
        try:
            v2 = migrate_v1_to_v2(pid, v1_data)
            if dry_run:
                print(f"  [DRY-RUN] {pid}  hero_headline={v2['metafields'].get('hero_headline','')[:40]}")
            else:
                path.write_text(
                    json.dumps(v2, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                hero = v2["metafields"].get("hero_headline", "")[:40]
                mf_count = sum(1 for v in v2["metafields"].values() if v and v != [] and v != "")
                print(f"  OK  {pid}  metafields={mf_count}  headline={hero}")
                migrated.append(pid)
        except Exception as e:
            print(f"  ERROR  {pid}: {e}")
            errors.append(pid)

    print(f"\nMigrated: {len(migrated)}  Errors: {len(errors)}")
    return migrated


if __name__ == "__main__":
    import io
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    elif hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Migrate publisher.json V1 → V2")
    ap.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    ap.add_argument("--pid", default=None, help="Migrate only this product ID")
    args = ap.parse_args()
    run(dry_run=args.dry_run, target_pid=args.pid)
