"""Google Gemini client for generating images and Hebrew product copy."""

from google import genai
from google.genai import types
from config.settings import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL = "gemini-2.5-flash"
IMAGE_MODEL = "gemini-2.0-flash-preview-image-generation"


def generate_product_description(product_title, product_type, tags):
    """Generate a Hebrew product description for baby clothing."""
    prompt = f"""אתה קופירייטר מקצועי לחנות בגדי תינוקות פרימיום בישראל.
כתוב תיאור מוצר בעברית עבור המוצר הבא:

שם המוצר: {product_title}
סוג: {product_type}
תגיות: {', '.join(tags) if tags else 'אין'}

התיאור צריך לכלול:
1. כותרת מושכת בתגית <h2>
2. תיאור כללי (2-3 משפטים) בתגית <p> שמדגיש נוחות, איכות וסגנון
3. רשימת יתרונות (4-5 נקודות) עם אייקונים מתאימים ברשימה <ul><li>

כתוב בטון חם, מזמין ומקצועי. השתמש בשפה שפונה להורים צעירים.
החזר רק HTML נקי, בלי markdown, בלי בלוק קוד, ובלי הסברים נוספים."""

    resp = client.models.generate_content(model=MODEL, contents=prompt)
    return resp.text


def generate_product_benefits(product_title, product_type):
    """Generate a list of product benefits in Hebrew."""
    prompt = f"""עבור מוצר תינוקות "{product_title}" מסוג "{product_type}",
כתוב בדיוק 5 יתרונות קצרים בעברית. כל יתרון בשורה נפרדת.
פורמט: אימוג'י מתאים + טקסט קצר (עד 6 מילים)
דוגמה:
🌿 עשוי מכותנה אורגנית 100%
👶 נוח ורך לעור התינוק

החזר רק את הרשימה."""

    resp = client.models.generate_content(model=MODEL, contents=prompt)
    return resp.text


def generate_product_image(product_title, product_type):
    """Generate a premium product image using Gemini image generation."""
    prompt = f"""Generate a clean, professional e-commerce product photo of a baby {product_type}
called "{product_title}". The image should have a pure white background, soft studio lighting,
and show the clothing item laid flat or on a simple display. Style: premium baby boutique,
minimal and elegant. High resolution, commercial quality."""

    resp = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        ),
    )

    # Extract image from response parts
    for part in resp.candidates[0].content.parts:
        if part.inline_data is not None:
            return part.inline_data.data, part.inline_data.mime_type

    return None, None
