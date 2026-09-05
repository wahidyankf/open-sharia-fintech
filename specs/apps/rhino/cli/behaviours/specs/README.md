# Specs Domain

Gherkin specs for the active `specs`, Markdown-link, and staged-environment validation commands.

| File                              | Public command              | Expanded scenarios |
| --------------------------------- | --------------------------- | ------------------ |
| `env-staged-guard.feature`        | `env staged-guard validate` | 8                  |
| `specs-audit.feature`             | `specs audit`               | 1                  |
| `validate-adoption.feature`       | `specs structure validate`  | 4                  |
| `validate-counts.feature`         | `specs counts validate`     | 5                  |
| `validate-links.feature`          | `md links validate`         | 4                  |
| `validate-logical-corpus.feature` | `specs structure validate`  | 6                  |
| `validate-tree.feature`           | `specs structure validate`  | 3                  |

The former `harness-bindings.feature` (two scenarios), `harness-registry-driven.feature` (two
scenarios), and `worktree-agnostic.feature` (one scenario) were retired on 2026-09-05. The first
two asserted a one-time harness-registry migration through source/config inspection instead of a
user-observable command result. The last explicitly described an internal test-suite regression and
had no Rhino CLI verb. Their production commands remain covered by the canonical `harness/`
behaviour family; worktree discovery remains an implementation concern exercised by ordinary
command tests rather than a standalone product behaviour.

## Related

- **Parent**: [gherkin](../README.md)
