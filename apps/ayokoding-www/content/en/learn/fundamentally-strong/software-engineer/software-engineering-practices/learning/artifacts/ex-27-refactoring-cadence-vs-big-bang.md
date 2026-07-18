---
title: "Artifact: Continuous Refactoring vs. a Big-Bang Rewrite"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 67
---

> ex-27 &middot; exercises co-14 &middot; the same debt, two remediation strategies compared.

**Debt**: the `inventory` module's pricing logic is scattered across four files with duplicated
rounding rules, discovered while shipping an unrelated feature.

| Option                | Approach                                                                                                                                 | Risk                                                                                                                                                                             | Cost                                                         |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| A -- continuous       | Extract one shared `round_price()` helper per touched file, over the next 6-8 unrelated PRs, each a small, independently reviewable diff | Low -- each change ships behind the normal review/CI gate, and a bad extraction only affects the one file it touched                                                             | Spread thin, mostly invisible to planning                    |
| B -- big-bang rewrite | A dedicated month-long branch rewriting all four files' pricing logic at once, merged in one large PR                                    | High -- a month of drift against trunk, one enormous diff no reviewer can meaningfully review line by line, and a single merge that can break all four call sites simultaneously | Concentrated, highly visible, blocks a month of related work |

**Decision**: Option A, continuous extraction.

**Verify**: the decision names a specific risk rationale (large-diff unreviewability and a month of
merge drift under Option B) rather than a vague "big rewrites are risky" preference, satisfying
co-14's rule.

**Key takeaway**: the same total amount of code changes either way -- the difference is entirely in
diff size and merge frequency, and smaller, more frequent diffs are strictly easier to review and
roll back.

**Why It Matters**: a month-long rewrite branch is exactly the long-lived-branch failure mode
co-01's trunk-based-development argument warns about, applied to refactoring specifically: the
longer a branch lives before merging, the more trunk drifts underneath it, and the more likely the
eventual merge introduces a regression no single diff was ever small enough to catch in review.
