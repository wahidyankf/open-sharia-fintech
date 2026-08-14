---
title: "Example: UI Feature Verification (multi-locale app)"
description: "A worked example of manually verifying a UI feature across locales."
category: explanation
subcategory: development
tags:
  - verification
  - testing
  - playwright
  - api
  - quality
  - manual-testing
created: 2026-04-04
when_to_use: "Use for a concrete example of multi-locale UI verification."
---

# Example: UI Feature Verification (multi-locale app)

```
For each locale in ["en", "id"]:
  For each breakpoint in [375, 768, 1280]:
    1. browser_resize(breakpoint, 900)
    2. browser_navigate("http://localhost:3200/{locale}/products")
    3. browser_snapshot() -- confirm product list renders with correct language
    4. browser_take_screenshot() -- save to evidence/phase-N-products-{locale}-{breakpoint}px.png
    5. browser_console_messages() -- confirm no errors
    6. browser_network_requests() -- confirm API calls succeed

After all locales/breakpoints:
  7. browser_click("Add Product button")
  8. browser_fill_form("Product Name", "Test Product")
  9. browser_click("Submit button")
  10. browser_snapshot() -- confirm product appears in list
  11. browser_network_requests() -- confirm POST /api/products returned 201

Record inline in delivery.md: screenshot paths, console status, network status per locale.
```
