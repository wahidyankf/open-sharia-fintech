---
title: "Special Considerations — Link Fixer as Fast-Tier"
description: "Explains why the link-fixer agent is assigned the fast tier."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when checking why link-fixer or a similar mechanical-fix agent should be fast-tier.
---

# Special Considerations — Link Fixer as Fast-Tier

The apps-ayokoding-www-link-fixer uses the fast tier despite being a fixer (yellow) — previously execution-grade. Its work is deterministic URL replacement driven entirely by a checker audit report: no independent link analysis, no content reasoning, just old-URL → new-URL substitution followed by an HTTP status re-check. The fast-tier model (73.3% SWE-bench Verified — [benchmark reference](../../../../docs/reference/ai-model-benchmarks.md#claude-haiku-45)) is fully sufficient and costs 5× less per token than the execution-grade tier. This is the fixer analogue of the Link Checkers as Fast-Tier rule above.
