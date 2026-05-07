# Shopify Auth Flow Audit

**Mode:** READ-ONLY / SECURITY SAFE
**Timestamp:** 2026-05-07T09:01:53.681428+00:00

## VERDICT: ENV_SOURCE_FOUND_VALID_TOKEN

## Auth Flow Found

| Field | Value |
|-------|-------|
| Flow | client_credentials OAuth |
| Endpoint | POST /admin/oauth/access_token |
| File | shopify_client.py |
| Config | config/settings.py |
| Credentials | SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET |
| Token TTL | ~24h (86399s) |
| Admin API | YES |
| Products write | YES |
| Browser required | NO |

## Connectivity Test

- client_credentials POST: **HTTP 200** — token  obtained
- GET product 10011383071033: **HTTP 200** — title verified

## Static Tokens (INVALID)

- Desktop : HTTP 401 — revoked/expired
- Project : HTTP 401 — revoked/expired

## Batch9 Scripts Updated

-  — now calls  at startup
-  — same

## Safe Next Command

