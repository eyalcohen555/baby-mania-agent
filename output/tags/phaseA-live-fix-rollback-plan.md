# Phase A — Rollback Plan

**Date:** 2026-05-10 12:47:42  

## A1 Pajama Product

- **PID:** `9606694306105`
- **Restore title:** `?? ???�?? ????? ??????`
- **Restore tags:** `baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, gender-neutral, kids-clothing, neutral-baby-outfit, type-set`
- **Command:** `PUT /products/9606694306105.json`

## A2 Navigation

- **Menu ID:** `gid://shopify/Menu/250909851961`
- **Restore:** Execute GraphQL menuUpdate with `restore_items` from output/tags/phaseA-live-fix-backup.json

## A3 occ-gift Collection

- **ID:** `526691860793`
- **Restore title:** `מתנות לתינוק`
- **Command:** `PUT /smart_collections/526691860793.json`

## A4 PID 9096636825913

- **PID:** `9096636825913`
- **Restore tags:** ``
- **Command:** `PUT /products/9096636825913.json`

## A5 PID 9605887689017

READ-ONLY — no rollback needed.
