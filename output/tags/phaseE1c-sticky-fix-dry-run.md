# Phase E1c — Dry Run
**Mode:** live
**Status:** PASS

## Diff
```diff
--- bm-sticky-bar.liquid (before)
+++ bm-sticky-bar.liquid (after)
@@ -107,20 +107,31 @@
   var bar = document.getElementById('bm-sticky-bar');
   var stickyBtn = document.getElementById('bm-sticky-add-btn');
   var stickyPrice = document.getElementById('bm-sticky-price');
   if (!bar || !stickyBtn) return;
 
-  // Watch the product form buttons container
-  var target = document.querySelector('.product-form__buttons');
-  if (!target) return;
-
-  new IntersectionObserver(
-    function (entries) {
-      bar.setAttribute('aria-hidden', entries[0].isIntersecting ? 'true' : 'false');
-    },
-    { threshold: 0 }
-  ).observe(target);
+  // Fix: section renders before main-product in template order.
+  // DOMContentLoaded ensures .product-form__buttons exists when observer attaches.
+  function initStickyObserver() {
+    var target = document.querySelector('.product-form__buttons')
+              || document.querySelector('.product-form__submit:not(#bm-sticky-add-btn)');
+    if (!target) return;
+
+    new IntersectionObserver(
+      function (entries) {
+        var vis = entries[0].isIntersecting;
+        bar.setAttribute('aria-hidden', vis ? 'true' : 'false');
+      },
+      { threshold: 0.1 }
+    ).observe(target);
+  }
+
+  if (document.readyState === 'loading') {
+    document.addEventListener('DOMContentLoaded', initStickyObserver);
+  } else {
+    initStickyObserver();
+  }
 
   // Sync price from live DOM (updates on variant change)
   function syncPrice() {
     if (!stickyPrice) return;
     var el = document.querySelector('.price__regular .price-item--regular, .price__sale .price-item--sale');

```

## Sanity Checks
- initStickyObserver_present: ✅
- domcontent_listener_present: ✅
- readystate_check_present: ✅
- threshold_0.1_present: ✅
- old_threshold_0_absent: ✅
- old_early_return_absent: ✅
- html_unchanged: ✅
- schema_unchanged: ✅
- style_unchanged: ✅