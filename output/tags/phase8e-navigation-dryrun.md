# Phase 8E — Navigation Dry Run

**Date:** 2026-05-05 15:27:25  
**Shop:** a2756c-c0.myshopify.com  
**Type:** DRY RUN — no mutation, no writes to Shopify  
**Token suffix:** `d666`  

---

## 1. מצב מערכת

| Item | Status |
|------|--------|
| Phase 8C | ✅ COMPLETE — 5 Smart Collections LIVE |
| Phase 8D | ✅ COMPLETE — Navigation Plan ready |
| Phase 8E scope (GraphQL read) | ✅ WORKS |
| main-menu נקרא | ✅ כן |
| Navigation שונה | ✅ לא — שום שינוי |
| Mega Menu | ✅ לא — לא יצור |
| Product tags שינוי | ✅ לא |
| Smart Collections live | ✅ 5 |

---

## 2. main-menu Snapshot (קריאה בלבד)

| Field | Value |
|-------|-------|
| GID | `gid://shopify/Menu/250909851961` |
| Handle | `main-menu` |
| Title | `תפריט` |
| Item count | 18 |

### פריטים קיימים:

| # | Title | URL | Type | Resource | Nested |
|---|-------|-----|------|----------|--------|
| 1 | דף הבית | `/` | FRONTPAGE | — | 0 |
| 2 | בגדי חורף | `/collections/%D7%91%D7%92%D7%93%D7%99-%D7%97%D7%95%D7%A8%D7%A3-1` | COLLECTION | gid://shopify/Collection/486381617465 | 0 |
| 3 | קיץ 2026 | `/collections/summer-2024` | COLLECTION | gid://shopify/Collection/473261211961 | 0 |
| 4 | כל המוצרים | `/collections/all` | CATALOG | — | 0 |
| 5 | בובת ריבורן | `/collections/reborn/%D7%91%D7%95%D7%91%D7%AA-%D7%A8%D7%99%D7%91%D7%95%D7%A8%D7%9F` | COLLECTION | gid://shopify/Collection/526156103993 | 0 |
| 6 | בגדי בנות | `/collections/%D7%91%D7%92%D7%93%D7%99-%D7%91%D7%A0%D7%95%D7%AA` | COLLECTION | gid://shopify/Collection/482519155001 | 0 |
| 7 | בגדי בנים | `/collections/%D7%91%D7%92%D7%93%D7%99-%D7%91%D7%A0%D7%99%D7%9D` | COLLECTION | gid://shopify/Collection/482519187769 | 0 |
| 8 | מוצרי בטיחות | `/collections/%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%91%D7%98%D7%99%D7%97%D7%95%D7%AA` | COLLECTION | gid://shopify/Collection/472982094137 | 0 |
| 9 | משחקים לתינוק | `/collections/%D7%9E%D7%A9%D7%97%D7%A7%D7%99%D7%9D-%D7%9C%D7%AA%D7%99%D7%A0%D7%95%D7%A7` | COLLECTION | gid://shopify/Collection/472981733689 | 0 |
| 10 | נעלי ילדים | `/collections/%D7%A0%D7%A2%D7%9C%D7%99%D7%99%D7%9D` | COLLECTION | gid://shopify/Collection/471568613689 | 0 |
| 11 | שמיכות עיטוף ושקי שינה | `/collections/%D7%A9%D7%9E%D7%99%D7%9B%D7%95%D7%AA-%D7%A2%D7%99%D7%98%D7%95%D7%A3-%D7%95%D7%A9%D7%A7%D7%99-%D7%A9%D7%99%D7%A0%D7%94` | COLLECTION | gid://shopify/Collection/471568580921 | 0 |
| 12 | תיקי החתלה | `/collections/%D7%AA%D7%99%D7%A7%D7%99-%D7%94%D7%97%D7%AA%D7%9C%D7%94` | COLLECTION | gid://shopify/Collection/471568548153 | 0 |
| 13 | לידה ואביזרים נלווים | `/collections/%D7%9C%D7%99%D7%93%D7%94-%D7%95%D7%90%D7%91%D7%99%D7%96%D7%A8%D7%99%D7%9D-%D7%A0%D7%9C%D7%95%D7%95%D7%99%D7%9D` | COLLECTION | gid://shopify/Collection/481499283769 | 0 |
| 14 | בלוג | `/blogs/news` | BLOG | gid://shopify/Blog/109164036409 | 0 |
| 15 | עיצוב וטקסטיל לחדרי ילדים | `/collections/%D7%A2%D7%99%D7%A6%D7%95%D7%91-%D7%95%D7%98%D7%A7%D7%A1%D7%98%D7%99%D7%9C-%D7%9C%D7%97%D7%93%D7%A8%D7%99-%D7%99%D7%9C%D7%93%D7%99%D7%9D` | COLLECTION | gid://shopify/Collection/481499414841 | 0 |
| 16 | מארזי מתנה | `/collections/%D7%9E%D7%90%D7%A8%D7%96%D7%99-%D7%9E%D7%AA%D7%A0%D7%94` | COLLECTION | gid://shopify/Collection/471568646457 | 0 |
| 17 | המיוחדים שלנו | `/collections/%D7%94%D7%9E%D7%99%D7%95%D7%97%D7%93%D7%99%D7%9D-%D7%A9%D7%9C%D7%A0%D7%95` | COLLECTION | gid://shopify/Collection/477318185273 | 0 |
| 18 | יצירת קשר | `/pages/contact` | PAGE | gid://shopify/Page/135463764281 | 0 |

---

## 3. חפיפות ישנות שנמצאו

| Title | URL | Flag |
|-------|-----|------|
| בגדי בנות | `/collections/%D7%91%D7%92%D7%93%D7%99-%D7%91%D7%A0%D7%95%D7%AA` | `remove_from_navigation_candidate` |
| בגדי בנים | `/collections/%D7%91%D7%92%D7%93%D7%99-%D7%91%D7%A0%D7%99%D7%9D` | `remove_from_navigation_candidate` |
| מארזי מתנה | `/collections/%D7%9E%D7%90%D7%A8%D7%96%D7%99-%D7%9E%D7%AA%D7%A0%D7%94` | `remove_from_navigation_candidate` |

> **הערה:** פריטים אלו מסומנים להסרה מהניווט בPhase 8F — לא למחיקת ה-collection.

---

## 4. המבנה החדש המוצע

```
בגדי תינוקות                       ← פריט ראשי חדש
├── בנות               → /collections/gender-girl
├── בנים               → /collections/gender-boy
├── סטים               → /collections/type-set
├── סרבלים ואוברולים   → /collections/type-romper
└── מתנות לתינוק       → /collections/occ-gift
```

**לא כלולים:**
- ❌ type-dress — 9 מוצרים בלבד (SEO thin)
- ❌ type-bodysuit — 8 מוצרים (HIGH SEO risk)
- ❌ Mega Menu — לא נדרש ל-5 items

---

## 5. URL Checks

| Title | URL | HTTP | תוצאה |
|-------|-----|------|--------|
| בנות | `/collections/gender-girl` | 200 | ✅ PASS |
| בנים | `/collections/gender-boy` | 200 | ✅ PASS |
| סטים | `/collections/type-set` | 200 | ✅ PASS |
| סרבלים ואוברולים | `/collections/type-romper` | 200 | ✅ PASS |
| מתנות לתינוק | `/collections/occ-gift` | 200 | ✅ PASS |

**כל הURLs תקינים:** ✅ כן

---

## 6. GraphQL Mutation Readiness

✅ Mutations נמצאו בschema:

| Mutation | Args |
|----------|------|
| `menuCreate` | title, handle, items |
| `menuDelete` | id |
| `menuUpdate` | id, title, handle, items |

> **הערה:** ביצוע mutation דורש scope `write_online_store_navigation`.
> Phase 8F יצטרך לבדוק אם scope זה זמין לפני ביצוע.

---

## 7. Rollback Plan

| שלב | פעולה |
|-----|--------|
| Backup | `current_main_menu` snapshot שמור ב-`phase8e-navigation-dryrun.json` |
| Rollback method | `menuUpdate` mutation עם הנתונים מה-snapshot |
| תוכן ה-backup | GID + handle + כל הitems הנוכחיים |
| Scope נדרש לrollback | `write_online_store_navigation` |
| אישור לפני | T3 approval מאייל לפני כל write |

---

## 8. מה ייכתב ב-Phase 8F אם יאושר (T3)

**GraphQL mutation לביצוע (לא מבוצע עכשיו):**

```graphql
# שלב 1: קריאה + backup (כבר בוצע)
# שלב 2: menuUpdate — הוסף בגדי תינוקות כ-parent עם 5 sub-items

mutation {
  menuUpdate(id: "<main-menu-gid>", input: {
    items: [
      # ... existing unrelated items ...
      { title: "בגדי תינוקות", type: HTTP, url: "#",
        items: [
          { title: "בנות",             type: COLLECTION, resourceId: "gid://shopify/Collection/526691729721" },
          { title: "בנים",             type: COLLECTION, resourceId: "gid://shopify/Collection/526691762489" },
          { title: "סטים",             type: COLLECTION, resourceId: "gid://shopify/Collection/526691795257" },
          { title: "סרבלים ואוברולים", type: COLLECTION, resourceId: "gid://shopify/Collection/526691828025" },
          { title: "מתנות לתינוק",     type: COLLECTION, resourceId: "gid://shopify/Collection/526691860793" }
        ]
      }
    ]
  }) {
    menu { id handle title }
    userErrors { field message }
  }
}
```

**ממה להימנע ב-Phase 8F:**
- ❌ לא לכלול type-dress / type-bodysuit
- ❌ לא ליצור Mega Menu
- ❌ לא לשנות פריטים קיימים שאין להם חפיפה
- ❌ לא למחוק collections ישנות — רק להסיר מהניווט

---

## 9. אישור שלא נכתב ל-Shopify

**NONE.** כל הפעולות היו GraphQL queries (read-only) + HTTP GET לבדיקת URLs.
אין mutation. אין PUT. אין POST. אין DELETE.

---

## 10. Summary

| Item | תוצאה |
|------|--------|
| main-menu נקרא | ✅ כן — 18 items |
| חפיפות ישנות | 3 נמצאו |
| כל 5 URLsמחזירים 200 | ✅ כן |
| GraphQL mutation אפשרי | ✅ כן |
| נכתב ל-Shopify | ✅ שום דבר |

---

## 11. Verdict

**READY_FOR_PHASE8F_T3_APPROVAL**

Dry run הושלם בהצלחה.

**תנאים לPhase 8F:**
1. T3 approval מאייל — אישור לכתיבת ניווט
2. `write_online_store_navigation` scope — בדיקה לפני mutation
3. backup JSON שמור: `output/tags/phase8e-navigation-dryrun.json`
4. Phase 8F יבצע mutation + verify + rollback אם נדרש

---

*Report generated by scripts/phase8e_navigation_dryrun.py*