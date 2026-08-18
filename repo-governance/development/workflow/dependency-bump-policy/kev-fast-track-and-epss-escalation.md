---
title: "KEV Fast-Track and EPSS Escalation"
description: How a CISA KEV listing bypasses the 60-day soak and forces Path C, and how a high EPSS score flags a bump for expedited scheduling.
category: explanation
subcategory: development
tags:
  - dependencies
  - security
  - versioning
  - reproducibility
  - workflow
created: 2026-05-15
when_to_use: Use when a CVE affecting the currently pinned version might be actively exploited, to decide whether to bypass the normal Path B soak window.
---

# KEV Fast-Track and EPSS Escalation

## KEV Fast-Track — Bypass 60-Day Soak for Actively Exploited CVEs

If any unpatched CVE affecting the **currently pinned** version appears in the CISA KEV catalog,
the 60-day soak window (Path B) is **bypassed** and the bump is automatically escalated to
**Path C** (Security-Override Waiver), regardless of whether a pre-cutoff version would otherwise
have been eligible.

**Rationale**: CISA KEV membership confirms the CVE is weaponized in the wild. Waiting 60 days
for community soak is unacceptable when active exploitation is ongoing.

**Procedure when KEV Fast-Track triggers**:

1. Look up the CVE IDs affecting the current pin in the CISA KEV JSON feed.
2. If any match: treat the bump as Path C immediately.
3. Complete the Path C waiver template; additionally record the KEV `dateAdded` field, the EPSS
   score, and the `knownRansomwareCampaignUse` value (`"Known"` or `"Unknown"`).
4. Append `(KEV-listed)` to the clearance status in all tables and registers.

## EPSS Escalation — Soft Urgency Signal

If the EPSS score for an unpatched CVE is **≥ 0.5** (top ~10% by exploitation likelihood within
30 days), treat the bump with Path C urgency and flag it for expedited scheduling — even if the
CVE has not yet been added to KEV. Record the EPSS score and percentile in the clearance table
and in `tech-docs.md`.
