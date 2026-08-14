---
title: "Research Delegation"
description: "Explains that docs-checker and docs-tutorial-checker delegate multi-page web research to web-researcher to keep audit contexts lean."
when_to_use: "Use when investigating why a checker is or isn't calling WebSearch/WebFetch directly for a given claim."
---

# Research Delegation

The `docs-checker` and `docs-tutorial-checker` agents invoked by this workflow delegate
multi-page web research to the [`web-researcher`](../../../../.claude/agents/web/web-researcher.md)
delegated agent when verifying a single claim requires more than one or two searches, or more than two
fetches. Checkers retain in-context `WebSearch`/`WebFetch` only for single-shot verification
against known authoritative URLs. This keeps each audit context lean. The delegation is encoded
in each checker agent's prompt — no workflow-level configuration required.
