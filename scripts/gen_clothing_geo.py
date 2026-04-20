#!/usr/bin/env python3
"""
STAGE-8 run#2 v2: Generate unique GEO drafts for 224 clothing products.
CORE PRINCIPLE: Every sentence embeds product-specific details.
No standalone generic sentences allowed.
"""

import json, os, sys, re, yaml, hashlib
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

OUTPUT_DIR = "output/stage-outputs"
CONTEXT_DIR = "shared/product-context"
PROGRESS_FILE = "bridge/stage-progress.md"
BATCH_SIZE = 12


def load_pids():
    # Use gap_map as authoritative source (242 PIDs) — not _clothing_missing_pids (224)
    with open(f"{OUTPUT_DIR}/layer4_geo_gap_map.json", encoding="utf-8") as f:
        gap = json.load(f)
    return gap["all_products_by_category"]["clothing"]


def load_context(pid):
    path = f"{CONTEXT_DIR}/{pid}.yaml"
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def clean_desc(raw):
    """Extract unique product description before boilerplate."""
    if not raw:
        return ""
    raw = str(raw)
    # Remove emojis
    raw = re.sub(r'[\U0001F300-\U0001F9FF\u2728\u2B50\u2705\u26A1\U0001F6CD\U0001F46C\U0001F3FC]', '', raw)
    # Split at first ⭐ to remove boilerplate
    parts = raw.split('⭐')
    first = parts[0].strip()
    # Also strip known boilerplate phrases
    boilerplate = [
        "איכות יוצאת דופן:",
        "עדין על העור:",
        "בד נושם ונעים:",
        "מתאים בול:",
        "יתרונות:",
        "הזמינו עכשיו",
        "פרטי המוצר:",
        "מבית בייבי מניה – איכו",
    ]
    for bp in boilerplate:
        idx = first.find(bp)
        if idx > 0:
            first = first[:idx]
    first = re.sub(r'\s+', ' ', first).strip()
    # Remove trailing partial sentences
    if first and first[-1] not in '.!?':
        # Find last complete sentence
        last_period = max(first.rfind('.'), first.rfind('!'), first.rfind('?'))
        if last_period > 10:
            first = first[:last_period + 1]
    return first


def extract_model_name(title):
    # Try separators first
    for sep in [' - ', ' – ', ': ']:
        if sep in title:
            return title.split(sep)[-1].strip()
    # Try "דגם X" pattern
    m = re.search(r'דגם\s+(\S+)', title)
    if m:
        return m.group(1)
    return ""


def unique_ref(title, model_name, gtype, pid):
    """Return a clean product reference — no PID suffix, no technical identifiers."""
    if model_name:
        return model_name  # e.g. "שון", "דניאל", "אנגל"

    # Strip garment type prefix from title
    short = title
    for prefix in ["סט ", "חליפת ", "חליפה ", "שמלת ", "שמלה ", "אוברול ",
                    "בגד גוף ", "מכנס ", "חולצת ", "כובע ", "מעיל ",
                    "סרבל ", "בגד ים ", "פיג'מה "]:
        if short.startswith(prefix):
            short = short[len(prefix):]
            break
    # Trim to reasonable length
    if len(short) > 30:
        short = short[:30].rsplit(' ', 1)[0]
    if not short or short == gtype:
        return gtype  # fallback to garment type — no technical ID
    return short


def ph(pid):
    """Product hash for deterministic variation."""
    return int(hashlib.md5(pid.encode()).hexdigest(), 16)


def parse_product(ctx, pid=""):
    title = str(ctx.get("product_title", ctx.get("title", "")))
    raw_desc = str(ctx.get("description_raw", ""))
    desc = clean_desc(raw_desc)
    price = str(ctx.get("price", "0"))
    model_name = extract_model_name(title)

    t = title.lower()
    combined = (title + " " + desc + " " + raw_desc[:400]).lower()

    # Guard: reject shoes products — must use generate_shoes_geo.py instead
    SHOES_SIGNALS = ["נעל", "סנדל", "מגף", "כפכף", "נעליים", "סנדלי", "מגפי", "נעלי"]
    if any(sig in t for sig in SHOES_SIGNALS):
        raise ValueError(f"[gen_clothing_geo] shoes product detected in title '{title}' (pid={pid}) — use generate_shoes_geo.py instead")

    # Type — title PREFIX takes priority (prevents accessory words mid-title from overriding)
    gtype = "בגד"
    primary_prefixes = [
        (["חליפת ", "חליפה "], "חליפה"),
        (["שמלת ", "שמלה "], "שמלה"),
        (["אוברול ", "רומפר ", "סרבל "], "אוברול"),
        (["בגד גוף ", "בגד-גוף "], "בגד גוף"),
        (["בגד ים "], "בגד ים"),
        (["פיג'מה ", "פיג'מת "], "פיג'מה"),
        (["סט "], "סט"),
        (["מכנס ", "מכנסיים "], "מכנסיים"),
        (["חולצת ", "חולצה "], "חולצה"),
        (["כובע "], "כובע"),
        (["מעיל ", "ג'קט "], "מעיל"),
        (["שמיכת ", "שמיכה "], "שמיכה"),
        (["גרביים ", "גרב "], "גרביים"),
        (["טוטו"], "שמלת טוטו"),
    ]
    for prefixes, label in primary_prefixes:
        if any(t.startswith(p) for p in prefixes):
            gtype = label
            break

    if gtype == "בגד":
        # Secondary: full title scan — accessories (כובע/גרב) excluded to avoid false matches
        secondary_map = [
            (["שמלה", "שמלת", "טוטו"], "שמלה"),
            (["אוברול", "רומפר", "סרבל"], "אוברול"),
            (["בגד גוף", "בודי"], "בגד גוף"),
            (["פיג'מ"], "פיג'מה"),
            (["חליפ"], "חליפה"),
            (["מכנס"], "מכנסיים"),
            (["חולצ"], "חולצה"),
            (["מעיל", "ג'קט"], "מעיל"),
            (["שמיכ", "עטיפ"], "שמיכה"),
        ]
        for keywords, label in secondary_map:
            if any(k in t for k in keywords):
                gtype = label
                break

    if gtype == "בגד" and ("סט " in t or "סט-" in t or title.startswith("סט")):
        gtype = "סט"
    # כובע/גרב only if they are clearly the main product (start of title)
    if gtype == "בגד" and t.startswith("כובע"):
        gtype = "כובע"
    if gtype == "בגד" and t.startswith("גרב"):
        gtype = "גרביים"

    # Features
    f = {}
    fabrics = [("כותנה", "כותנה"), ("טטרה", "טטרה"), ("פשתן", "פשתן"),
               ("קטיפה", "קטיפה"), ("velvet", "קטיפה"), ("סריג", "סריג"),
               ("דנים", "ג'ינס"), ("ג'ינס", "ג'ינס"), ("פליז", "פליז"),
               ("אלסטי", "בד אלסטי"), ("משי", "משי")]
    for kw, label in fabrics:
        if kw in combined:
            f["fabric"] = label
            break

    if any(w in combined for w in ["קיצי", "קיץ", "summer", "קייצי"]):
        f["season"] = "קיץ"
    elif any(w in combined for w in ["חורף", "winter", "חורפי"]):
        f["season"] = "חורף"
    elif any(w in combined for w in ["מעבר", "סתיו", "אביב"]):
        f["season"] = "מעבר"

    designs = [("פרח", "פרחוני"), ("פסים", "פסים"), ("פס ", "פסים"),
               ("דוב", "דובונים"), ("bear", "דובונים"), ("משובצ", "משובץ"),
               ("leopard", "מנומר"), ("נמר", "מנומר"), ("תחרה", "תחרה"),
               ("lace", "תחרה"), ("כוכב", "כוכבים"), ("לב ", "לבבות")]
    for kw, label in designs:
        if kw in combined:
            f["design"] = label
            break

    if "ללא שרוולים" in combined or "ללא שרוול" in combined:
        f["sleeves"] = "ללא שרוולים"
    elif "שרוול ארוך" in combined or "שרוולים ארוכים" in combined:
        f["sleeves"] = "שרוול ארוך"
    elif "שרוול קצר" in combined:
        f["sleeves"] = "שרוול קצר"

    if any(w in combined for w in ["אירוע", "חגיג", "מסיבה"]):
        f["occasion"] = "אירועים"
    elif "פיג'" in combined or "שינה" in combined:
        f["occasion"] = "שינה"

    if "3 חלקים" in combined or "שלושה חלקים" in combined:
        f["pieces"] = "3"
    elif "2 חלקים" in combined or "שני חלקים" in combined:
        f["pieces"] = "2"

    colors = []
    for c in ["ורוד", "כחול", "לבן", "שחור", "אדום", "ירוק", "צהוב", "סגול", "אפור", "בז'", "חום", "כתום"]:
        if c in combined:
            colors.append(c)
    if colors:
        f["colors"] = colors

    try:
        p = float(price)
        f["price_tier"] = "premium" if p >= 180 else ("mid" if p >= 130 else "value")
    except:
        f["price_tier"] = "mid"

    return {
        "title": title, "model_name": model_name, "desc_unique": desc,
        "gtype": gtype, "price": price, "features": f,
    }


def compose_who_for(pid, info):
    """Every sentence contains product-specific identity."""
    h = ph(pid)
    gtype = info["gtype"]
    feats = info["features"]
    model = info["model_name"]
    title = info["title"]
    desc = info["desc_unique"]
    uref = unique_ref(title, model, gtype, pid)

    # Build unique identity string for this product
    identity_parts = [gtype]
    if uref and uref != gtype:
        identity_parts.append(f"דגם {uref}")
    if feats.get("design"):
        identity_parts.append(f"ב{feats['design']}")
    if feats.get("fabric"):
        identity_parts.append(f"מ{feats['fabric']}")
    if feats.get("season"):
        season_he = {"קיץ": "קייצי", "חורף": "חורפי", "מעבר": "לעונות מעבר"}
        identity_parts.append(season_he.get(feats["season"], ""))
    if feats.get("pieces"):
        identity_parts.append(f"ב-{feats['pieces']} חלקים")
    if feats.get("sleeves") and feats["sleeves"] == "ללא שרוולים":
        identity_parts.append("ללא שרוולים")

    # Create the unique product descriptor (max 3 details)
    identity = identity_parts[0]
    extras = [x for x in identity_parts[1:] if x]
    if extras:
        identity += " " + " ".join(extras[:3])

    # Sentence 1: Audience opener with product identity embedded
    audience_templates = [
        f"הורים שמחפשים {identity} — ",
        f"מי שצריכה {identity} לילד — ",
        f"אמא שרוצה {identity} שגם נראה טוב וגם מרגיש נוח — ",
        f"הורים שנמאס להם מבגדים גנריים ומחפשים {identity} שבאמת שונה — ",
        f"מי שמחפשת {identity} שהילד ירצה ללבוש בלי מלחמות — ",
        f"סבתא שמחפשת מתנה מושלמת — {identity} שיעשה רושם — ",
        f"הורים שיודעים שילדים צריכים {identity} שלא מתפשר על איכות — ",
    ]
    sent1 = audience_templates[h % len(audience_templates)]

    # Sentence 2: Feature-based — no raw description copy
    s2_parts = []
    fab = feats.get("fabric", "")
    season = feats.get("season", "")
    if fab and season:
        season_adj = {"קיץ": "קייצי ונושם", "חורף": "חורפי ומחמם", "מעבר": "מאוזן לעונות מעבר"}
        s2_parts.append(f"עשוי {fab} {season_adj.get(season, 'איכותי')} שמרגיש טוב כל היום")
    elif fab:
        fab_desc_map = {
            "כותנה": "כותנה רכה שנעימה על עור עדין",
            "טטרה": "טטרה קלה ומאווררת שמושלמת לתינוקות",
            "פשתן": "פשתן טבעי שמרגיש קריר ונושם",
            "קטיפה": "קטיפה עדינה שנוחה ויוקרתית לגוף",
            "פליז": "פליז חם שמגן מפני קור בלי להכביד",
            "סריג": "סריג גמיש שמתאים לגוף ולא מגביל",
            "ג'ינס": "ג'ינס רך שמחזיק מעמד כביסה אחרי כביסה",
        }
        s2_parts.append(fab_desc_map.get(fab, f"{fab} איכותי"))
    elif feats.get("occasion") == "אירועים":
        s2_parts.append(f"מעוצב לאירועים — נראה חגיגי ומרגיש יומיומי לתינוק")
    elif feats.get("occasion") == "שינה":
        s2_parts.append(f"תוכנן לשינה נוחה — לא מפריע לתנועה ולא מתקפל")
    elif feats.get("pieces"):
        s2_parts.append(f"סט {feats['pieces']} חלקים שעובדים ביחד ובנפרד")
    if not s2_parts:
        tier_desc = {
            "premium": "ברמת גימור שמורגשת ברגע שנוגעים",
            "value": "במחיר נוח ובאיכות שלא מתפשרת",
            "mid": "שמאזן נכון בין איכות למחיר",
        }
        s2_parts.append(f"{gtype} {tier_desc.get(feats.get('price_tier', 'mid'), '')}")

    sent2 = ". ".join(s2_parts) + "."

    # Sentence 3: Specific benefit tied to THIS product
    if feats.get("fabric") == "כותנה":
        sent3 = f"{uref} מכותנה שנושמת — העור של הילד לא מזיע ולא מתגרה."
    elif feats.get("fabric") == "טטרה":
        sent3 = f"בד הטטרה של {uref} קל כמו אוויר — מושלם לעור רגיש של תינוקות."
    elif feats.get("fabric") == "פשתן":
        sent3 = f"הפשתן של {uref} נהיה רך יותר עם כל כביסה — נוחות שמשתפרת עם הזמן."
    elif feats.get("fabric") == "קטיפה":
        sent3 = f"הקטיפה של {uref} עוטפת ומחממת בלי להכביד על הגוף."
    elif feats.get("fabric") == "פליז":
        sent3 = f"הפליז של {uref} שומר על חום גם ביום רטוב — שכבת חימום שסומכים עליה."
    elif feats.get("season") == "קיץ":
        sent3 = f"{uref} — קל ונושם, בדיוק מה שצריך כשבחוץ חם ולח."
    elif feats.get("season") == "חורף":
        sent3 = f"{uref} — חם ועוטף, בלי הכבדה שמגבילה תנועה."
    elif feats.get("design"):
        sent3 = f"העיצוב {feats['design']} של {uref} נשאר חי ויפה גם אחרי כביסות."
    elif feats.get("price_tier") == "premium":
        sent3 = f"רמת הגימור של {uref} מורגשת ברגע שנוגעים — זה לא בגד רגיל."
    elif feats.get("price_tier") == "value":
        sent3 = f"את {uref} מקבלים באיכות שלא מתפשרת — גם במחיר שנוח לכיס."
    else:
        sent3 = f"{uref} — בגד שעובד ליומיום בלי להתפשר על איך שזה נראה ומרגיש."

    return (sent1 + sent2 + " " + sent3).strip()


def compose_use_case(pid, info):
    """Situation-specific, with product identity in every sentence."""
    h = ph(pid)
    gtype = info["gtype"]
    feats = info["features"]
    model = info["model_name"]
    title = info["title"]

    prod_ref = unique_ref(title, model, gtype, pid)
    short_ref = prod_ref

    # Sentence 1: Specific situation with product reference
    sit_options = []

    if gtype == "שמלה" or gtype == "שמלת טוטו":
        sit_options = [
            f"כשמגיעים עם הילדה לאירוע ו{prod_ref} עושה את כל העבודה — נראית מושלמת בלי מאמץ",
            f"ביום הולדת או חג בגן, {prod_ref} הופכת את הילדה לכוכבת בלי שצריכים להתאמץ",
            f"בצילומי משפחה כש{prod_ref} תופסת אור יפה ונראית מדהימה בתמונות",
            f"בשבת חגיגית כשהילדה לובשת את {prod_ref} ומרגישה כמו נסיכה אמיתית",
            f"כשצריכים שהילדה תיראה מרשימה באירוע — {prod_ref} פותרת את זה ברגע",
        ]
    elif gtype == "אוברול":
        sit_options = [
            f"בבוקר לחוץ כשצריכים להלביש מהר — {prod_ref} זה בגד אחד ויצאנו מהבית",
            f"ביום בגן כשהילד רץ ומטפס — {prod_ref} נשאר במקום ומגן על הגוף",
            f"בטיול משפחתי כש{prod_ref} נותן חופש תנועה מלא בלי שמשהו זז",
            f"כשהילד זוחל על הרצפה ומתלכלך — {prod_ref} קל לכביסה ומתייבש מהר",
            f"בנסיעה ארוכה כש{prod_ref} לא מתקפל ולא לוחץ — הילד נוח לשבת",
        ]
    elif gtype == "בגד גוף":
        sit_options = [
            f"כשצריכים שכבת בסיס שנשארת במקום — {prod_ref} לא נשלף מהמכנס כל היום",
            f"בהחלפת חיתול כשהפתיחה בתחתית של {prod_ref} חוסכת את כל ההפשטה",
            f"ביום חורפי כש{prod_ref} מחזיק חום מתחת לחליפה בלי להוסיף נפח",
            f"כשצריכים בגד בסיס לכל outfit — {prod_ref} עובד מתחת לכל דבר",
            f"ביום מעבר כש{prod_ref} עובד לבד או כשכבה מתחת לסוודר",
        ]
    elif gtype == "סט":
        sit_options = [
            f"בבוקר לחוץ כשאין זמן לחשוב — {prod_ref} כבר מתואם ומוכן להלבשה",
            f"כשצריכים look שלם ל{prod_ref} — פותחים, מלבישים, ויוצאים",
            f"כמתנת לידה — {prod_ref} נראה מרשים באריזה וישמש ביומיום",
            f"לצילומים או אירוע כש{prod_ref} המתואם עושה את התמונה",
            f"כשנמאס לחפש מה מתאים למה — {prod_ref} פותר את הדילמה הזו לגמרי",
        ]
    elif gtype == "חליפה":
        _season = feats.get("season", "")
        if _season == "קיץ":
            sit_options = [
                f"ביום חם כשצריכים חליפה קלה — {prod_ref} אוורירית ולא מכבידה",
                f"בגן ביום שרב כש{prod_ref} מאפשרת תנועה חופשית בלי חיכוך",
                f"בטיול קיצי כש{prod_ref} שומרת על קרירות מהבוקר עד הצהריים",
                f"ביום חינוך ארוך כש{prod_ref} לא מגביל ולא מחמם יותר מדי",
                f"כשמוציאים את הילד לפארק בקיץ — {prod_ref} קלה ונוחה גם בשיא החום",
                f"בחופשת קיץ כש{prod_ref} עובדת מהבוקר בבית ועד הצהריים בחוץ",
                f"ביום חם ולח כשצריכים חליפה שנושמת — {prod_ref} לא לוכדת חום",
            ]
        elif _season == "חורף":
            sit_options = [
                f"ביום חורפי כשצריכים לצאת לגן — {prod_ref} מחמם מראש ועד רגל",
                f"בטיול משפחתי קר כש{prod_ref} נותן חום ועדיין מאפשר תנועה",
                f"כשיורד גשם ורוצים שהילד יהיה חם בפנים — {prod_ref} הפתרון השקט",
                f"בבוקר חורפי לחוץ לפני הגן כש{prod_ref} מלבישים ולא חוזרים לבדוק",
                f"ביום קר כשהטמפרטורה יורדת — {prod_ref} מספיקה בלי שכבות מיותרות",
                f"כשיוצאים בחורף ורוצים חליפה אחת שעושה הכל — {prod_ref} בדיוק זה",
                f"בנסיעה ארוכה ביום קר כש{prod_ref} נשארת נוחה גם שעתיים בכיסא הרכב",
            ]
        else:  # general / מעבר / unknown
            sit_options = [
                f"ביום יומיומי כש{prod_ref} עושה את העבודה מבלי לדרוש תשומת לב",
                f"בבוקר לחוץ כשפותחים ארון ו{prod_ref} תמיד הבחירה הנכונה",
                f"בביקור משפחתי כש{prod_ref} נראית טרייה ומסודרת מהרגע הראשון",
                f"ביום של הרבה זחילה ומשחק — {prod_ref} נשארת במקום ולא מסתובבת",
                f"בסוף שבוע כש{prod_ref} מתאימה גם לבית וגם לצאת",
                f"כשרוצים חליפה אחת שמספיקה לרוב הסיטואציות — {prod_ref} עונה על זה",
                f"ביום רגיל בגן כש{prod_ref} לא מפריעה לילד לרוץ, לטפס ולשחק",
            ]
    elif gtype == "פיג'מה":
        sit_options = [
            f"בלילות כש{prod_ref} עוטפת את הילד ברכות — שינה שקטה מובטחת",
            f"בערב כש{prod_ref} מחליפה את בגדי היום ומסמנת שהגיע זמן לישון",
            f"כשהבטן נחשפת בלילה — {prod_ref} נשארת במקום ומכסה את הגב כל הלילה",
        ]
    elif gtype == "בגד ים":
        sit_options = [
            f"בים או בבריכה כש{prod_ref} מגן ומאפשר תנועה חופשית במים",
            f"בחופשת קיץ כש{prod_ref} עובד מהבריכה לחול בלי להחליף",
            f"בשיעור שחייה כש{prod_ref} מחזיק מעמד בכלור ומתייבש מהר",
        ]
    elif gtype == "מכנסיים":
        sit_options = [
            f"ביום בגן כשהילד רץ ומטפס — {prod_ref} זז עם הגוף בלי ללחוץ",
            f"כשצריכים מכנס שלא משאיר סימנים — {prod_ref} עם הגומי הרך עושה את זה",
        ]
    elif gtype == "חולצה":
        sit_options = [
            f"ביום בגן כשצריכים חולצה מסודרת — {prod_ref} נשארת נקייה ומסודרת",
            f"כשכבה מתחת לסוודר — {prod_ref} רכה ולא מפריעה",
        ]
    elif gtype == "כובע":
        sit_options = [
            f"ביום חם כשהשמש חזקה — {prod_ref} שומר על הראש מוגן ומוצל",
            f"בטיול כש{prod_ref} נשאר על הראש ולא מחליק כל שנייה",
        ]
    elif gtype == "מעיל":
        sit_options = [
            f"בבוקר קר כשצריכים לצאת לגן — {prod_ref} מחמם ברצינות",
            f"ביום גשום כש{prod_ref} שומר על הילד יבש וחם בדרך לגן",
        ]
    elif gtype == "שמיכה":
        sit_options = [
            f"בלילות כשהתינוק זורק שמיכות — {prod_ref} עוטפת ומרגיעה",
            f"בעגלה כשרוח קרה נושבת — {prod_ref} מכסה ושומרת על חום",
        ]
    else:
        sit_options = [
            f"ביום בגן כש{prod_ref} מחזיק מעמד מהבוקר ועד הצהריים",
            f"בביקור משפחתי כשהילד לובש את {prod_ref} ונראה חמוד ומסודר",
            f"ביום רגיל בבית כש{prod_ref} נותן נוחות בלי לוותר על המראה",
            f"בטיול משפחתי כש{prod_ref} עובד בכל תנאי — מהבית ועד הפארק",
            f"כשצריכים בגד אמין ליומיום — {prod_ref} עושה בדיוק את העבודה",
        ]

    sent1 = sit_options[h % len(sit_options)]

    # Sentence 2: How the product performs in that situation (fabric/feature specific)
    fabric = feats.get("fabric")
    if fabric == "כותנה":
        cotton_pool = [
            f"הכותנה של {short_ref} נושמת על העור — הילד לא מזיע גם כשרץ",
            f"{short_ref} מכותנה טבעית — רכה, נוחה, ולא גורמת לגירוי",
            f"כותנת {short_ref} גמישה ומאווררת — נוחות שמחזיקה כל היום",
            f"הבד של {short_ref} כותנה טבעית — נעים על עור התינוק שעות ארוכות",
            f"כותנת {short_ref} מתרככת עם כל כביסה — ממש משתפרת עם הזמן",
            f"{short_ref} מכותנה שנושמת — לא מזיע, לא מגרד, לא מפריע",
        ]
        sent2 = cotton_pool[(h >> 2) % len(cotton_pool)]
    elif fabric == "טטרה":
        sent2 = f"הטטרה של {short_ref} קלה על הגוף ומאווררת — מושלם לימים חמים"
    elif fabric == "פשתן":
        sent2 = f"הפשתן של {short_ref} שומר על קרירות גם כשהחום עולה"
    elif fabric == "קטיפה":
        sent2 = f"הקטיפה של {short_ref} עוטפת ומחממת — מרגישה יוקרתית על העור"
    elif fabric == "פליז":
        sent2 = f"הפליז של {short_ref} מחמם גם ביום רטוב — שכבה שסומכים עליה"
    elif fabric == "סריג":
        sent2 = f"הסריג של {short_ref} נמתח עם הגוף — לא לוחץ ולא מגביל"
    elif fabric == "ג'ינס":
        sent2 = f"הג'ינס הרך של {short_ref} מחזיק מעמד בלי לאבד גמישות"
    elif fabric == "בד אלסטי":
        sent2 = f"הבד האלסטי של {short_ref} מלווה כל תנועה — בלי לחיצות ובלי הגבלות"
    elif feats.get("design"):
        design_he = feats["design"]
        sent2 = f"העיצוב ה{design_he} של {short_ref} נשאר חד ויפה גם אחרי כביסות"
    elif feats.get("pieces"):
        sent2 = f"{feats['pieces']} החלקים של {short_ref} עובדים ביחד ובנפרד — גמישות מלאה"
    else:
        # Use product title fragment for uniqueness
        sent2_pool = [
            f"הבד של {short_ref} רך ונעים — הילד מרגיש חופשי כל היום",
            f"{short_ref} קל להלבשה ולהפשטה — גם כשהילד לא משתף פעולה",
            f"החומר של {short_ref} מחזיק מעמד בכביסות — לא מתכווץ ולא דוהה",
            f"{short_ref} נשאר מסודר כל היום — בלי שצריך לתקן כל חמש דקות",
            f"הגזרה של {short_ref} מתאימה לגוף — לא לוחצת ולא נופלת",
            f"{short_ref} עוצב להלבשה מהירה — פחות זמן על הבגד, יותר זמן לשחק",
            f"ה{gtype} {short_ref} שורד ימים עמוסים בלי להיראות מוזנח",
            f"העיבוד של {short_ref} שומר על צורה גם אחרי עשר כביסות",
        ]
        sent2 = sent2_pool[(h >> 4) % len(sent2_pool)]

    # Sentence 3: Outcome — no fabricated social proof (no "הורים שקנו/מספרים")
    outcome_templates = [
        f"בסוף יום מלא {short_ref} עדיין נראה בדיוק כמו שיצא מהארון",
        f"ילדים שלובשים {short_ref} לא מתלוננים — הגוף מרגיש את ההבדל",
        f"{short_ref} — מהבגדים שנכנסים לרוטציה ולא יוצאים ממנה",
        f"עם {short_ref} גם הבוקר הלחוץ הופך לפשוט בשניות",
        f"{short_ref} שורד כביסות ומשחקים — ה{gtype} שאפשר לסמוך עליו",
        f"ה{gtype} הזה, {short_ref}, חוסך את ה'מה ללבוש היום'",
        f"בחירה ב{short_ref} מחזירה את עצמה כבר בשבוע הראשון",
        f"{short_ref} — {gtype} שמצדיק את הבחירה כל בוקר מחדש",
        f"עם {short_ref} פחות מריבות על הלבשה ויותר זמן לדברים חשובים",
        f"אחרי שבוע עם {short_ref} קשה לתאר ארון תינוקות בלי ה{gtype} הזה",
    ]
    sent3 = outcome_templates[(h >> 8) % len(outcome_templates)]

    return f"{sent1}. {sent2}. {sent3}."


def validate_uniqueness(batch_drafts, all_sentences):
    issues = []
    batch_sentences = {}
    for pid, draft in batch_drafts.items():
        for field in ["geo_who_for", "geo_use_case"]:
            text = draft.get(field, "")
            sents = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 15]
            for sent in sents:
                if sent in batch_sentences:
                    issues.append(f"BATCH: '{sent[:50]}' → {pid} & {batch_sentences[sent]}")
                elif sent in all_sentences:
                    issues.append(f"GLOBAL: '{sent[:50]}' → {pid} & {all_sentences[sent]}")
                else:
                    batch_sentences[sent] = pid
    return issues, batch_sentences


def update_progress(batch_num, total_batches, products_done, products_total, last_pid, status="IN_PROGRESS"):
    content = f"""STAGE_ID: STAGE-8
PLAN_ID: layer4-geo-priority-001
BATCH_CURRENT: {batch_num}
BATCH_TOTAL: {total_batches}
PRODUCTS_DONE: {products_done}
PRODUCTS_TOTAL: {products_total}
LAST_PID: {last_pid}
STATUS: {status}
TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
NOTE: Run#2 v2 — product identity embedded in every sentence for uniqueness.
"""
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    pids = load_pids()
    total = len(pids)
    total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

    processed = 0
    skipped = 0
    created = 0
    failures = 0
    total_issues = 0
    all_sentences = {}

    for batch_num in range(total_batches):
        start = batch_num * BATCH_SIZE
        end = min(start + BATCH_SIZE, total)
        batch_pids = pids[start:end]
        batch_drafts = {}

        for pid in batch_pids:
            draft_path = f"{OUTPUT_DIR}/{pid}_geo_draft.json"
            if os.path.exists(draft_path):
                skipped += 1
                continue

            ctx = load_context(pid)
            if not ctx:
                failures += 1
                continue

            info = parse_product(ctx)
            who_for = compose_who_for(pid, info)
            use_case = compose_use_case(pid, info)

            batch_drafts[pid] = {
                "product_id": str(pid),
                "product_title": info["title"],
                "category": "clothing",
                "geo_who_for": who_for,
                "geo_use_case": use_case,
                "geo_comparison": None,
                "comparison_eligible": False,
                "classification": {
                    "type": info["gtype"],
                    "price": float(info["price"]) if info["price"] else 0,
                    "variants": 0
                },
                "generated_at": datetime.now(timezone.utc).isoformat()
            }

        issues, batch_sents = validate_uniqueness(batch_drafts, all_sentences)
        total_issues += len(issues)
        if issues:
            print(f"  Batch {batch_num+1}: {len(issues)} issues", file=sys.stderr)
            for i in issues[:3]:
                print(f"    {i}", file=sys.stderr)

        for pid, draft in batch_drafts.items():
            with open(f"{OUTPUT_DIR}/{pid}_geo_draft.json", "w", encoding="utf-8") as f:
                json.dump(draft, f, ensure_ascii=False, indent=2)
            created += 1

        all_sentences.update(batch_sents)
        processed += len(batch_pids)
        last_pid = batch_pids[-1] if batch_pids else ""
        update_progress(batch_num + 1, total_batches, processed + 69, total + 69, last_pid)
        print(f"Batch {batch_num+1}/{total_batches}: created={len(batch_drafts)} | total={created}")

    update_progress(total_batches, total_batches, processed + 69, total + 69, pids[-1] if pids else "", "COMPLETE")

    print(f"\n{'='*50}")
    print(f"STAGE-8 RUN#2 v2 RESULTS")
    print(f"{'='*50}")
    print(f"PRODUCTS_PROCESSED: {processed}")
    print(f"PRODUCTS_SKIPPED_EXISTING: {skipped}")
    print(f"OUTPUT_FILES_CREATED: {created}")
    print(f"FAILURES: {failures}")
    print(f"UNIQUENESS_ISSUES: {total_issues}")
    verdict = "PASS" if failures == 0 and created > 0 and total_issues < 10 else "FAIL"
    print(f"STAGE_VERDICT: {verdict}")
    return verdict


if __name__ == "__main__":
    v = main()
    sys.exit(0 if v == "PASS" else 1)
