# rhino-cli Gherkin Specs

Gherkin feature files for [rhino-cli](../../../../../../apps/rhino-cli/README.md) — the Repository
Hygiene & INtegration Orchestrator CLI.

## Structure

Feature files are grouped into domain subdirectories, one per subcommand family:

```
behavior/rhino-cli/gherkin/
├── convention/       # convention subcommand family
├── ddd/              # ddd subcommand family
├── env/              # env subcommand family
├── gate/              # gate-registry command family
├── git/              # git subcommand family
├── harness/          # harness subcommand family (agent/binding machinery)
├── md/               # md subcommand family
├── repo-governance/  # repo-governance subcommand family
├── spec-coverage/    # specs coverage command (folded from old spec-coverage subcommand)
├── specs/            # specs subcommand family
└── system/           # system commands (doctor)
```

## Feature Files by Domain

### convention

| File                                    | Command(s)                    | Scenarios |
| --------------------------------------- | ----------------------------- | --------- |
| `repo-governance-emoji-audit.feature`   | `convention emoji validate`   | 5         |
| `repo-governance-license-audit.feature` | `convention license validate` | 4         |

### ddd

| File             | Command(s)                               | Scenarios |
| ---------------- | ---------------------------------------- | --------- |
| `ddd-bc.feature` | `specs structure validate` (`bc:` layer) | 11        |
| `ddd-ul.feature` | `specs structure validate` (`ul:` layer) | 7         |

### env

| File                  | Command(s)    | Scenarios |
| --------------------- | ------------- | --------- |
| `env-backup.feature`  | `env backup`  | 18        |
| `env-init.feature`    | `env init`    | 4         |
| `env-restore.feature` | `env restore` | 13        |

### gate

| File                             | Command(s)                            | Scenarios |
| -------------------------------- | ------------------------------------- | --------- |
| `gate-binary-resolution.feature` | `gate run` (binary resolution)        | 4         |
| `gate-declaration.feature`       | `repo-config validate` / `gate list`  | 9         |
| `gate-emission.feature`          | `gate emit`                           | 5         |
| `gate-enumeration.feature`       | `gate list`                           | 7         |
| `gate-execution.feature`         | `gate run`                            | 25        |
| `gate-validation.feature`        | `gate validate`                       | 20        |
| `parity-manifest.feature`        | `parity manifest generate`/`validate` | 4         |

### git

| File                     | Command(s)       | Scenarios |
| ------------------------ | ---------------- | --------- |
| `git-pre-commit.feature` | `git pre-commit` | 1         |

### governance

| File                              | Command(s)                         | Scenarios |
| --------------------------------- | ---------------------------------- | --------- |
| `governance-word-budget.feature`  | `governance word-budget validate`  | 6         |
| `governance-readme-index.feature` | `governance readme-index validate` | 15        |

### harness

| File                                        | Command(s)                                                     | Scenarios |
| ------------------------------------------- | -------------------------------------------------------------- | --------- |
| `agents-bindings.feature`                   | `harness bindings validate`/`generate`                         | 10        |
| `agents-detect-duplication.feature`         | `harness duplication validate`                                 | 4         |
| `agents-skills-mirror.feature`              | `harness bindings generate`/`validate` (skills mirror)         | 5         |
| `agents-sync.feature`                       | `harness sync validate`                                        | 8         |
| `agents-validate-claude.feature`            | `harness claude validate`                                      | 5         |
| `codex-binding.feature`                     | `harness bindings generate` (Codex)                            | 3         |
| `governance-word-budget-agents-md.feature`  | `governance word-budget validate`                              | 3         |
| `governance-word-budget-pre-push.feature`   | `governance word-budget validate`                              | 3         |
| `governance-word-budget-rule.feature`       | `governance word-budget validate`                              | 5         |
| `governance-word-budget-thresholds.feature` | `governance word-budget validate`                              | 6         |
| `harness-audit.feature`                     | `harness audit`                                                | 1         |
| `harness-catalog.feature`                   | `harness catalog generate`/`validate`                          | 2         |
| `harness-ownership.feature`                 | `harness ownership validate`                                   | 5         |
| `harness-sync-triage.feature`               | `harness sync triage`/`promote`                                | 12        |
| `opencode-conformance.feature`              | n/a (catalog-content and ideas-tree invariant)                 | 2         |
| `opencode-skills-removal.feature`           | `governance word-budget validate` (content-deletion invariant) | 2         |
| `vendored-skill-preservation.feature`       | `harness bindings generate`/`validate`, `repo-config validate` | 2         |

### md

| File                                        | Command(s)                      | Scenarios |
| ------------------------------------------- | ------------------------------- | --------- |
| `docs-validate-frontmatter.feature`         | `md frontmatter validate`       | 5         |
| `docs-validate-heading-hierarchy.feature`   | `md heading-hierarchy validate` | 4         |
| `docs-validate-links.feature`               | `md links validate`             | 4         |
| `docs-validate-mermaid.feature`             | `md mermaid validate`           | 22        |
| `docs-validate-naming.feature`              | `md naming validate`            | 3         |
| `repo-governance-frontmatter-audit.feature` | `md frontmatter-dates validate` | 5         |

### repo-governance

| File                                         | Command(s)                                 | Scenarios |
| -------------------------------------------- | ------------------------------------------ | --------- |
| `repo-governance-audit.feature`              | `repo-governance audit`                    | 5         |
| `repo-governance-layer-coherence.feature`    | `repo-governance layer-coherence validate` | 3         |
| `repo-governance-traceability-audit.feature` | `repo-governance traceability validate`    | 5         |
| `repo-governance-vendor-audit.feature`       | `repo-governance vendor validate`          | 7         |

### spec-coverage

| File                             | Command(s)       | Scenarios |
| -------------------------------- | ---------------- | --------- |
| `spec-coverage-validate.feature` | `specs coverage` | 10        |

### specs

| File                              | Command(s)                                                                                  | Scenarios |
| --------------------------------- | ------------------------------------------------------------------------------------------- | --------- |
| `behavior-coverage.feature`       | `specs behavior-coverage validate`                                                          | 6         |
| `domain-coverage.feature`         | `specs behavior-coverage validate` (domain allowlist gate)                                  | 2         |
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

### system

| File                         | Command(s) | Scenarios |
| ---------------------------- | ---------- | --------- |
| `cargo-target-share.feature` | `doctor`   | 18        |
| `doctor.feature`             | `doctor`   | 17        |

## Conventions

- **File naming**: `[domain]-[action].feature` (kebab-case, domain-prefixed)
- **Step language**: CLI-semantic only — no framework or library names
- **User story block**: Every `Feature:` block opens with `As a … / I want … / So that …`

## Related

- **Parent**: [rhino-cli specs](../../README.md)
- **BDD Standards**: [behavior-driven-development-bdd/](../../../../../../docs/explanation/software-engineering/development/behavior-driven-development-bdd/README.md)

See [Specs Directory Structure Convention](../../../../../../repo-governance/conventions/structure/specs-directory-structure.md)
for the canonical purpose of this folder.

- [Contracts Domain](./contracts/README.md)
- [rhino — behavior/rhino-cli/gherkin/convention](./convention/README.md)
- [rhino — behavior/rhino-cli/gherkin/ddd](./ddd/README.md)
- [rhino — behavior/rhino-cli/gherkin/env](./env/README.md)
- [Gate Gherkin Specs](./gate/README.md)
- [rhino — behavior/rhino-cli/gherkin/git](./git/README.md)
- [rhino — behavior/rhino-cli/gherkin/governance](./governance/README.md)
- [rhino — behavior/rhino-cli/gherkin/harness](./harness/README.md)
- [rhino — behavior/rhino-cli/gherkin/md](./md/README.md)
- [rhino — behavior/rhino-cli/gherkin/repo-governance](./repo-governance/README.md)
- [rhino — behavior/rhino-cli/gherkin/spec-coverage](./spec-coverage/README.md)
- [rhino — behavior/rhino-cli/gherkin/system](./system/README.md)
- [Test Coverage Domain](./test-coverage/README.md)
