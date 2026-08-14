---
title: "Examples"
description: Worked examples of Path A (LTS), Path B (60-day eligible), and Path C (security waiver) decisions.
category: explanation
subcategory: development
tags:
  - dependencies
  - security
  - versioning
  - reproducibility
  - workflow
created: 2026-05-15
when_to_use: Use as a reference when classifying a real bump into Path A, B, or C.
---

# Examples

## Example 1: Path A (LTS, Recent Patch)

Node.js: `package.json` `volta.node` = `"24.15.0"`. Released 2026-04-15 (30 days before the bump on 2026-05-15). LTS Krypton confirmed. CVE-clean per NVD. **Decision: keep at 24.15.0** — LTS path overrides the 60-day rule.

## Example 2: Path B (Non-LTS, Eligible Older Version)

Tailwind CSS: latest is 4.3.0 (released 2026-05-08, 7 days old). Cutoff = 2026-03-16. Latest version released on or before 2026-03-16 is 4.2.1 (released 2026-02-23). 4.2.1 is CVE-clean. **Decision: bump to 4.2.1** — skip 4.3.0; it is not eligible until 60 days have elapsed.

## Example 3: Path C (Waiver)

mermaid: latest is 11.15.0 (released 2026-05-11, 4 days old). All versions below 11.15.0 have unpatched CVE-2026-41148 (CSS injection, High 7.1) and five related CVEs. No pre-cutoff CVE-clean version exists. **Decision: waiver — pin to 11.15.0.** Justification: required for active CVE patches; 60-day rule waived per Path C.
