# BabyMania — Higgsfield CLI Setup

Claude Code is connected to Higgsfield CLI with an active account.

## Image generation

For product images, hero images, backgrounds, ads, and ecommerce visuals, use:

```
higgsfield product-photoshoot create
```

Recommended modes:
- hero_banner
- lifestyle_scene
- product_shot

## Video generation

For general video creation, use:

```
higgsfield generate create
```

Recommended model:
- seedance_2_0

For marketing/ad video, use:
- marketing_studio_video

## Installed skills

- higgsfield-product-photoshoot — product photos, hero banners, ad visuals
- higgsfield-generate — general image/video generation
- higgsfield-marketplace-cards — product cards
- higgsfield-soul-id — consistent character / recurring identity

## Reborn doll safety note

When creating Reborn doll visuals with image reference, do not write:
"reborn doll"

Use safer wording:
"collectible vinyl doll"

Reason:
NSFW detection may incorrectly block Reborn doll reference images.

## Credits

Free plan includes 10 credits.

Before generating any image or video:
- report expected action
- ask for approval if credit usage is unclear
- do not waste credits on tests without confirmation

## Auth

If authentication is needed:

```
higgsfield auth login
```

This is usually a one-time login.

## BabyMania workflow rule

For every Higgsfield task, Claude must return:

```
SYSTEM STATE
PRODUCT STATE
ISSUES FOUND
RISK LEVEL
NEXT STEP
```

Do not generate assets without confirming:
- purpose
- format
- size
- desktop/mobile target
- product reference
- whether text should be inside the image or added later in HTML/CSS
