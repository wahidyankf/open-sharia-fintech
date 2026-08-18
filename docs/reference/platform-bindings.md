---
title: "Platform Bindings Catalog"
description: Catalog of all AI coding agent platform bindings in ose-public, their directories, root instruction files, and mechanical translation artifacts.
category: reference
created: 2026-05-02
---

# Platform Bindings Catalog

This reference catalogs every AI coding agent platform binding in this repository: where it lives,
what root instruction file it reads, its current status, and what mechanical translations exist
between bindings.

A **platform binding** is the platform-specific directory and configuration that wires an AI coding
agent to this repository. Governance prose lives in `repo-governance/` (vendor-neutral). Platform
bindings live in their own directories and are explicitly excluded from the
[Governance Vendor-Independence Convention](../../repo-governance/conventions/structure/governance-vendor-independence.md).

## Platform Binding Directories

The table below catalogs all nine named coding-agent harnesses plus OpenCode. Columns record every
surface each harness exposes so contributors know exactly which files to create or extend when
adding support for a given tool.

**Verified 2026-05-24.**

| Platform                                                | Reads root `AGENTS.md` natively?                                                                                                                                                       | Tool-specific instruction surface                                                                              | Project MCP config                                                                              | Custom-agent surface                                                                                                | Skills surface                            | Status                                                   |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- | -------------------------------------------------------- |
| Claude Code                                             | No — reads `CLAUDE.md` (shim `@AGENTS.md`)                                                                                                                                             | `CLAUDE.md`, `.claude/`                                                                                        | `.mcp.json`                                                                                     | `.claude/agents/*.md`                                                                                               | `.claude/skills/*/SKILL.md`               | Active                                                   |
| OpenCode                                                | Yes                                                                                                                                                                                    | `.opencode/agents/` (auto-synced); reads `.claude/skills/` natively                                            | `opencode.json`                                                                                 | `.opencode/agents/*.md`                                                                                             | reads `.claude/skills/`                   | Active                                                   |
| OpenAI Codex CLI                                        | Yes (since Apr 2025)                                                                                                                                                                   | `AGENTS.override.md` (overrides), `.codex/config.toml`                                                         | `.codex/config.toml` `[mcp_servers]`                                                            | `[agents.<name>]` in `config.toml` (with optional `config_file` pointer to a TOML layer, e.g. `.codex/<name>.toml`) | `.agents/skills/`                         | Partial (`.codex/` exists)                               |
| GitHub Copilot                                          | Yes (nearest file wins)                                                                                                                                                                | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`                                    | `.vscode/mcp.json`                                                                              | `.github/agents/*.agent.md`                                                                                         | n/a                                       | Reserved (reads root `AGENTS.md`; `.github/` is CI-only) |
| Cursor                                                  | Yes                                                                                                                                                                                    | `.cursor/rules/*.mdc` (+ legacy `.cursorrules`)                                                                | `.cursor/mcp.json`                                                                              | `.cursor/agents/*.md` (generated from `.claude/agents/`)                                                            | `.cursor/skills/`                         | Active (generated agent surface)                         |
| Windsurf                                                | Yes                                                                                                                                                                                    | `.windsurf/rules/*.md`, `.windsurf/workflows/`                                                                 | global only                                                                                     | not officially documented                                                                                           | `.windsurf/skills/` (unverified)          | Reserved                                                 |
| JetBrains Junie                                         | Yes — `.junie/AGENTS.md` outranks root `AGENTS.md`                                                                                                                                     | `.junie/AGENTS.md`, `.junie/rules/*.md` (imports `.claude/agents/`, `.codex/agents/`, `.claude/skills/`)       | `.junie/mcp/mcp.json`                                                                           | `.junie/agents/`, `.agents/`                                                                                        | `.junie/skills/<name>/SKILL.md`           | Reserved                                                 |
| Amazon Q Developer (superseded by Kiro CLI — see below) | Q Developer CLI: No (feature request #2712, still open and never resolved for that product). **Kiro CLI: Yes** — `AGENTS.md` at workspace root or `~/.kiro/steering/`, always included | Q Developer: `.amazonq/rules/*.md` (via agent JSON `resources`) → Kiro: `.kiro/steering/`, `~/.kiro/steering/` | Q Developer: `.amazonq/mcp.json` → Kiro: `.kiro/settings/mcp.json`, `~/.kiro/settings/mcp.json` | Q Developer: JSON in `.amazonq/` / `~/.aws/amazonq/cli-agents/` → Kiro: `.kiro/agents/`, `~/.kiro/agents/`          | Q Developer: none → Kiro: `.kiro/skills/` | Sunsetting (IDE plugins EOS 2027-04-30)                  |
| Google Antigravity CLI                                  | Yes (since v1.20.3) — `GEMINI.md` outranks `AGENTS.md`                                                                                                                                 | `GEMINI.md` (overrides), `.agent/rules/*.md`                                                                   | `~/.gemini/antigravity/mcp_config.json` (global; no confirmed project-level path)               | runtime-orchestrated (no declarative file)                                                                          | `.agents/skills/<name>/SKILL.md`          | Reserved                                                 |
| Pi (pi.dev)                                             | Yes (also reads `CLAUDE.md`)                                                                                                                                                           | `.pi/settings.json`, `.pi/AGENTS.md`, `.pi/SYSTEM.md`                                                          | none (intentionally no native MCP)                                                              | none built-in (extension-based)                                                                                     | `.agents/skills/` or `.pi/skills/`        | Reserved                                                 |
| Aider                                                   | Requires explicit opt-in — `aider --read AGENTS.md` or `.aider.conf.yml`; AGENTS.md standard site lists support but Aider does not auto-discover any instruction file                  | `CONVENTIONS.md` (requires explicit `--read` or `.aider.conf.yml`; not auto-loaded)                            | n/a                                                                                             | n/a                                                                                                                 | n/a                                       | Reserved (`CONVENTIONS.md` not yet provided)             |

### Root instruction file hierarchy

Platforms that read `AGENTS.md` natively require no additional binding directory — the native read
is sufficient. Platforms that predate the `AGENTS.md` standard (or that require a harness-specific
entry point) receive either a shim that imports `AGENTS.md` (Claude Code's `CLAUDE.md`) or a
generated bridge file.

Some harnesses rank a tool-specific file **above** `AGENTS.md` when both are present. Those files
must never carry content that diverges from `AGENTS.md`. See the
[No-shadowing note](#no-shadowing-note) below.

> **Note on Gemini CLI**: The former "Gemini CLI" row referred to the standalone Gemini CLI tool,
> which was superseded in 2026 by the Google Antigravity CLI (which bundles Gemini model access
> alongside broader agent orchestration). The Antigravity CLI reads `AGENTS.md` natively since
> v1.20.3. All previous "Gemini CLI" entries in this document are replaced by the "Google Antigravity
> CLI" row above.

### Provenance of pre-existing partial bindings

One binding-adjacent directory exists in the repository but was **not produced by `rhino-cli agents
sync`**:

- **`.codex/config.toml`** — Provided by the OpenAI Codex CLI tooling. It configures the
  `nx-mcp` MCP server for Codex and declares the `ci-monitor-subagent` agent entry as an
  `[agents.<name>]` sub-table whose `config_file` points to `.codex/ci-monitor-subagent.toml`.
  The former `.codex/agents/` directory was removed (2026-06-06): it was never an official
  Codex CLI convention — the official per-agent mechanism is `config.toml` `agents.<name>`
  sub-tables — and `rhino-cli harness bindings validate` now fails if `.codex/agents/`
  reappears. These files are Codex/Nx infrastructure — not
  hand-authored custom agents produced by this repo's pipeline. `rhino-cli harness bindings generate` does
  not write to `.codex/` and will not clobber these files.

`.github/` holds only the in-repo CI surface — GitHub Actions `workflows/` and composite `actions/`,
hand-authored in this repo. The Nx MCP tooling's Copilot artifacts that previously lived there (the
`nx-*` agent skills under `.github/skills/`, plus the CI-monitor `.github/agents/ci-monitor-subagent.agent.md`
and `.github/prompts/monitor-ci.prompt.md`) were removed; the repo reads Nx skills via the `nx-mcp`
plugin and monitors CI via the `gh` CLI.

The `.codex` files are safe to leave in place; they serve the Nx CI-monitoring capability and do not
affect the canonical `AGENTS.md` instruction surface.

### Generated Amazon Q Developer bridge

Amazon Q Developer does not read the canonical `AGENTS.md` natively (open feature request #2712), so
its instruction surface is generated mechanically by `rhino-cli harness bindings generate`:

- **`.amazonq/rules/00-agents-md.md`** — a pointer file (not a copy) directing Amazon Q to read and
  follow `AGENTS.md` at the repository root.
- **`.amazonq/cli-agents/ose-default.json`** — a minimal Amazon Q agent definition whose `resources`
  load `file://AGENTS.md` and `file://.amazonq/rules/**/*.md`.

These files are deterministic and idempotent — never hand-edit them. The companion guard
`rhino-cli harness bindings validate` enforces byte-for-byte parity against the generator and runs in
the pre-push pipeline. The same guard asserts that every present binding directory under `.amazonq`,
`.claude`, `.opencode`, `.codex`, and `.github` is referenced in this catalog.

### Amazon Q Developer CLI → Kiro CLI succession

**Verified 2026-07-20 against AWS and Kiro primary sources.** This transition is in progress through
April 2027; re-check as the milestones below pass.

AWS has **rebranded the Amazon Q Developer CLI to Kiro CLI** ("The Amazon Q Developer CLI has been
rebranded to Kiro" —
[AWS docs](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/upgrade-to-kiro.html)). Sunset
milestones, from the
[Amazon Q Developer end-of-support announcement](https://aws.amazon.com/blogs/devops/amazon-q-developer-end-of-support-announcement/):

- **2026-05-15** — new sign-ups for Amazon Q Developer no longer available.
- **2026-05-29** — Opus 4.6 no longer available on Q Developer Pro. Opus 4.5 and other existing
  models remain; the latest coding models (including Opus 4.7) are available **exclusively on
  Kiro**.
- **2027-04-30** — Amazon Q Developer IDE plugins and paid subscriptions reach end of support,
  giving a 12-month transition window.

**The `AGENTS.md` situation reversed.** Amazon Q Developer CLI did not read `AGENTS.md` natively, and
[feature request #2712](https://github.com/aws/amazon-q-developer-cli/issues/2712) remains open —
never resolved for that product. **Kiro CLI supports the `AGENTS.md` standard natively**: files at
the workspace root or in `~/.kiro/steering/` are picked up automatically and are **always included**,
unlike custom steering files ([Kiro steering docs](https://kiro.dev/docs/cli/steering/)). Workspace
scope overrides global on conflict. Note that **custom (non-default) Kiro agents do not auto-include
steering** — they need an explicit `{"resources": ["file://.kiro/steering/**/*.md"]}` entry.

Kiro CLI orchestration capabilities relevant to this repo's N+1 model
([Kiro subagents docs](https://kiro.dev/docs/cli/chat/subagents/)):

- **Native DAG task-graphs** — "Subagents support breaking down complex tasks into a directed
  acyclic graph (DAG) where tasks can depend on each other"; independent tasks run in parallel while
  dependent ones gate on their dependencies.
- **Up to four concurrent subagents** — "The main agent can spawn up to four subagents at once."
- **Isolation is context-level, not git-worktree-level.** Kiro's own docs describe each subagent
  getting "its own isolated context" and say nothing about git worktrees. Worktree-based isolation
  for Kiro exists only as a **third-party** orchestration pattern (e.g. the community
  [`requix/kiro-team`](https://github.com/requix/kiro-team) project), not as a first-party feature.
- **`q` and `q chat` are preserved** — "All the functionality in Amazon Q Developer CLI is available
  in Kiro CLI", though `kiro-cli` is the recommended entry point.
- **Config auto-migrates on upgrade** — agents and prompts from `~/.aws/amazonq` copy to `~/.kiro`,
  `~/.aws/amazonq/mcp.json` to `~/.kiro/settings/mcp.json`, and the `rules` folder to
  `~/.kiro/steering` ([migration guide](https://kiro.dev/docs/cli/migrating-from-q/)).

**Implication for this repo's bridge**: the generated `.amazonq/` bridge above exists because Q
Developer could not read `AGENTS.md`. Kiro can. The bridge stays for now — it still serves Q
Developer users through the 2027-04-30 end-of-support date — but once this repo targets Kiro rather
than Q Developer, the bridge becomes redundant and `.amazonq/` can be retired in favour of Kiro's
native `AGENTS.md` read. That retirement is a separate, deliberate change, not a side effect of this
catalog update.

### No-shadowing note

Some harnesses rank a tool-specific file **above** the canonical `AGENTS.md` when both files are
present in the repository. These higher-precedence files silently override `AGENTS.md` for that
tool only, producing divergent behavior invisible to contributors using any other harness.

The following files trigger this rule:

- `AGENTS.override.md` — OpenAI Codex CLI ranks this above `AGENTS.md` when present.
- `.junie/AGENTS.md` — JetBrains Junie ranks this above the root `AGENTS.md`.
- `GEMINI.md` — Google Antigravity CLI ranks this above `AGENTS.md` when present.

**The repo's default is not to create any of these files.** If a future operational need forces one
to exist, it must be implemented as a pure pointer or import directive referencing `AGENTS.md` —
never as a file with independent prose. Any exception must be recorded in this catalog with an
explicit justification.

See [Multi-Harness Binding Convention](../../repo-governance/conventions/structure/multi-harness-binding.md)
for the full no-shadowing rule (Rule 3 / AD3) and the two-tier binding model that governs all
harness integrations.

### Optional thin pointers

Tier-1 harnesses (Cursor, Windsurf, JetBrains Junie, GitHub Copilot, OpenAI Codex CLI, Google
Antigravity CLI, Pi, OpenCode) read the root `AGENTS.md` natively, so they need no tool-specific
instruction file to receive the canonical instructions.

**Decision: the repo ships no optional thin pointer files** (e.g., `.github/copilot-instructions.md`,
`.cursor/rules/*.mdc`, `.windsurf/rules/*.md`) by default. Rationale: each would be either redundant
(the native `AGENTS.md` read already applies) or a drift/shadowing risk. Only the Tier-2 Amazon Q
bridge is generated, because Amazon Q does not read `AGENTS.md` natively. If a thin pointer is added
later, it must be a pure `AGENTS.md` pointer emitted by `rhino-cli harness bindings generate` and covered
by `rhino-cli harness bindings validate`.

**Amended for the agent surface only (2026-07-28):** the standing "no thin pointer files" decision
is amended for the agent surface only — `.cursor/agents/` is generated from `.claude/agents/` and is
not an instruction-surface thin pointer. The instruction surface (rules, `AGENTS.md` read) is unchanged;
no `.cursor/rules/*.mdc` files are shipped by default.

**Why the generator flattens `.claude/agents/` mirrors:** Claude Code scans `.claude/agents/`
recursively and derives agent identity from the `name` frontmatter key, not the path
([docs](https://code.claude.com/docs/en/sub-agents)). OpenCode does **not** — its maintainers closed
the subdirectory feature request as _not planned_
([opencode#6635](https://github.com/anomalyco/opencode/issues/6635)). Any future reorganization of
`.claude/agents/` into subfolders is safe only because `rhino-cli harness bindings generate` flattens
every generated mirror; a mirror consumer that assumed the source shape would break silently.

## Translation Artifacts

Mechanical translations that platform bindings apply when generating output from upstream sources.
All translations are performed by `rhino-cli harness bindings generate` (`npm run generate:bindings`).

### Color Translation (Claude Code → OpenCode)

The Claude Code binding uses named color strings (`blue`, `green`, `yellow`, `purple`, etc.) in
agent frontmatter. OpenCode uses theme tokens (`primary`, `success`, `warning`, `secondary`, etc.).

- **Source**: `.claude/agents/<name>.md` frontmatter `color:` field
- **Transform**: `convert_color` in `apps/rhino-cli/src/internal/agents/converter.rs`
- **Sink**: `.opencode/agents/<name>.md` frontmatter `color:` field
- **Policy**: [Platform Binding Color Translation](../../repo-governance/development/agents/ai-agents/agent-color-categorization.md#platform-binding-color-translation)
  ("Platform Binding Color Translation" subsection)

| Claude Code color | OpenCode theme token | Role hint            |
| ----------------- | -------------------- | -------------------- |
| `blue`            | `primary`            | Maker agents         |
| `green`           | `success`            | Checker agents       |
| `yellow`          | `warning`            | Fixer agents         |
| `purple`          | `secondary`          | Executor agents      |
| `red`             | `error`              | Critical/alert       |
| `orange`          | `warning`            | (maps to warning)    |
| `pink`            | `accent`             | Reserved future role |
| `cyan`            | `info`               | Informational        |
| unrecognized/hex  | passed through       | Escape hatch         |

### Model ID Translation (Claude Code → OpenCode)

Claude Code agent frontmatter uses short aliases (`sonnet`, `haiku`) or omits `model:` for
planning-grade inheritance. OpenCode uses Zhipu AI GLM model IDs.

- **Source**: `.claude/agents/<name>.md` frontmatter `model:` field
- **Transform**: `convert_model` in `apps/rhino-cli/src/internal/agents/converter.rs`
- **Sink**: `.opencode/agents/<name>.md` frontmatter `model:` field
- **Policy**: [Model Selection Convention](../../repo-governance/development/agents/model-selection.md)
  ("Platform Binding Examples" section)

| Claude Code alias       | OpenCode model ID         | Capability tier                     |
| ----------------------- | ------------------------- | ----------------------------------- |
| `opus`                  | `zai-coding-plan/glm-5.2` | Thinking (collapsed onto execution) |
| `sonnet`/omit (inherit) | `zai-coding-plan/glm-5.2` | Execution                           |
| `haiku`                 | `zai-coding-plan/glm-5.2` | Fast (collapsed onto execution)     |

### Model ID Translation (Claude Code → Cursor)

Cursor agent frontmatter uses Cursor-native model IDs. The emitter implements **full tier collapse**
onto the non-fast Composer 2.5 identifier — every Claude alias maps to the same pin.

- **Source**: `.claude/agents/<name>.md` frontmatter `model:` field (or omitted)
- **Transform**: `convert_cursor_model` in `apps/rhino-cli/src/application/agents/cursor.rs`
- **Sink**: `.cursor/agents/<name>.md` frontmatter `model:` field
- **Policy**: [Model Selection Convention](../../repo-governance/development/agents/model-selection.md)
  ("Platform Binding Examples" section — Cursor full-tier collapse)

| Claude Code alias       | Cursor model ID | Capability tier                     |
| ----------------------- | --------------- | ----------------------------------- |
| `opus`                  | `composer-2.5`  | Thinking (collapsed onto execution) |
| `sonnet`/omit (inherit) | `composer-2.5`  | Execution                           |
| `haiku`                 | `composer-2.5`  | Fast (collapsed — avoids 6× toggle) |

**The emitter must never write `composer-2.5-fast`.** That slug is the six-times-priced fast
inference toggle; this binding exists to pin delegated subagents off it.

### Cursor model-pin reach

The `model:` pin in `.cursor/agents/` governs **delegated subagents** launched from those files. It
**does not govern** the interactive Cursor Agent session's model, the `cursor-agent` CLI default,
or anything running under Auto/Router mode — those surfaces are outside repository-file control.

### Tool Translation (Claude Code → OpenCode)

Claude Code agent frontmatter lists tools as an array of string names. OpenCode uses a
`permission` object mapping each tool to `allow`/`ask`/`deny` (the older boolean flag form
`tools: { read: true, … }` is deprecated/legacy and no longer emitted).

- **Source**: `.claude/agents/<name>.md` frontmatter `tools:` array
- **Transform**: `convert_permission` in `apps/rhino-cli/src/internal/agents/converter.rs`
- **Sink**: `.opencode/agents/<name>.md` frontmatter `permission:` map (`read: allow`, `write: allow`, etc.)

## Adding a New Platform Binding

To add a new generated binding:

1. Add a `harness:` entry to `repo-config.yml` (tier, agent-dir, mirrors, instruction surfaces, shadow globs).
2. Add a row to the Platform Binding Directories table above.
3. Implement the converter in `apps/rhino-cli/src/application/agents/` and wire it into `harness bindings generate`.
4. Add Rust integration tests and Gherkin scenarios under `specs/apps/rhino/behavior/rhino-cli/gherkin/`.
5. Update this document's Translation Artifacts section.

## Related

- [Governance Vendor-Independence Convention](../../repo-governance/conventions/structure/governance-vendor-independence.md) —
  policy separating vendor-neutral governance from platform bindings
- [Multi-Harness Binding Convention](../../repo-governance/conventions/structure/multi-harness-binding.md) —
  two-tier binding model, no-shadowing rule, mechanical-generation requirement, and parity guard
- [AI Agents Development Guide](../../repo-governance/development/agents/ai-agents.md) — agent authoring
  guide with binding-specific Platform Binding Examples
- [Model Selection Convention](../../repo-governance/development/agents/model-selection.md) — capability
  tiers and how they resolve to per-binding model IDs
- `AGENTS.md` at repo root — canonical root instruction file read by most platforms
- `CLAUDE.md` at repo root — Claude Code shim importing `AGENTS.md`

Those regenerated mirrors are part of your change: they belong on your touched-file ledger and MUST land in the **same commit** as the `.claude/` source that produced them, never a follow-up sync commit. Verify with `npm run validate:sync`; never hand-edit a mirror. See [File-Touch Discipline](../../repo-governance/development/practice/file-touch-discipline.md).
