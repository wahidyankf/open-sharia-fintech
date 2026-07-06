# Claude Code Agents

This directory contains specialized AI agents for the open-sharia-enterprise project. These agents are organized by role and follow the Maker-Checker-Fixer pattern where applicable.

## Agent Organization

### 🟦 Content Creation (Makers)

- **[docs-maker](docs-maker.md)** - Expert documentation writer
- **[docs-tutorial-maker](docs-tutorial-maker.md)** - Tutorial creation specialist
- **[readme-maker](readme-maker.md)** - README file writer
- **[apps-ayokoding-www-general-maker](apps-ayokoding-www-general-maker.md)** - General content for AyoKoding
- **[apps-ayokoding-www-by-example-maker](apps-ayokoding-www-by-example-maker.md)** - By-example tutorials
- **[apps-ayokoding-www-in-the-field-maker](apps-ayokoding-www-in-the-field-maker.md)** - In-the-field tutorials for AyoKoding
- **[apps-ose-www-content-maker](apps-ose-www-content-maker.md)** - OSE Platform content
- **[pdf-to-md-maker](pdf-to-md-maker.md)** - PDF to verbatim Markdown conversion (text-based and image-only via OCR)
- **[plan-maker](plan-maker.md)** - Project plan creation
- **[repo-rules-maker](repo-rules-maker.md)** - Governance document creation
- **[repo-workflow-maker](repo-workflow-maker.md)** - Workflow documentation
- **[specs-maker](specs-maker.md)** - Spec area scaffolding and feature file creation
- **[social-linkedin-post-maker](social-linkedin-post-maker.md)** - LinkedIn content creation
- **[agent-maker](agent-maker.md)** - Agent definition creation
- **[swe-ui-maker](swe-ui-maker.md)** - UI component creation
- **[pr-review-maker](pr-review-maker.md)** - Posts adversarial code-review findings on a GitHub PR via the GitHub Reviews API (SHA-pinned, confidence-scored); the maker half of the PR-Review Maker→Fixer Cycle for `*-to-pr` delivery-mode plans

### 🟩 Validation (Checkers)

- **[docs-checker](docs-checker.md)** - Factual accuracy validation
- **[docs-tutorial-checker](docs-tutorial-checker.md)** - Tutorial quality validation
- **[docs-link-checker](docs-link-checker.md)** - Link validity checking
- **[docs-software-engineering-separation-checker](docs-software-engineering-separation-checker.md)** - Programming language docs separation validation
- **[readme-checker](readme-checker.md)** - README quality validation
- **[apps-ayokoding-www-general-checker](apps-ayokoding-www-general-checker.md)** - General content validation
- **[apps-ayokoding-www-by-example-checker](apps-ayokoding-www-by-example-checker.md)** - By-example validation
- **[apps-ayokoding-www-in-the-field-checker](apps-ayokoding-www-in-the-field-checker.md)** - In-the-field content validation
- **[apps-ayokoding-www-facts-checker](apps-ayokoding-www-facts-checker.md)** - Factual accuracy for AyoKoding
- **[apps-ayokoding-www-link-checker](apps-ayokoding-www-link-checker.md)** - Link validation for AyoKoding
- **[apps-ose-www-content-checker](apps-ose-www-content-checker.md)** - OSE content validation
- **[pdf-to-md-checker](pdf-to-md-checker.md)** - PDF-to-Markdown fidelity validation (text completeness, tables, figures, Mermaid, OCR quality)
- **[plan-checker](plan-checker.md)** - Project plan validation
- **[plan-execution-checker](plan-execution-checker.md)** - Plan execution validation
- **[repo-setup-manager](repo-setup-manager.md)** - Phase 0 environment setup and baseline for every plan delivery (installs dependencies, converges polyglot toolchain, resolves preexisting failures)
- **[repo-rules-checker](repo-rules-checker.md)** - Governance compliance validation
- **[repo-workflow-checker](repo-workflow-checker.md)** - Workflow documentation validation
- **[repo-harness-compatibility-checker](repo-harness-compatibility-checker.md)** - Validates cross-vendor parity invariants (Phase 0, deterministic) and detects external harness drift (Phase 1, web-research-backed)
- **[specs-checker](specs-checker.md)** - Gherkin/BDD specs directory structural and content validation
- **[swe-code-checker](swe-code-checker.md)** - Validates projects against platform coding standards (validates application code rather than documentation)
- **[swe-ui-checker](swe-ui-checker.md)** - UI component quality validation
- **[ci-checker](ci-checker.md)** - CI/CD standards validation (mandatory Nx targets, coverage thresholds, Docker setup, Gherkin specs)

### 🟨 Fixing (Fixers)

- **[docs-file-manager](docs-file-manager.md)** - File organization and management
- **[docs-fixer](docs-fixer.md)** - Apply validated documentation fixes
- **[docs-tutorial-fixer](docs-tutorial-fixer.md)** - Apply tutorial fixes
- **[docs-software-engineering-separation-fixer](docs-software-engineering-separation-fixer.md)** - Fix programming language docs separation issues
- **[readme-fixer](readme-fixer.md)** - Apply README fixes
- **[apps-ayokoding-www-general-fixer](apps-ayokoding-www-general-fixer.md)** - Apply general content fixes
- **[apps-ayokoding-www-by-example-fixer](apps-ayokoding-www-by-example-fixer.md)** - Apply by-example fixes
- **[apps-ayokoding-www-in-the-field-fixer](apps-ayokoding-www-in-the-field-fixer.md)** - Fix in-the-field content issues
- **[apps-ayokoding-www-facts-fixer](apps-ayokoding-www-facts-fixer.md)** - Apply factual corrections
- **[apps-ayokoding-www-link-fixer](apps-ayokoding-www-link-fixer.md)** - Fix broken links
- **[apps-ose-www-content-fixer](apps-ose-www-content-fixer.md)** - Fix OSE content issues
- **[pdf-to-md-fixer](pdf-to-md-fixer.md)** - Apply validated PDF-to-Markdown fixes (re-extracts missing content from PDF source)
- **[plan-fixer](plan-fixer.md)** - Apply plan fixes
- **[repo-rules-fixer](repo-rules-fixer.md)** - Fix governance compliance issues
- **[repo-workflow-fixer](repo-workflow-fixer.md)** - Fix workflow documentation
- **[repo-harness-compatibility-fixer](repo-harness-compatibility-fixer.md)** - Apply validated parity and harness-compatibility fixes; auto-remediates binding-sync drift; updates specs/apps/rhino/ when harness changes alter documented CLI behavior
- **[specs-fixer](specs-fixer.md)** - Fix specs structural and accuracy issues
- **[swe-ui-fixer](swe-ui-fixer.md)** - Apply validated UI component fixes
- **[ci-fixer](ci-fixer.md)** - Apply validated CI/CD standards fixes
- **[pr-review-fixer](pr-review-fixer.md)** - Triages and resolves `pr-review-maker` findings on a GitHub PR (fix / reject-with-reason / defer-with-reason / clarify), replying to and resolving review threads; the fixer half of the PR-Review Maker→Fixer Cycle

### 🔍 Research (Green)

- **[web-researcher](web-researcher.md)** - Read-only web research specialist; returns cited, structured findings with confidence tags in an isolated context (no file writes, no shell). Invoke for current API/library docs, fact verification, best-practice surveys.

### 🧪 Testing

- **[web-exploratory-tester](web-exploratory-tester.md)** - **Spec-aware** session-based exploratory testing of a live site against a goal; actively hunts edge cases and boundary conditions; files findings (functional, behavioural consistency, edge-case/boundary, UI/responsive, accessibility, performance, URL/IA quality, safe security surface) as a new backlog plan (README + brd + prd + findings + spec-gaps with steps-to-reproduce). Compares live behaviour against existing `specs/**` Gherkin and proposes new scenarios (Gherkin) for correct behaviours — especially edge cases — that lack coverage. Non-destructive; does not modify the site or fix code. Supports selectable output modes: `plan` (default — files a new backlog plan), `delivery` (appends findings into an existing plan's `delivery.md`, the rule-15 retest mechanism), `local-temp` (throwaway findings for direct fixing).
- **[web-usability-tester](web-usability-tester.md)** - **Spec-blind** heuristic usability evaluation of a live site; judges only what a first-time user perceives (deliberately ignores specs/source/mockups) against established usability principles (Nielsen's 10 heuristics + 0–4 severity, cognitive walkthrough, information scent, first-click, Jakob's Law, ISO 9241-110, WCAG Understandable, UX laws). Evaluates predictability, internal/external consistency, information scent & flow, cognitive load, edge-case UX states (empty/loading/error), responsive usability (mobile/tablet/desktop), and URL/IA naturalness. Files findings as a backlog plan (README + brd + prd + findings + walkthrough + spec-suggestions). Suggests new behaviour for `specs/**` in Gherkin (spec-blind `USS-###` candidates, flagged for reconciliation — distinct from exploratory's spec-gaps). Distinct from web-exploratory-tester (correctness); non-destructive. Supports selectable output modes: `plan` (default — files a new backlog plan), `delivery` (appends findings into an existing plan's `delivery.md`, the rule-15 retest mechanism), `local-temp` (throwaway findings for direct fixing).
- **[web-design-tester](web-design-tester.md)** - **Design-aware** design-fidelity evaluation of a live site; judges whether the **running** rendered page matches its design and follows good design practice against five ground-truth sources (committed plan-folder mockups, design tokens/theme at runtime, design-system primitives `libs/web-ui`, an optional external Figma/mockup source passed at invocation, and general design best-practice grounded by `web-researcher`). Evaluates mockup fidelity, runtime token/theme fidelity, design-system-primitive reuse, visual hierarchy, alignment, spacing/density (not cramped), typography, colour, and cross-surface visual consistency. Files `DWT-###` findings as a backlog plan (README + brd + prd + findings + spec-gaps), locale- and evidence-aware. The **runtime** counterpart to `swe-ui-checker`'s **static** source audit, with no overlap. Distinct from web-exploratory-tester (correctness) and web-usability-tester (usability); non-destructive. Supports selectable output modes: `plan` (default — files a new backlog plan), `delivery` (appends findings into an existing plan's `delivery.md`, the rule-15 retest mechanism), `local-temp` (throwaway findings for direct fixing).
- **[api-exploratory-tester](api-exploratory-tester.md)** - **Spec-aware, contract-aware** session-based exploratory testing of a live **REST or GraphQL** API against a goal; HTTP/curl-driven, **never** a browser. Actively hunts edge cases and boundary conditions (payloads, status codes, error envelopes, auth/authz, pagination, idempotency, GraphQL nullability/partial-errors/depth). Compares live responses against both the **API contract** (OpenAPI 3.x spec or GraphQL SDL) and existing `specs/**` Gherkin; proposes new scenarios (Gherkin) for correct behaviours — especially edge cases — that lack coverage. Files `AET-###` findings as a new backlog plan (README + brd + prd + findings + spec-gaps with exact `curl`/GraphQL steps-to-reproduce, secrets redacted). The **API-surface** counterpart to the rendered-UI web tester triad, with no overlap (it never audits HTML/CSS/visual/responsive concerns). Non-destructive (read-only by default; state-changing requests only with explicit per-run authorization). Supports selectable output modes: `plan` (default — files a new backlog plan), `delivery` (appends findings into an existing plan's `delivery.md`, the rule-15 retest mechanism), `local-temp` (throwaway findings for direct fixing).

### 🟪 Operations

- **[apps-ayokoding-www-deployer](apps-ayokoding-www-deployer.md)** - AyoKoding marketing site deployment (`prod-ayokoding-www`, Next.js via Vercel)
- **[apps-ose-www-deployer](apps-ose-www-deployer.md)** - OSE Platform marketing site deployment (`prod-ose-www`)
- **[apps-organiclever-www-deployer](apps-organiclever-www-deployer.md)** - OrganicLever marketing site deployment (`prod-organiclever-www`)
- **[apps-organiclever-app-web-deployer](apps-organiclever-app-web-deployer.md)** - OrganicLever app-group staging deployment (`stag-organiclever-app-web` + `stag-organiclever-be`; prod CD deferred)
- **[apps-ose-app-web-deployer](apps-ose-app-web-deployer.md)** - OSE Application app-group staging deployment (`stag-ose-app-web` + `stag-ose-be`; prod CD deferred)
- **[apps-wahidyankf-www-deployer](apps-wahidyankf-www-deployer.md)** - wahidyankf portfolio deployment (`prod-wahidyankf-www`, Next.js via Vercel)
- **[apps-web-ui-storybook-deployer](apps-web-ui-storybook-deployer.md)** - web-ui Storybook deployment to Vercel via `prod-web-ui` force-push

### 💻 Development

- **[swe-csharp-dev](swe-csharp-dev.md)** - C# application development
- **[swe-e2e-dev](swe-e2e-dev.md)** - E2E testing with Playwright
- **[swe-fsharp-dev](swe-fsharp-dev.md)** - F# application development
- **[swe-golang-dev](swe-golang-dev.md)** - Go application development
- **[swe-rust-dev](swe-rust-dev.md)** - Rust application development
- **[swe-typescript-dev](swe-typescript-dev.md)** - TypeScript application development

## Naming Rule

Every agent filename follows: `<scope>(-<qualifier>)*-<role>`

- `scope` — top-level domain (`agent`, `apps`, `ci`, `docs`, `pdf-to-md`, `plan`, `readme`, `repo`, `social`, `specs`, `swe`, `web`).
- `qualifier` — zero or more refinement tokens (e.g., `ayokoding-web`, `link`, `ui`, `execution`).
- `role` — exactly one trailing token from the Role Vocabulary below.

No other structure is permitted. No exceptions.

Normative source: [Agent Naming Convention](../../repo-governance/conventions/structure/agent-naming.md).

## Role Vocabulary

| Role         | Semantics                                                                              | Example agents                                                                                  |
| ------------ | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `maker`      | Produces a content/research artifact                                                   | `docs-maker`, `docs-tutorial-maker`                                                             |
| `checker`    | Validates an artifact against standards                                                | `plan-checker`, `plan-execution-checker`, `swe-code-checker`                                    |
| `fixer`      | Applies validated checker findings                                                     | `plan-fixer`, `swe-ui-fixer`                                                                    |
| `dev`        | Writes code in a language or test framework                                            | `swe-rust-dev`, `swe-e2e-dev`                                                                   |
| `deployer`   | Deploys an application to an environment                                               | `apps-ayokoding-www-deployer`                                                                   |
| `manager`    | Performs file or resource operations (rename/move/delete)                              | `docs-file-manager`                                                                             |
| `tester`     | Explores or evaluates a running system, live site, or API and reports defects/friction | `web-exploratory-tester`, `web-usability-tester`, `web-design-tester`, `api-exploratory-tester` |
| `researcher` | Gathers and verifies external information; read-only research                          | `web-researcher`                                                                                |

Enforcement: `rhino-cli agents validate-naming` (wired into pre-push and CI).

## Agent Format (Claude Code)

Agents use YAML frontmatter with the following structure:

```yaml
---
name: agent-name
description: Expert in X specializing in Y. Use when Z.
tools: Read, Glob, Grep
model:
color: blue
skills: []
---
```

**Name**: Required field - unique identifier using lowercase letters and hyphens
**Description**: Required field - when Claude should delegate to this agent
**Tools**: Comma-separated string with capitalized tool names (only tools the agent needs)
**Model**: Required field - omit for opus (default), or use \`sonnet\` or \`haiku\`. Opus-tier agents omit `model` by design (budget-adaptive — inherits session model). Do not add `model: opus`.
**Color**: Required field - `blue` (makers), `green` (checkers), `yellow` (fixers), `purple` (implementors)
**Skills**: Required field - list of Skill names (empty array `[]` if no Skills used)

Note: Frontmatter MUST NOT contain YAML inline comments (# symbols). Put explanations in the document body.

### Model Benchmark Context

Benchmark scores supporting tier assignments are documented in
[docs/reference/ai-model-benchmarks.md](../../docs/reference/ai-model-benchmarks.md).
Opus-tier agents omit the `model` field by design — they inherit the session's active
model (Max/Team Premium → Opus 4.7; Pro/Standard → Sonnet 4.6). Do NOT add `model: opus`.

## Maker-Checker-Fixer Pattern

Three-stage quality workflow:

1. **Maker** (🟦 Blue) - Creates content
2. **Checker** (🟩 Green) - Validates content, generates audit reports
3. **Fixer** (🟨 Yellow) - Applies validated fixes

**Criticality Levels**: CRITICAL, HIGH, MEDIUM, LOW
**Confidence Levels**: HIGH, MEDIUM, FALSE_POSITIVE

## Dual-Mode Operation

**Source of Truth**: This directory (`.claude/agents/`) is the PRIMARY source.
**Sync Target**: Changes are synced to `.opencode/agents/` (SECONDARY) via automation.

**Making Changes**:

1. Edit agents in `.claude/agents/` directory
2. Run: `npm run generate:bindings` (powered by `rhino-cli` for fast syncing)
3. Both systems stay synchronized

**Implementation**: Sync powered by `rhino-cli agents sync` (~121ms, 25-60x faster than bash)

**See**: [CLAUDE.md](../../CLAUDE.md) for complete guidance, [AGENTS.md](../../AGENTS.md) for OpenCode documentation, [apps/rhino-cli/README.md](../../apps/rhino-cli/README.md) for rhino-cli details

## Skills Integration

Agents leverage skills from `.claude/skills/` for progressive knowledge delivery. Skills are NOT agents - they provide reusable knowledge and execution services to agents.

**See**: [.claude/skills/README.md](../skills/README.md) for complete skills catalog

## Governance Standards

All agents follow governance principles:

- **Documentation First** - Documentation is mandatory, not optional
- **Explicit Over Implicit** - Clear tool permissions, no magic
- **Simplicity Over Complexity** - Single-purpose agents, minimal abstraction
- **Accessibility First** - WCAG AA compliance in all outputs

**See**: [repo-governance/principles/README.md](../../repo-governance/principles/README.md)
