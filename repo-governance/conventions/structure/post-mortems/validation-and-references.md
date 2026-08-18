---
title: "Post-Mortem Convention: Validation and References"
description: The completion checklist for a finished post-mortem, plus in-repo and industry-source references for the post-mortem convention
when_to_use: Read this when doing a final check before marking a post-mortem complete, or when looking up a source this convention is built on.
category: explanation
subcategory: conventions
tags:
  - post-mortem
  - incidents
  - blameless
  - reliability
  - structure
created: 2026-06-05
---

# Validation and References

## Validation

A post-mortem is complete when:

- [ ] File is in `docs/explanation/post-mortems/` with a valid `YYYY-MM-DD-<system>-<short-failure>.md` name
- [ ] Frontmatter includes `doc_status` field
- [ ] Metadata table present immediately after H1
- [ ] All mandatory sections present in the specified order
- [ ] Severity classified using the authoritative scale
- [ ] Timeline uses absolute timestamps with timezone
- [ ] Root Cause is distinct from Trigger
- [ ] Every P0 action item has a Ticket reference (or `—` with a note that promotion is pending)
- [ ] No secret values in any field — placeholders used throughout
- [ ] Index entry added to `docs/explanation/post-mortems/README.md`
- [ ] `doc_status` advances to `closed` only after all P0 items resolve

## References

**In-repo**:

- [`docs/explanation/post-mortems/README.md`](../../../../docs/explanation/post-mortems/README.md) — Writer-facing template and index
- [No Secrets in Git](../../security/no-secrets-in-committed-files.md) — Hard iron rule; applies in full to post-mortems
- [Diagrams Convention](../../formatting/diagrams.md) — Mermaid syntax and accessibility rules
- [Color Accessibility Convention](../../formatting/color-accessibility.md) — Verified WCAG AA palette
- [Timestamp Format](../../formatting/timestamp.md) — UTC+7 WIB standard used in timelines
- [Diátaxis Framework](../diataxis-framework.md) — Why post-mortems belong in `docs/explanation/`
- [Plans Organization](../plans.md) — How to create a `plans/` entry for action items
- [Knowledge Capture Convention](../../../development/quality/knowledge-capture.md) — The plan-execution
  triage matrix that decides when a captured learning routes here as a post-mortem, versus a
  convention, doc, agent, skill, code change, or discard

**Industry sources**:

- Beyer, B. et al. (2016). _Site Reliability Engineering_, Chapter 15: Postmortem Culture:
  Learning from Failure. Google. <https://sre.google/sre-book/postmortem-culture/>
- Allspaw, J. (2012). _Blameless PostMortems and a Just Culture_. Etsy Code as Craft.
  <https://www.etsy.com/codeascraft/blameless-postmortems>
- PagerDuty. _Postmortem Templates and Best Practices_.
  <https://postmortems.pagerduty.com/>
- Atlassian. _Incident Handbook: How to Run a Postmortem_.
  <https://www.atlassian.com/incident-management/postmortem>
