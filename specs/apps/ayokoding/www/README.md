# AyoKoding Web — Specification Corpus

Audience: engineers and technical product managers working on
[`apps/ayokoding-www`](../../../../apps/ayokoding-www/README.md) — the multilingual educational
site.

This corpus is the single source of truth for what the site does. A scenario here defines what a
learner sees, what a tRPC procedure returns, or what a build-time script must produce.

## Contents

- [Architecture](./architecture.md) — the current as-built system: its context, the one container it
  deploys, the bounded contexts inside it, and the constraints that bind them.
- [Behaviors](./behaviors/README.md) — the recursive Gherkin corpus, split by the perspective a
  scenario takes rather than by deployable.

## Why one owner

AyoKoding ships exactly one deployable. The server tier and the browser tier are two runtime tiers
of the same Next.js container, and the build-time index generators run before it is built. All three
therefore belong to one owner corpus, with `behaviors/` carrying the split:

| Directory                | Perspective                                                         |
| ------------------------ | ------------------------------------------------------------------- |
| `behaviors/frontend/`    | what a learner sees — DOM, navigation, accessibility, locale toggle |
| `behaviors/backend/`     | what a tRPC procedure returns — shapes, error codes, locale scoping |
| `behaviors/build-tools/` | what the build-time index generators must produce                   |

## Related

- [`apps/ayokoding-www/README.md`](../../../../apps/ayokoding-www/README.md) — the implementing project.
- [BDD Spec-to-Test Mapping Convention](../../../../repo-governance/development/infra/bdd-spec-test-mapping.md) —
  the repository-wide rule this corpus follows.
