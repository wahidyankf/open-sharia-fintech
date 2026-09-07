---
description: "Explains why the link-fixer agent is assigned the fast tier."
when_to_use: Use when checking why link-fixer or a similar mechanical-fix agent should be fast-tier.
---

# Special Considerations — Link Fixer as Fast-Tier

The apps-ayokoding-www-link-fixer uses the fast tier despite being a fixer (yellow) — previously execution-grade. Its work is deterministic URL replacement driven entirely by a checker audit report: no independent link analysis, no content reasoning, just old-URL → new-URL substitution followed by an HTTP status re-check. The fast-grade model ([benchmark reference](../../../../docs/reference/ai-model-benchmarks.md#claude-haiku-45)) is fully sufficient and costs half as much per token as the execution grade. This is the fixer analogue of the Link Checkers as Fast-Tier rule above.
