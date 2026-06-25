(function () {
  const KEY = 'bm_gift_ok';

  // =========================
  // 🎁 GIFT VARIANT IDS
  // =========================
  const GIFT_VARIANT_IDS = [

    // כובע חורף דובי
    51300721983801,
    51300721983848,
    51300721983802,
    51300721983806,
    51300721983811,
    51300721983807,
    51300721983810,
    51300721983809,
    51300721983812,

    // מגבת מתנה
    513028069869,

    // חזיית הנקה
    513028064847,
    513028064851,
    513028064849,
    513028064853,
    513028064856,
    513028064859,
    513028064862,
    513028064865,

    // מצלמה לילדים
    51667276851669,

    // משקפי שמש
    47389275786841,
    47389275786909,
    47389275786809
  ];

  // =========================
  // אישור חד פעמי להוספת מתנה
  // =========================
  window.BabyManiaAllowGiftAdd = function () {
    try {
      sessionStorage.setItem(KEY, '1');
    } catch (e) {}
  };

  const originalFetch = window.fetch;

  function getVariantId(body, init) {
    try {
      if (!body) return null;

      const contentType =
        (init?.headers?.get && init.headers.get('Content-Type')) ||
        init?.headers?.['Content-Type'] ||
        '';

      // JSON
      if (typeof body === 'string' && contentType.includes('application/json')) {
        const obj = JSON.parse(body);
        if (obj?.id) return Number(obj.id);
      }

      // URL encoded
      if (typeof body === 'string') {
        const match = body.match(/(?:^|&)id=(\d+)/);
        return match ? Number(match[1]) : null;
      }

      // URLSearchParams
      if (body instanceof URLSearchParams) {
        const id = body.get('id');
        return id ? Number(id) : null;
      }

      // FormData
      if (body instanceof FormData) {
        const id = body.get('id');
        return id ? Number(id) : null;
      }

      return null;
    } catch {
      return null;
    }
  }

  function isGiftByProperties(body) {
    if (!body) return false;

    if (typeof body === 'string') {
      return (
        body.includes('properties[gift]') ||
        body.includes('properties[threshold_offer]') ||
        body.includes('properties[_threshold_offer]') ||
        body.includes('properties%5Bgift%5D') ||
        body.includes('properties%5Bthreshold_offer%5D') ||
        body.includes('properties%5B_threshold_offer%5D')
      );
    }

    if (body instanceof URLSearchParams || body instanceof FormData) {
      return (
        body.has('properties[gift]') ||
        body.has('properties[threshold_offer]') ||
        body.has('properties[_threshold_offer]')
      );
    }

    return false;
  }

  window.fetch = async function (input, init) {
    try {
      const url =
        typeof input === 'string' ? input : input?.url || '';
      const method = (init?.method || 'GET').toUpperCase();

      if (method === 'POST' && url.includes('/cart/add')) {
        const allowed = sessionStorage.getItem(KEY) === '1';
        const body = init?.body;

        const variantId = getVariantId(body, init);

        const isGiftVariant =
          typeof variantId === 'number' &&
          GIFT_VARIANT_IDS.includes(variantId);

        const isGiftProp = isGiftByProperties(body);

        // ⛔ חסימה מוחלטת ללא אישור
        if (!allowed && (isGiftVariant || isGiftProp)) {
          console.warn('Gift blocked', variantId);
          return new Response(
            JSON.stringify({ error: 'Gift blocked' }),
            {
              status: 403,
              headers: { 'Content-Type': 'application/json' }
            }
          );
        }

        // אישור חד פעמי
        if (allowed) {
          sessionStorage.removeItem(KEY);
        }
      }
    } catch {}

    return originalFetch.apply(this, arguments);
  };
})();
