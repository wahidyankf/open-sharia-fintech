---
title: "Scheme 3 — CLI Command Naming: `{domain} {noun…} {verb}` (Verb-Last)"
description: The verb-last `{domain} {noun...} {verb}` grammar for rhino-cli subcommands, including the old-to-new command mapping and cross-domain moves.
category: explanation
subcategory: development
tags:
  - nx
  - naming
  - conventions
created: 2026-06-13
when_to_use: Use when adding or renaming a rhino-cli subcommand, or looking up the verb-last replacement for a retired verb-middle command.
---

# Scheme 3 — CLI Command Naming: `{domain} {noun…} {verb}` (Verb-Last)

All `rhino-cli` subcommands follow a verb-last grammar introduced in §2a of the SDLC-parity plan
(2026-06-26). The terminal token of every command path is the **verb** — `validate`, `generate`,
`clean`, `scaffold`, or similar.

**Pattern**: `{domain} {sub-domain…} {noun} {verb}`

| Old (verb-middle)                          | New (verb-last)                            |
| ------------------------------------------ | ------------------------------------------ |
| `convention validate emoji`                | `convention emoji validate`                |
| `convention validate license`              | `convention license validate`              |
| `harness validate bindings`                | `harness bindings validate`                |
| `harness validate duplication`             | `harness duplication validate`             |
| `harness validate sync`                    | `harness sync validate`                    |
| `harness validate claude`                  | `harness claude validate`                  |
| `harness generate bindings`                | `harness bindings generate`                |
| `md validate links`                        | `md links validate`                        |
| `md validate mermaid`                      | `md mermaid validate`                      |
| `md validate heading-hierarchy`            | `md heading-hierarchy validate`            |
| `md validate naming`                       | `md naming validate`                       |
| `md validate frontmatter`                  | `md frontmatter validate`                  |
| `md validate frontmatter-dates`            | `md frontmatter-dates validate`            |
| `repo-governance validate vendor`          | `repo-governance vendor validate`          |
| `repo-governance validate layer-coherence` | `repo-governance layer-coherence validate` |
| `repo-governance validate traceability`    | `repo-governance traceability validate`    |
| `specs validate gherkin-cardinality`       | `specs gherkin-cardinality validate`       |

**Cross-domain moves** (domain changes, not just verb position):

| Removed                                        | Replaced by                                      |
| ---------------------------------------------- | ------------------------------------------------ |
| legacy `convention` per-surface size validator | `governance word-budget validate`                |
| `harness validate naming`                      | Removed (agent role-suffix rule withdrawn)       |
| `workflows validate naming`                    | Removed (workflow type-suffix rule withdrawn)    |
| `harness sync opencode`                        | `harness bindings generate --harness opencode`   |
| `harness emit amazonq`                         | `harness bindings generate --harness amazonq`    |
| `convention validate agents-md-size`           | Removed (superseded by `governance-word-budget`) |
| `md validate readme-index`                     | `governance readme-index validate`               |
| `git pre-commit`                               | Removed (pre-commit steps call tools directly)   |

**Stable commands** (already verb-last or single-word noun, unchanged):

- `env validate`, `env init`, `env backup`, `env restore`
- `env staged-guard validate`
- `specs structure validate`, `specs behavior-coverage validate`, `specs domain-coverage validate`
- All `{domain} audit` leaf commands

**Rules**:

- Verbs (`validate`, `generate`, `clean`, `scaffold`) are always the LAST token.
- Nouns are kebab-case (`heading-hierarchy`, `gherkin-cardinality`, `frontmatter-dates`).
- Cross-domain moves require removing the old path entirely — no aliases are kept.
- Any new CLI command added must follow this verb-last pattern.
