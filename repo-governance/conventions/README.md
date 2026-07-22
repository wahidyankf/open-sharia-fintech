---
title: "Conventions"
description: Documentation conventions and standards for open-sharia-enterprise
category: explanation
subcategory: conventions
tags:
  - index
  - conventions
  - standards
created: 2025-11-22
---

# Conventions

Documentation conventions and standards for the open-sharia-enterprise project. These documents define how documentation should be organized, named, written, and formatted.

**Governance**: All conventions in this directory serve the [Vision](../vision/open-sharia-enterprise.md) (Layer 0) and implement the [Core Principles](../principles/README.md) (Layer 1) as part of the six-layer architecture. Each convention MUST include a "Principles Implemented/Respected" section that explicitly traces back to foundational principles. See [Repository Governance Architecture](../repository-governance-architecture.md) for complete governance model and [Convention Writing Convention](./writing/conventions.md) for structure requirements.

## Scope

**This directory contains conventions for DOCUMENTATION:**

**Belongs Here:**

- How to write and format markdown content
- Documentation organization and structure (Diataxis)
- File naming, linking, and cross-referencing
- Visual elements in docs (diagrams, colors, emojis, math notation)
- Content quality and accessibility standards
- Documentation file formats (tutorials, plans)
- Repository documentation standards (README, CONTRIBUTING)

**Does NOT Belong Here (use [Development](../development/README.md) instead):**

- Software development methodologies (BDD, testing, agile)
- Build processes and tooling workflows
- Development infrastructure (temporary files, build artifacts)
- Git workflows and commit practices
- AI agent development standards
- Code quality and testing practices

## The Layer Test for Conventions

**Question**: Does this document answer "**WHAT are the documentation rules?**"

**Belongs in conventions/** if it defines:

- HOW to write markdown content (formatting, syntax, structure)
- WHAT files should be named or organized
- WHAT visual standards to follow in docs (colors, diagrams, emojis)
- WHAT content quality standards apply to documentation

**Does NOT belong** if it defines:

- WHY we value something (that's a principle)
- HOW to develop software/themes (that's a development practice)
- HOW to solve a specific problem (that's a how-to guide)

**Examples**:

- "Files must use lowercase kebab-case names" - Convention (documentation rule)
- "Use 2-space indentation for nested lists" - Convention (documentation formatting)
- "Web app themes use Tailwind CSS" - Development (software practice)
- "Why we avoid time estimates in tutorials" - Principle (foundational value)

## Directory Structure

Conventions are organized into semantic categories:

- **[formatting/](./formatting/README.md)** - Markdown formatting, syntax, visual elements
- **[linking/](./linking/README.md)** - Cross-reference and internal linking standards
- **[writing/](./writing/README.md)** - Content quality, validation, writing standards
- **[structure/](./structure/README.md)** - Documentation organization, file naming, plans
- **[tutorials/](./tutorials/README.md)** - Tutorial creation and structure conventions
- **[security/](./security/README.md)** - Security conventions governing agent behavior and data protection

---

## Formatting

Standards for markdown formatting, syntax, and visual elements.

- [Color Accessibility](./formatting/color-accessibility.md) - MASTER REFERENCE for all color decisions. Verified accessible color palette (Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC, Brown #CA9161) supporting all color blindness types, WCAG AA standards, with complete implementation guidance for Mermaid diagrams and AI agent categorization
- [Diagrams and Schemas](./formatting/diagrams.md) - Standards for Mermaid diagrams (primary) and ASCII art. Enforces an explicit Format Selection Rule: folder/file trees MUST use ASCII art (`├──`, `└──`, `│`); all relationship/flow diagram types (flow charts, sequence diagrams, state machines, architecture/component diagrams, dependency-direction, user-flow, ER/class, C4 model) MUST use Mermaid. Also contains the **UI Mockups in Plan Docs** section (both-tiers rule, design funnel, rendering-support matrix, ruled-out table) governing draft UI wireframes in UI-bearing plans; the **Placement HARD RULE** (`## Placement — the UI lives in prd.md`) requires all funnel artefacts (low-fi wireframes, hi-fi `![]()` embeds, selection, rationale) to reside in `prd.md` — a plan failing this gate is flagged HIGH by `plan-checker`. **Gate location**: Mermaid validation runs at pre-commit (staged `.md` files only, via lint-staged); does NOT run at pre-push or in a standalone CI workflow (folded into `pr-quality-gate.yml`)
- [Emoji Usage](./formatting/emoji.md) - Semantic emoji usage to enhance document scannability and engagement with accessible colored emojis
- [Indentation](./formatting/indentation.md) - Standard markdown indentation using 2 spaces per indentation level. YAML frontmatter uses 2 spaces. Code blocks use language-specific conventions
- [Linking Convention](./formatting/linking.md) - Standards for linking between documentation files using GitHub-compatible markdown. Defines two-tier formatting for rule references (first mention = markdown link, subsequent mentions = inline code). `rhino-cli md links validate` validates `#fragment` anchor references in addition to file-existence checks
- [Mathematical Notation](./formatting/mathematical-notation.md) - Standards for LaTeX notation for mathematical equations and formulas. Defines inline (`$...$`) vs display (`$$...$$`) delimiters, forbidden contexts (code blocks, Mermaid), GitHub rendering compatibility
- [Nested Code Fences](./formatting/nested-code-fences.md) - Standards for properly nesting code fences when documenting markdown structure within markdown content. Defines fence depth rules (outer = 4 backticks, inner = 3 backticks), orphaned fence detection, and validation checklist
- [Timestamp Format](./formatting/timestamp.md) - Standard timestamp format using UTC+7 (Indonesian WIB Time)

## Linking

Standards for cross-referencing and internal linking between repository content.

- [Internal AyoKoding Reference Links](./linking/internal-ayokoding-references.md) - Standards for linking from docs/ to apps/ayokoding-www/ content using relative paths instead of public web URLs. Ensures links work during local development, testing, and remain portable across environments. Defines path calculation method, common patterns, and enforcement mechanisms for repository-internal references

## Writing

Content quality standards, validation methodology, and writing guidelines.

- [Content Quality Principles](./writing/quality.md) - Universal markdown content quality standards applicable to ALL repository markdown contexts (docs/, Next.js web content, plans/, root files). Covers writing style and tone (active voice, professional, concise), heading hierarchy (single H1, proper nesting), accessibility (alt text, semantic HTML, color contrast, screen readers), and formatting. **Machine enforcement**: heading hierarchy runs on a prose allowlist (`docs/`, `repo-governance/`, `plans/` excl. `done/`, `specs/`, root `*.md`, `apps/*/README.md`, `libs/*/README.md`, `apps/*/docs/**`, `libs/*/docs/**`) at pre-commit + CI
- [Conventions](./writing/conventions.md) - **Meta-convention** defining how to write and organize convention documents. Covers document structure, scope boundaries, quality checklist, when to create new vs update existing, length guidelines, and integration with agents. Essential reading for creating or updating conventions
- [Dynamic Collection References](./writing/dynamic-collection-references.md) - Standards for referencing dynamic collections (agents, principles, conventions, practices, skills) without hardcoding counts. Prevents documentation drift by requiring count-free references with links to authoritative index documents. **Agents**: repo-rules-checker, repo-rules-fixer
- [Factual Validation](./writing/factual-validation.md) - Universal methodology for validating factual correctness across all repository content using web verification (WebSearch + WebFetch). Defines core validation methodology (command syntax, features, versions, code examples, external refs, mathematical notation, diagram colors), web verification workflow, confidence classification (Verified, Unverified, Error, Outdated)
- [FP-Variant Multi-Language Convention](./writing/fp-variant-multi-language.md) - Bidirectional idiomatic-language rule for FP-variant by-example tutorials in ayokoding-www. Requires F# AND Clojure tabs with each language kept idiomatic to its own community. Defines idiomatic patterns for each language, cross-paradigm concept handling (closest native equivalent + annotation), and per-tab annotation density (1.0–2.25 ratio). **Agents**: apps-ayokoding-www-by-example-maker, apps-ayokoding-www-by-example-checker, apps-ayokoding-www-by-example-fixer
- [Indonesian Content Policy](./writing/indonesian-content-policy.md) - Policy defining when and how to create Indonesian content in ayokoding-www. Establishes English-first policy for technical tutorials, defines Indonesian content categories (unique content, strategic translations, discouraged mirrors), provides decision tree for language selection, and specifies agent behavior for content creation
- [OSS Documentation](./writing/oss-documentation.md) - Standards for repository documentation files (README, CONTRIBUTING, ADRs, security) following open source best practices
- [README Quality](./writing/readme-quality.md) - Quality standards for README.md files ensuring engagement, accessibility, and scannability. Defines problem-solution hooks, jargon elimination (plain language over corporate speak), acronym context requirements, benefits-focused language, navigation structure, and paragraph length limits. **Agents**: readme-maker, readme-checker
- [Web Research Delegation](./writing/web-research-delegation.md) - Normative rule requiring AI agents to delegate public-web information gathering to the `web-researcher` delegated agent when research exceeds the delegation threshold (2+ `WebSearch` calls or 3+ `WebFetch` calls for a single claim). Enumerates three exceptions (single-shot known URL; fixer re-validation; link-reachability checkers). **Agents**: web-researcher, repo-rules-checker
- [Why It Matters Content Convention](./writing/why-it-matters-content.md) - Prohibits corporate case studies, fabricated platform scenarios, and unsourced numeric claims in `**Why It Matters**:` sections of ayokoding-www tutorials; requires theoretical explanations only. Applies to all by-example and in-the-field content in both English and Indonesian. **Agents**: apps-ayokoding-www-by-example-maker, apps-ayokoding-www-in-the-field-maker, apps-ayokoding-www-by-example-checker, apps-ayokoding-www-in-the-field-checker, apps-ayokoding-www-by-example-fixer, apps-ayokoding-www-in-the-field-fixer

## Structure

Documentation organization frameworks, file naming, and project planning structure.

- [Agent Naming Convention](./structure/agent-naming.md) - Single exception-free filename rule for agent files in `.claude/agents/` and `.opencode/agents/`. Defines scope vocabulary, role vocabulary (maker, checker, fixer, dev, deployer, manager), and the audit command enforced by `repo-rules-checker`
- [App README vs Specs Convention](./structure/app-readme-vs-specs.md) - **Pilot** — Defines what content lives in app/infra READMEs vs `specs/`, the C4-aware five-folder spec tree shape, and the PM-readability contract for `specs/`
- [Governance Vendor-Independence Convention](./structure/governance-vendor-independence.md) - Requires all `repo-governance/` prose to be vendor-neutral. Defines forbidden vendor terms, the `binding-example` fence allowlist mechanism, vocabulary map (vendor → neutral replacements), and migration guidance for governance file rewrites. **Agents**: repo-rules-checker
- [Multi-Harness Binding Convention](./structure/multi-harness-binding.md) - Keeps one canonical root instruction surface while supporting many coding-agent harnesses. Defines the two-tier binding model (native readers vs. bridge-required), the no-shadowing rule, mechanical generation, and the deterministic pre-push parity guard. **Agents**: repo-harness-compatibility-checker, repo-harness-compatibility-fixer
- [Diataxis Framework](./structure/diataxis-framework.md) - Understanding the four-category documentation organization framework we use (Tutorials, How-To, Reference, Explanation)
- [File Naming Convention](./structure/file-naming.md) - Lowercase kebab-case file names anchored on standard markdown and GitHub compatibility
- [Learning-Plan `syllabus/` Folder Convention](./structure/learning-plan-syllabus.md) - Defines the learning-bearing plan trigger, the required `syllabus/courses/` + `syllabus/paths/` folder layout, measured section-tiering derivation, the copy-paste course template, `## Corpus Disposition` values, and the single-custodian custody rule for learning-path plans
- [No Last Updated Convention](./structure/no-last-updated.md) - **SUPERSEDED** — Stub redirecting to No Manual Date Metadata Convention
- [No Manual Date Metadata Convention](./structure/no-date-metadata.md) - Non-website markdown files must not contain manual date metadata: no `updated:` frontmatter fields, no `**Last Updated**` footer blocks, and no inline body date annotations. Git history is the authoritative change record. **Agents**: repo-rules-checker, repo-rules-fixer
- [Deterministic vs AI Validation Split](./structure/deterministic-vs-ai-validation-split.md) - Defines which governance validation categories run as deterministic preflight (mechanical predicates, milliseconds, cached) vs AI checker (semantic judgement) and the JSON envelope contract between the two layers. **Agents**: repo-rules-checker
- [Per-Directory Licensing](./structure/licensing.md) - Standards for the per-directory licensing strategy using MIT for all code in this repository. Defines LICENSE file placement rules, copyright notice format, and rules for new directories
- [Plans Organization](./structure/plans.md) - Standards for organizing project planning documents in plans/ folder including structure (ideas/, backlog/, in-progress/, done/), naming patterns (YYYY-MM-DD\_\_identifier/), lifecycle stages, and project identifiers. Defines how plans move from ideas → backlog → in-progress → done
- [Post-Mortem Convention](./structure/post-mortems.md) - Standards for blameless incident post-mortems: location (`docs/explanation/post-mortems/`), `YYYY-MM-DD-<system>-<short-failure>.md` naming, mandatory sections, the authoritative Sev-1..Sev-4 severity scale, action-item tracking, and `doc_status` lifecycle. Software-incident framing (CI/CD failures, Vercel outages, dependency-bump and parity-guard regressions)
- [Programming Language Documentation Separation](./structure/programming-language-docs-separation.md) - Establishes clear separation between repository-specific programming language style guides (docs/explanation/) and educational programming language content (ayokoding-www). Defines scope boundaries, prerequisite knowledge requirements, cross-referencing patterns, and DRY principle application. Applies to all programming languages (Java, Python, Golang, TypeScript, Elixir, Kotlin, Dart, Rust, Clojure, F#, C#)
- [Specs Directory Structure](./structure/specs-directory-structure.md) - Canonical directory structure for Gherkin feature files, C4 architecture diagrams, and OpenAPI contracts in the specs/ directory. Defines path patterns, domain subdirectory rules (required for BE/FE, flat for CLI), and lib spec organization
- [Workflow Naming Convention](./structure/workflow-naming.md) - Single exception-free filename rule for workflow files under `repo-governance/workflows/` (except `meta/` reference docs). Defines scope vocabulary, type vocabulary (quality-gate, execution, setup), and the audit command enforced by `repo-rules-checker` and `rhino-cli repo-governance workflows naming validate`
- [Worktree Path Convention](./structure/worktree-path.md) - Defines the worktree directory structure, naming convention, and gitignore requirements for `claude --worktree` routing

## Tutorials

Tutorial creation, structure, naming, and content standards applying to **all tutorial content** (docs/, ayokoding-www, ose-www, anywhere). These conventions **build upon and extend** the writing conventions above.

- [By Concept Tutorial](./tutorials/by-concept.md) - **Universal** standards for narrative-driven by-concept tutorials (Component 4 of Full Set Tutorial Package) achieving 95% coverage through comprehensive concept explanations. Applies to all programming language tutorials across the repository
- [By Example Tutorial](./tutorials/swe-by-example.md) - **Universal** standards for code-first by-example tutorials (Component 3 of Full Set Tutorial Package - PRIORITY) with 75-85 heavily annotated, self-contained, runnable examples achieving 95% coverage. Defines five-part example structure (brief explanation, optional Mermaid diagram, heavily annotated code with `// =>` notation, key takeaway), self-containment rules across beginner/intermediate/advanced levels, educational comment standards (1-2.25 ratio), and coverage progression (0-40%, 40-75%, 75-95%). Prioritized for fast learning ("move fast"). Applies to all programming language tutorials across the repository
- [Cookbook Tutorial](./tutorials/cookbook.md) - **Universal** standards for problem-focused cookbook tutorials (Component 5 of Full Set Tutorial Package) with 30+ practical, copy-paste ready recipes organized by problem type. Defines recipe structure (Problem - Solution - Explanation - Pitfalls - Related), lighter annotation density (0.5-1.5 vs 1-2.25), recipe independence (no required reading order), and cross-level applicability (useful for all skill levels). Complements both by-example and by-concept tracks. Applies to all programming language tutorials across the repository
- [Programming Language Content Standard](./tutorials/programming-language-content.md) - **Universal** Full Set Tutorial Package architecture for programming language education. Defines 5 mandatory components with by-example prioritized first (Component 3: code-first 75-85 examples for fast learning), by-concept second (Component 4: narrative-driven for deep learning), plus foundational tutorials, cookbook in tutorials/, and supporting docs. Coverage philosophy (0-30% foundational, 95% learning tracks), quality metrics, and completeness criteria. Applies to all programming language tutorials (docs/, ayokoding-www, anywhere). **See also**: [How to Add a Programming Language](../../docs/how-to/add-programming-language.md)
- [Programming Language Tutorial Structure](./tutorials/programming-language-structure.md) - **Universal** directory structure for Full Set Tutorial Package with 5 mandatory components: foundational tutorials (initial-setup, quick-start), by-example track (Component 3 - PRIORITY: code-first with 75-85 examples, 95% coverage, "move fast"), by-concept track (Component 4: narrative-driven, 95% coverage, "learn deep"), and cookbook (Component 5: practical recipes in tutorials/cookbook/). Defines navigation pattern (by-example first), weight values, and creation order. All 5 components required for complete language content. Applies to all programming language tutorials across the repository
- [Tutorial Convention](./tutorials/general.md) - **Universal** standards for creating learning-oriented tutorials with narrative flow, progressive scaffolding, and hands-on elements. Covers all 7 tutorial types that combine into Full Set Tutorial Package. Applies to all tutorial content (docs/, ayokoding-www, ose-www, anywhere)
- [Tutorial Naming](./tutorials/naming.md) - **Universal** Full Set Tutorial Package definition (5 mandatory components) and tutorial type standards (Initial Setup, Quick Start, Beginner, Intermediate, Advanced, Cookbook, By Example). Replaces old "Full Set" concept (5 sequential levels) with new architecture emphasizing component completeness. Applies to all tutorial content across the repository
- [In-the-Field Tutorial Convention](./tutorials/in-the-field.md) - **Universal** standards for production-ready implementation guides that build on by-example and by-concept foundations by introducing frameworks, libraries, and enterprise patterns used in real-world systems. Targets developers ready to apply concepts in production environments. Applies to all in-the-field tutorial content across the repository

## Security

Security conventions governing how agents and contributors interact with sensitive repository artifacts.

- [No Secrets in Git](./security/no-secrets-in-committed-files.md) - The hard iron rule: no system secret (SSH/private keys, passwords, API tokens, privileged usernames, certificates, connection strings, and similar) may ever be committed to any git-tracked file. Real secret values belong in uncommitted `.env*` files (except `.env.example`) or other gitignored files. The broad governing rule that `guard-env-file-access` partially enforces. **Agents**: repo-rules-checker, repo-rules-fixer
- [Environment File Access](./security/env-file-access.md) - The `guard-env-file-access` policy. AI agents must not directly read, write, edit, or commit any `.env*` file except `.env.example`. Covers the script carve-out, trust boundary, git-commit prevention (gitignore + pre-commit guard), cross-platform enforcement paths, and known gaps with accepted compensating controls. **Agents**: repo-rules-checker, repo-rules-fixer

## Related Documentation

- [Repository Governance Architecture](../repository-governance-architecture.md) - Complete six-layer architecture (Layer 2: Conventions)
- [Core Principles](../principles/README.md) - Layer 1: Foundational values that govern conventions
- [Development](../development/README.md) - Layer 3: Software practices (parallel governance with conventions)
- [Software Design Reference](../../docs/explanation/software-engineering/software-design-reference.md) - Cross-reference to authoritative software design and coding standards
