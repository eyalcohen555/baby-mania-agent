import os
from dotenv import load_dotenv

# Load project .env first (SHOPIFY_SHOP_URL, GEMINI_API_KEY, etc.)
load_dotenv()
# Override token credentials from the secure desktop .env
load_dotenv(r"C:\Users\3024e\Desktop\shopify-token\.env", override=True)

SHOPIFY_SHOP_URL = os.getenv("SHOPIFY_SHOP_URL")
SHOPIFY_CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID")
SHOPIFY_CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Shopify API version
SHOPIFY_API_VERSION = "2024-10"

# Baby clothing size chart (Israeli market standard)
SIZE_CHART = {
    "0-3M": {"age": "0-3 חודשים", "height_cm": "50-62", "weight_kg": "3-6"},
    "3-6M": {"age": "3-6 חודשים", "height_cm": "62-68", "weight_kg": "6-8"},
    "6-12M": {"age": "6-12 חודשים", "height_cm": "68-80", "weight_kg": "8-10"},
    "12-18M": {"age": "12-18 חודשים", "height_cm": "80-86", "weight_kg": "10-12"},
    "18-24M": {"age": "18-24 חודשים", "height_cm": "86-92", "weight_kg": "12-14"},
    "2-3Y": {"age": "2-3 שנים", "height_cm": "92-98", "weight_kg": "14-16"},
}

# ─── BabyMania Template Configuration ───────────────────────────────────────

# Metafield namespace used across all BabyMania product pages
METAFIELD_NAMESPACE = "baby_mania"

# Sections connected to the product page template
# סקשנים מ-product.json (Shopify theme 2.0)
TEMPLATE_SECTIONS = [
    "product-hero",        # תמונה ראשית, שם מוצר, מחיר
    "color-selector",      # בורר צבעים
    "size-selector",       # בורר מידות
    "stock-bar",           # פס מלאי (Low / In Stock / Out)
    "product-gallery",     # גלריית thumbnails
    "product-details",     # פרטי המוצר (חומר, טיפול, מידות)
    "whatsapp-button",     # כפתור WhatsApp לייעוץ
    "related-products",    # מוצרים דומים
    # ── סקשנים חדשים (theme/sections/bm-store-*.liquid) ──
    "bm-store-fabric",     # סיפור הבד — קורא מ-baby_mania.fabric_story
    "bm-store-benefits",   # יתרונות — קורא מ-baby_mania.benefits
    "bm-store-sizes",      # מדריך מידות — נגזר מ-product variants
    "bm-store-care",       # טיפול ומפרט — קורא מ-baby_mania.care_instructions
    "bm-store-faq",        # שאלות נפוצות — קורא מ-baby_mania.faq
    "bm-store-urgency",    # דחיפות מלאי — קורא מ-baby_mania.stock_level/units_left
    "bm-store-contact",    # WhatsApp CTA — קורא מ-baby_mania.whatsapp_number/message
]

# Mapping: section → metafield key(s) it reads
SECTION_METAFIELD_MAP = {
    "product-hero": [
        f"{METAFIELD_NAMESPACE}.subtitle",        # כותרת משנה (סקנדינבי/אורגני וכו')
        f"{METAFIELD_NAMESPACE}.badge_text",      # תווית על התמונה (NEW / SALE)
    ],
    "color-selector": [
        f"{METAFIELD_NAMESPACE}.available_colors",  # רשימת צבעים זמינים (JSON)
        f"{METAFIELD_NAMESPACE}.color_images",      # מיפוי צבע → URL תמונה (JSON)
    ],
    "size-selector": [
        f"{METAFIELD_NAMESPACE}.available_sizes",   # מידות זמינות לפי SKU (JSON)
        f"{METAFIELD_NAMESPACE}.size_guide_url",    # קישור לטבלת מידות
    ],
    "stock-bar": [
        f"{METAFIELD_NAMESPACE}.stock_level",       # "low" | "in_stock" | "out_of_stock"
        f"{METAFIELD_NAMESPACE}.units_left",        # מספר יחידות שנותרו (אופציונלי)
    ],
    "product-gallery": [
        f"{METAFIELD_NAMESPACE}.gallery_images",    # רשימת URL תמונות נוספות (JSON)
    ],
    "product-details": [
        f"{METAFIELD_NAMESPACE}.material",          # הרכב בד (e.g. "100% כותנה אורגנית")
        f"{METAFIELD_NAMESPACE}.care_instructions", # הוראות כביסה
        f"{METAFIELD_NAMESPACE}.country_of_origin", # ארץ ייצור
    ],
    "whatsapp-button": [
        f"{METAFIELD_NAMESPACE}.whatsapp_number",   # מספר ווטסאפ לייעוץ
        f"{METAFIELD_NAMESPACE}.whatsapp_message",  # הודעה ברירת מחדל (אופציונלי)
    ],
    "related-products": [
        f"{METAFIELD_NAMESPACE}.related_product_ids",  # IDs של מוצרים קשורים (JSON)
    ],
    # ── Shopify Liquid sections (theme/sections/bm-store-*.liquid) ──
    "bm-store-fabric": [
        f"{METAFIELD_NAMESPACE}.fabric_story",         # JSON: { title, dream, body, tags }
    ],
    "bm-store-benefits": [
        f"{METAFIELD_NAMESPACE}.benefits",             # JSON array: [{ icon, title, desc, chain }]
    ],
    "bm-store-sizes": [
        f"{METAFIELD_NAMESPACE}.size_guide_url",       # קישור למדריך מידות חיצוני (אופציונלי)
    ],
    "bm-store-care": [
        f"{METAFIELD_NAMESPACE}.care_instructions",    # JSON: { material, closure, items:[{icon,text}] }
    ],
    "bm-store-faq": [
        f"{METAFIELD_NAMESPACE}.faq",                  # JSON array: [{ question, answer }]
    ],
    "bm-store-urgency": [
        f"{METAFIELD_NAMESPACE}.stock_level",          # "low" | "in_stock" | "out_of_stock"
        f"{METAFIELD_NAMESPACE}.units_left",           # מספר יחידות שנותרו (אופציונלי)
    ],
    "bm-store-contact": [
        f"{METAFIELD_NAMESPACE}.whatsapp_number",      # מספר ווטסאפ (ספרות בלבד)
        f"{METAFIELD_NAMESPACE}.whatsapp_message",     # הודעת פתיחה ל-WA (אופציונלי)
    ],
}
