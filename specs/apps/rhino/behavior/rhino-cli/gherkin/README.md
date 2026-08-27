# rhino-cli Gherkin Specs

Gherkin feature files for [rhino-cli](../../../../../../apps/rhino-cli/README.md) — the Repository
Hygiene & INtegration Orchestrator CLI.

## Structure

Feature files are grouped into domain subdirectories, one per subcommand family:

```
behavior/rhino-cli/gherkin/
├── contracts/              # contracts subcommand family (scaffolding generators)
├── convention/             # convention subcommand family
├── ddd/                    # ddd subcommand family
├── env/                    # env subcommand family
├── env-contract/           # env validate's IaC (terraform/ansible) dispatch surface
├── gate/                   # gate-registry command family
├── git/                    # git subcommand family
├── governance/             # governance subcommand family (word-budget, readme-index)
├── harness/                # harness subcommand family (agent/binding machinery)
├── md/                     # md subcommand family
├── repo-config/            # repo-config.yml-driven-behaviour regressions
├── repo-config-validate/   # repo-config validate schema-parity gate
├── repo-governance/        # repo-governance subcommand family
├── spec-coverage/          # specs coverage command (folded from old spec-coverage subcommand)
├── specs/                  # specs subcommand family
├── system/                 # system commands (doctor)
└── test-coverage/          # test-coverage subcommand family
```

## Feature Files by Domain

### contracts

| File                              | Command(s)                | Scenarios |
| --------------------------------- | ------------------------- | --------- |
| `contracts-dart-scaffold.feature` | `contracts dart-scaffold` | 3         |

### convention

| File                                    | Command(s)                    | Scenarios |
| --------------------------------------- | ----------------------------- | --------- |
| `convention-audit.feature`              | `convention audit`            | 1         |
| `repo-governance-emoji-audit.feature`   | `convention emoji validate`   | 6         |
| `repo-governance-license-audit.feature` | `convention license validate` | 4         |

### ddd

| File             | Command(s)                               | Scenarios |
| ---------------- | ---------------------------------------- | --------- |
| `ddd-bc.feature` | `specs structure validate` (`bc:` layer) | 11        |
| `ddd-ul.feature` | `specs structure validate` (`ul:` layer) | 7         |

### env

| File                             | Command(s)     | Scenarios |
| -------------------------------- | -------------- | --------- |
| `env-backup.feature`             | `env backup`   | 21        |
| `env-init.feature`               | `env init`     | 4         |
| `env-restore.feature`            | `env restore`  | 16        |
| `env-validate-app-drift.feature` | `env validate` | 3         |

### env-contract

| File                         | Command(s)     | Scenarios |
| ---------------------------- | -------------- | --------- |
| `iac-env-validation.feature` | `env validate` | 1         |

### gate

| File                             | Command(s)                            | Scenarios |
| -------------------------------- | ------------------------------------- | --------- |
| `gate-binary-resolution.feature` | `gate run` (binary resolution)        | 4         |
| `gate-declaration.feature`       | `repo-config validate` / `gate list`  | 11        |
| `gate-emission.feature`          | `gate emit`                           | 5         |
| `gate-enumeration.feature`       | `gate list`                           | 8         |
| `gate-execution.feature`         | `gate run`                            | 30        |
| `gate-validation.feature`        | `gate validate`                       | 26        |
| `parity-manifest.feature`        | `parity manifest generate`/`validate` | 5         |

### git

| File                     | Command(s)       | Scenarios |
| ------------------------ | ---------------- | --------- |
| `git-pre-commit.feature` | `git pre-commit` | 5         |

### governance

| File                              | Command(s)                         | Scenarios |
| --------------------------------- | ---------------------------------- | --------- |
| `governance-word-budget.feature`  | `governance word-budget validate`  | 22        |
| `governance-readme-index.feature` | `governance readme-index validate` | 19        |

### harness

| File                                      | Command(s)                                                     | Scenarios |
| ----------------------------------------- | -------------------------------------------------------------- | --------- |
| `agents-bindings.feature`                 | `harness bindings validate`/`generate`                         | 10        |
| `agents-detect-duplication.feature`       | `harness duplication validate`                                 | 4         |
| `agents-skills-mirror.feature`            | `harness bindings generate`/`validate` (skills mirror)         | 5         |
| `agents-sync.feature`                     | `harness sync validate`                                        | 8         |
| `agents-validate-claude.feature`          | `harness claude validate`                                      | 5         |
| `codex-binding.feature`                   | `harness bindings generate` (Codex)                            | 3         |
| `governance-word-budget-pre-push.feature` | `governance word-budget validate`                              | 4         |
| `governance-word-budget-rule.feature`     | `governance word-budget validate`                              | 5         |
| `harness-audit.feature`                   | `harness audit`                                                | 1         |
| `harness-catalog.feature`                 | `harness catalog generate`/`validate`                          | 2         |
| `harness-ownership.feature`               | `harness ownership validate`                                   | 5         |
| `harness-sync-triage.feature`             | `harness sync triage`/`promote`                                | 12        |
| `opencode-conformance.feature`            | n/a (catalog-content and ideas-tree invariant)                 | 2         |
| `opencode-skills-removal.feature`         | `governance word-budget validate` (content-deletion invariant) | 2         |
| `vendored-skill-preservation.feature`     | `harness bindings generate`/`validate`, `repo-config validate` | 2         |

### md

| File                                        | Command(s)                      | Scenarios |
| ------------------------------------------- | ------------------------------- | --------- |
| `docs-validate-frontmatter.feature`         | `md frontmatter validate`       | 11        |
| `docs-validate-heading-hierarchy.feature`   | `md heading-hierarchy validate` | 12        |
| `docs-validate-links.feature`               | `md links validate`             | 10        |
| `docs-validate-mermaid.feature`             | `md mermaid validate`           | 39        |
| `docs-validate-naming.feature`              | `md naming validate`            | 3         |
| `md-audit.feature`                          | `md audit`                      | 1         |
| `repo-governance-frontmatter-audit.feature` | `md frontmatter-dates validate` | 5         |

### repo-config

| File                  | Command(s)                                                 | Scenarios |
| --------------------- | ---------------------------------------------------------- | --------- |
| `data-driven.feature` | N/A — data-driven-behavior regression (no single CLI verb) | 9         |

### repo-config-validate

| File                           | Command(s)             | Scenarios |
| ------------------------------ | ---------------------- | --------- |
| `repo-config-validate.feature` | `repo-config validate` | 5         |

### repo-governance

| File                                         | Command(s)                                 | Scenarios |
| -------------------------------------------- | ------------------------------------------ | --------- |
| `repo-governance-audit.feature`              | `repo-governance audit`                    | 6         |
| `repo-governance-layer-coherence.feature`    | `repo-governance layer-coherence validate` | 3         |
| `repo-governance-traceability-audit.feature` | `repo-governance traceability validate`    | 8         |
| `repo-governance-vendor-audit.feature`       | `repo-governance vendor validate`          | 12        |

### spec-coverage

| File                             | Command(s)       | Scenarios |
| -------------------------------- | ---------------- | --------- |
| `spec-coverage-validate.feature` | `specs coverage` | 12        |

### specs

| File                              | Command(s)                                                                                  | Scenarios |
| --------------------------------- | ------------------------------------------------------------------------------------------- | --------- |
| `behavior-coverage.feature`       | `specs behavior-coverage validate`                                                          | 6         |
| `domain-coverage.feature`         | `specs behavior-coverage validate` (domain allowlist gate)                                  | 2         |
| `e2e-coverage.feature`            | `specs e2e-coverage validate`                                                               | 13        |
| `env-staged-guard.feature`        | `env staged-guard validate`                                                                 | 3         |
| `gherkin-cardinality.feature`     | `specs gherkin-cardinality validate`                                                        | 1         |
| `harness-bindings.feature`        | `harness bindings validate`                                                                 | 2         |
| `harness-registry-driven.feature` | `harness duplication validate`                                                              | 2         |
| `specs-audit.feature`             | `specs audit`                                                                               | 1         |
| `validate-adoption.feature`       | `specs structure validate` (merged; scenarios exercise `validate_spec_adoption` in-process) | 4         |
| `validate-counts.feature`         | `specs counts validate`                                                                     | 4         |
| `validate-links.feature`          | `md links validate` (composed; standalone `specs validate-links` was deleted)               | 4         |
| `validate-tree.feature`           | `specs structure validate` (merged; scenarios exercise `validate_spec_tree` in-process)     | 4         |
| `worktree-agnostic.feature`       | N/A — internal `find_root_from_worktree` regression (no CLI verb)                           | 1         |

### system

| File                             | Command(s)                                             | Scenarios |
| -------------------------------- | ------------------------------------------------------ | --------- |
| `cargo-target-share.feature`     | `doctor`                                               | 18        |
| `doctor.feature`                 | `doctor`                                               | 17        |
| `fsharp-tool-invocation.feature` | N/A — F# lint-target manifest regression (no CLI verb) | 1         |

### test-coverage

| File                             | Command(s)               | Scenarios |
| -------------------------------- | ------------------------ | --------- |
| `test-coverage-diff.feature`     | `test-coverage diff`     | 4         |
| `test-coverage-merge.feature`    | `test-coverage merge`    | 3         |
| `test-coverage-validate.feature` | `test-coverage validate` | 10        |

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
- [Env-Contract Domain](./env-contract/README.md)
- [Gate Gherkin Specs](./gate/README.md)
- [rhino — behavior/rhino-cli/gherkin/git](./git/README.md)
- [rhino — behavior/rhino-cli/gherkin/governance](./governance/README.md)
- [rhino — behavior/rhino-cli/gherkin/harness](./harness/README.md)
- [rhino — behavior/rhino-cli/gherkin/md](./md/README.md)
- [Repo-Config Domain](./repo-config/README.md)
- [Repo-Config-Validate Domain](./repo-config-validate/README.md)
- [rhino — behavior/rhino-cli/gherkin/repo-governance](./repo-governance/README.md)
- [rhino — behavior/rhino-cli/gherkin/spec-coverage](./spec-coverage/README.md)
- [Specs Domain](./specs/README.md)
- [rhino — behavior/rhino-cli/gherkin/system](./system/README.md)
- [Test Coverage Domain](./test-coverage/README.md)
