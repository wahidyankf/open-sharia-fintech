---
description: When encountering preexisting errors, bugs, or broken state during any work, fix the root cause rather than ignoring, monkey-patching, or passively mentioning the problem
when_to_use: Use whenever you encounter a preexisting error, broken test, incorrect configuration, or degraded code while doing other work.
---

# Proactive Preexisting Error Resolution

When you encounter a preexisting error, broken test, incorrect configuration, or degraded code during your work — fix the root cause. Not around it. Not after it. Not in a note at the bottom of a PR description. Fix it now.

This practice extends [Root Cause Orientation](../../principles/general/root-cause-orientation.md) from governing assigned bug reports to also governing errors discovered incidentally during other work: every encounter with broken state is an obligation to leave the codebase healthier than you found it.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: The foundational requirement is to find root causes and fix them properly. This practice operationalizes that requirement for errors encountered incidentally — not only when given a direct bug report.

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Encountering broken state and continuing anyway is the opposite of deliberate. Recognizing and resolving the problem before proceeding is the deliberate choice.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Monkey-patching adds layers of complexity that obscure the real problem. A proper root cause fix is almost always simpler in the long run than a workaround that accumulates alongside the original defect.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Agents that fix errors autonomously reduce the human overhead of maintaining a backlog of known-but-unresolved problems. Every passively mentioned issue that lands in a backlog requires human triage, scheduling, and re-investigation.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Content Quality Principles](../../conventions/writing/quality.md)**: When fixing preexisting errors in documentation — broken links, incorrect headings, outdated examples — the same root cause standard applies. The fix belongs in the document, not in a review comment.

## Contents

- [Why This Matters](./proactive-preexisting-error-resolution/why-this-matters.md) — the backlog problem, the monkey-patch problem, and the normalization problem.
- [The Three Anti-Patterns](./proactive-preexisting-error-resolution/the-three-anti-patterns.md) — acting ignorant, monkey-patching, and passive mentioning, each with worked examples.
- [Expected Behaviour](./proactive-preexisting-error-resolution/expected-behaviour.md) — the five-step response: diagnose, fix, verify, scope, communicate.
- [Scope Judgment](./proactive-preexisting-error-resolution/scope-judgment.md) — how to size a fix as small (inline), medium (own commit), or large (a plan).
- [Checklist, For AI Agents, and Related Documentation](./proactive-preexisting-error-resolution/checklist-agents-and-related-documentation.md) — the completion checklist, agent behaviour rules, and links to related conventions.
