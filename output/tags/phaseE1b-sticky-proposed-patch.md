# Phase E1b — Sticky Add-to-Cart Proposed Patch
**Date:** 2026-05-10 | **Mode:** PATCH PLAN ONLY — not applied
**Tier:** T2 | **File:** sections/bm-sticky-bar.liquid
**Status:** AWAITING T2 APPROVAL

---

## Root Cause (1 sentence)

The sticky script is a non-deferred inline `<script>` that runs before the `main-product` section renders, so `.querySelector('.product-form__buttons')` returns null and the function exits early — the IntersectionObserver is never created.

---

## Option A — Recommended Fix (DOM timing fix)

**Change:** Replace the hard `if (!target) return` exit with a DOMContentLoaded-aware init function.
**Lines changed:** ~8 lines in the JS block. No HTML. No CSS. No schema.

### BEFORE (current broken code)

```javascript
// Watch the product form buttons container
var target = document.querySelector('.product-form__buttons');
if (!target) return;

new IntersectionObserver(
    function (entries) {
        bar.setAttribute('aria-hidden', entries[0].isIntersecting ? 'true' : 'false');
    },
    { threshold: 0 }
).observe(target);
```

### AFTER (proposed patch)

```javascript
// Fix: sticky section renders before main-product, so we must defer until DOM ready.
function initStickyObserver() {
    var target = document.querySelector('.product-form__buttons')
              || document.querySelector('.product-form__submit:not(#bm-sticky-add-btn)');
    if (!target) return;

    new IntersectionObserver(
        function (entries) {
            var vis = entries[0].isIntersecting;
            bar.setAttribute('aria-hidden', vis ? 'true' : 'false');
        },
        { threshold: 0.1 }
    ).observe(target);
}

// If DOM is still parsing (section renders before main-product), wait for DOMContentLoaded.
// If DOM is already ready (edge cases, test environments), run immediately.
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStickyObserver);
} else {
    initStickyObserver();
}
```

### What changes and why

| Change | Reason |
|--------|--------|
| Wrap observer setup in `initStickyObserver()` | Allows deferred call |
| `readyState === 'loading'` check | True when script runs before DOM complete |
| `DOMContentLoaded` listener | Fires after all sections parsed → `.product-form__buttons` exists |
| Fallback `initStickyObserver()` in else | Handles edge case where DOM already ready |
| `.product-form__submit:not(#bm-sticky-add-btn)` fallback | If container class changes, button class is stable |
| `threshold: 0.1` instead of `0` | Show sticky when 90% of button is gone (slightly better UX) |

### Full patched JS block (drop-in replacement)

```javascript
<script>
(function () {
  var bar = document.getElementById('bm-sticky-bar');
  var stickyBtn = document.getElementById('bm-sticky-add-btn');
  var stickyPrice = document.getElementById('bm-sticky-price');
  if (!bar || !stickyBtn) return;

  function initStickyObserver() {
    var target = document.querySelector('.product-form__buttons')
              || document.querySelector('.product-form__submit:not(#bm-sticky-add-btn)');
    if (!target) return;

    new IntersectionObserver(
      function (entries) {
        var vis = entries[0].isIntersecting;
        bar.setAttribute('aria-hidden', vis ? 'true' : 'false');
      },
      { threshold: 0.1 }
    ).observe(target);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStickyObserver);
  } else {
    initStickyObserver();
  }

  // Sync price from live DOM (updates on variant change)
  function syncPrice() {
    if (!stickyPrice) return;
    var el = document.querySelector('.price__regular .price-item--regular, .price__sale .price-item--sale');
    if (el) stickyPrice.textContent = el.textContent.trim();
  }
  syncPrice();

  var priceContainer = document.querySelector('.price');
  if (priceContainer) {
    new MutationObserver(syncPrice).observe(priceContainer, {
      childList: true, subtree: true, characterData: true
    });
  }

  // Click: add to cart via fetch (variant ID from the live form input)
  stickyBtn.addEventListener('click', function () {
    var variantInput = document.querySelector(
      'input[name="id"].product-variant-id, product-form input[name="id"], form[action*="/cart/add"] input[name="id"]'
    );
    if (!variantInput) return;

    var variantId = variantInput.value;
    var qty = 1;
    var qtyInput = document.querySelector('.quantity__input');
    if (qtyInput && parseInt(qtyInput.value, 10) > 0) {
      qty = parseInt(qtyInput.value, 10);
    }

    stickyBtn.disabled = true;
    var originalText = stickyBtn.textContent;
    stickyBtn.textContent = '...';

    fetch('/cart/add.json', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
      body: JSON.stringify({ id: variantId, quantity: qty })
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.status) {
          stickyBtn.textContent = originalText;
          stickyBtn.disabled = false;
          return;
        }
        fetch('/cart.js')
          .then(function (r) { return r.json(); })
          .then(function (cart) {
            document.querySelectorAll('.cart-count-bubble span[aria-hidden]').forEach(function (el) {
              el.textContent = cart.item_count;
            });
            document.querySelectorAll('.cart-count-bubble span:not([aria-hidden])').forEach(function (el) {
              el.textContent = cart.item_count + ' items';
            });
            document.dispatchEvent(new CustomEvent('cart:refresh', { bubbles: true }));
          });

        stickyBtn.textContent = '✓ נוסף!';
        setTimeout(function () {
          stickyBtn.textContent = originalText;
          stickyBtn.disabled = false;
        }, 1800);
      })
      .catch(function () {
        stickyBtn.textContent = originalText;
        stickyBtn.disabled = false;
      });
  });
}());
</script>
```

---

## Option B — Always Show After Scroll (simpler, less accurate)

```javascript
// Mobile-only: show sticky after scrollY > 250px
if (window.innerWidth <= 768) {
    window.addEventListener('scroll', function () {
        var scrolled = window.scrollY || window.pageYOffset;
        if (scrolled > 250) {
            bar.setAttribute('aria-hidden', 'false');
        } else {
            bar.setAttribute('aria-hidden', 'true');
        }
    }, { passive: true });
} else {
    // Desktop: use IntersectionObserver with timing fix (Option A logic)
    // ...
}
```

**Not recommended** — less accurate UX (shows sticky even when ATC button is still visible).

---

## Deployment Checklist (when approved)

- [ ] T2 approval from Ayal
- [ ] Backup current `sections/bm-sticky-bar.liquid` to `output/tags/phaseE1b-sticky-bar-backup.liquid`
- [ ] Apply Option A patch via Shopify Admin → Themes → Code editor (or theme API PUT)
- [ ] Test on live clothing product: scroll down → sticky appears → click button → item added to cart
- [ ] Test on desktop: no regression
- [ ] Test on EasySleep (should still NOT work — different T3 issue)
- [ ] Commit change files + output report

---

## EasySleep / Tempio (still needs separate T3 fix)

Even after applying Option A, EasySleep and Tempio will still be broken:
- At DOMContentLoaded, main-product is disabled → form not rendered → `.product-form__buttons` = null
- Fix requires T3: enable main-product section in both templates (with care for layout conflicts)
