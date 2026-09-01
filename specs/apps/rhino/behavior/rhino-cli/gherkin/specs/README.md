# Specs Domain

Gherkin specs for the `specs` subcommand family (coverage, structure, and audit validators).

| File                              | Command(s)                                                                                  | Scenarios |
| --------------------------------- | ------------------------------------------------------------------------------------------- | --------- |
| `behavior-coverage.feature`       | `specs behavior-coverage validate`                                                          | 6         |
| `e2e-coverage.feature`            | `specs e2e-coverage validate`                                                               | 9         |
| `env-staged-guard.feature`        | `env staged-guard validate`                                                                 | 2         |
| `gherkin-cardinality.feature`     | `specs gherkin-cardinality validate`                                                        | 1         |
| `harness-bindings.feature`        | `harness bindings validate`                                                                 | 1         |
| `harness-registry-driven.feature` | `harness duplication validate`                                                              | 1         |
| `specs-audit.feature`             | `specs audit`                                                                               | 1         |
| `validate-adoption.feature`       | `specs structure validate` (merged; scenarios exercise `validate_spec_adoption` in-process) | 4         |
| `validate-counts.feature`         | `specs counts validate`                                                                     | 4         |
| `validate-links.feature`          | `md links validate` (composed; standalone `specs validate-links` was deleted)               | 4         |
| `validate-tree.feature`           | `specs structure validate` (merged; scenarios exercise `validate_spec_tree` in-process)     | 4         |
| `worktree-agnostic.feature`       | N/A — internal `find_root_from_worktree` regression (no CLI verb)                           | 1         |

## Related

- **Parent**: [gherkin](../README.md)
