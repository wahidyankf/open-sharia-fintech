---
title: "Examples"
description: "Worked examples of correctly captured evidence."
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
when_to_use: "Use when you need a concrete example of properly captured evidence."
---

# Examples

## PASS: Complete evidence record

```markdown
- [x] [AI] Verify salary calculator computes correctly in EN and ID — acceptance: displayed
      value matches independent computation; no console errors; all 3 breakpoints tested
  > **Evidence** (2026-06-20): Computed gross salary IDR 25,000,000/month. Independent check:
  > 25000000 / 160h = 156,250/h ✓
  >
  > - `![EN desktop](./evidence/phase-4-calc-en-1280px.png)` — value correct, no console errors
  > - `![EN mobile](./evidence/phase-4-calc-en-375px.png)` — layout intact, value correct
  > - `![ID desktop](./evidence/phase-4-calc-id-1280px.png)` — value correct, thousands separator "." ✓
  > - `![ID mobile](./evidence/phase-4-calc-id-375px.png)` — layout intact
```

## FAIL: Evidence missing

```markdown
- [x] [AI] Verify salary calculator works — verified manually ✓
```

Missing: no screenshot, no locale coverage, no computation check, no console-error check.
`plan-execution-checker` would flag this as HIGH.

## FAIL: Locale coverage incomplete

```markdown
- [x] [AI] Verify tools page — `![EN desktop](./evidence/phase-3-tools-en-1280px.png)` ✓
```

Missing: ID locale not verified. `plan-execution-checker` would flag this as HIGH if the app
supports Indonesian.
