---
title: "Locale Testing Evidence Requirements"
description: "The evidence bar for locale/i18n testing across supported languages."
category: explanation
subcategory: development
tags:
  - evidence
  - testing
  - screenshots
  - plans
  - verification
  - locale
  - manual-testing
created: 2026-06-20
when_to_use: "Use when verifying a locale-sensitive feature and capturing its evidence."
---

# Locale Testing Evidence Requirements

For any plan that touches a **multilingual / multi-locale web app**, every manual verification step
MUST cover ALL supported locales — not just the default.

## How to Discover Supported Locales

```bash
# For Next.js apps: read the locale config
grep -r "locales" apps/<app-name>/src/features/i18n/ --include="*.ts" | head -10
# Or read the Next.js config
cat apps/<app-name>/next.config.ts | grep -A 5 "i18n"
```

## Required Evidence Per Locale

For each locale `L` in the app's supported locales:

1. Navigate to the locale-specific URL (e.g., `http://localhost:3101/en/tools`,
   `http://localhost:3101/id/tools`).
2. Capture a screenshot: `evidence/phase-{N}-{feature}-{L}-{breakpoint}px.png`.
3. Verify locale-specific content: correct language text, correct locale-aware formatting
   (dates, numbers, currency symbols, units).
4. Verify the `html[lang]` attribute matches the locale.
5. Verify aria-labels, page title, and meta description are in the correct language.
6. Note any missing or untranslated strings in the implementation notes.

## Locale Evidence in `delivery.md`

```markdown
- [x] [AI] Verify /tools page renders correctly in all locales — acceptance: correct language text,
      html[lang] matches locale, no untranslated strings
  > **Evidence** (2026-06-20):
  >
  > - EN: `![/en/tools desktop](./evidence/phase-3-tools-en-1280px.png)` — html lang="en", all strings translated ✓
  > - ID: `![/id/tools desktop](./evidence/phase-3-tools-id-1280px.png)` — html lang="id", all strings translated ✓
  > - EN mobile: `![/en/tools mobile](./evidence/phase-3-tools-en-375px.png)` — layout intact ✓
  > - ID mobile: `![/id/tools mobile](./evidence/phase-3-tools-id-375px.png)` — layout intact ✓
```
