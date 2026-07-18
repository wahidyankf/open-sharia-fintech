---
title: "Artifact: Pruned vs. Unpruned Context Session"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 44
---

> The same question asked once with ten files loaded and once pruned to the three actually
> relevant -- exercises co-04.

```text
UNPRUNED SESSION -- 10 files loaded
------------------------------------
checkout.py, calculate_total.py, discount_rules.py, test_checkout.py,
marketing_banner.tsx, homepage.tsx, analytics.py, README.md, CHANGELOG.md,
deploy.yml

Answer given: "...this may relate to promotional banner logic in
marketing_banner.tsx, which also references a $500 threshold for
free-shipping banner display..."

PRUNED SESSION -- 3 files loaded
----------------------------------
checkout.py, discount_rules.py, test_checkout.py

Answer given: "discount_rules.py caps the combined discount at $500
(MAX_DISCOUNT_CAP = 500); orders whose subtotal after discount exceeds
that cap raise a ValueError in checkout.py's finalize_order(), which is
exactly what's failing."
```

**Verify**: the pruned run's answer cites only `discount_rules.py` and `checkout.py` -- both
genuinely relevant to the failure -- and states the actual mechanism (`MAX_DISCOUNT_CAP = 500`),
while the unpruned run's answer cites `marketing_banner.tsx`, a file with no relationship to
checkout logic at all -- satisfying ex-04's rule that the pruned run stays on-topic while the
unpruned run cites an irrelevant file.
