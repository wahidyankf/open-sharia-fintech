---
description: The surfaces the code-as-liability practice reaches — non-Markdown files under apps/, libs/, and scripts/ — and the explicit exemption for tests, specs, and fixtures.
when_to_use: Use when deciding whether a given added file falls under the cost/benefit obligation.
---

# What Counts as Code

Code means **non-Markdown files under `apps/`, `libs/`, and `scripts/`** — source, configuration,
and scripts alike. A YAML pipeline job and a Rust module are equally code: both must be understood
and kept working by whoever inherits them.

That list is the floor, not a boundary to hide behind. Anything executable or machine-consumed
elsewhere in the tree is covered by the same reasoning; relocating a file does not make it free.

Markdown is prose. It is held to the
[governance word budget](../../../conventions/structure/governance-word-budget.md) instead, which
applies the same pressure through a different mechanism.

## Tests and Specs Are Exempt

Tests, Gherkin specs, and their fixtures are **out of scope**. This is stated explicitly so the
practice can never be cited against writing them.

They are what makes changing the other code safe, and they are separately mandatory: development is
test-driven, and every bug fix carries a regression test. A pull request that adds only tests owes
no cost/benefit section.

A redundant or low-value test is still worth challenging on its own merits during review. That is a
test-quality question, not this practice's business.

## Related Documents

- [The Obligation](./the-obligation.md) — what a pull request must state once code is in scope.
- [Test-Driven Development](../../workflow/test-driven-development.md) — why the exemption exists.
