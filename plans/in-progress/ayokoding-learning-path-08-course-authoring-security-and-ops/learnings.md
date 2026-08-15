<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: ayokoding-learning-path-08-course-authoring-security-and-ops

## Phase 4 Rule-15 exemption

The `web-exploratory-tester`, `web-usability-tester`, and `web-design-tester` triad is exempt because:

1. This plan ships only Markdown course bundles, not screens or components; the rendering surface is
   owned by `ayokoding-learning-path-03-navigation-ui`.
2. Dedicated content, facts, and link checkers cover the authored material more directly than the
   general live-site triad.
3. A triad run on these pages would exercise the navigation plan's rendering surface and could produce
   findings this plan cannot act on.

This exemption is narrow: Playwright MCP verification of all eleven `en` course pages at 375, 768, and
1280 px was performed with screenshot evidence in `evidence/`.
