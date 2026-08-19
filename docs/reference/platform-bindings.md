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

The table below catalogs the three supported coding-agent harnesses — exactly the entries declared
in `repo-config.yml` `harness:`. Columns record every surface each harness exposes so contributors
know which files to create or extend. Harnesses absent from the registry are not supported; adding
one starts with a registry entry, not a row here.

**Verified 2026-05-24.**

| Platform         | Reads root `AGENTS.md` natively?           | Tool-specific instruction surface                                   | Project MCP config                   | Custom-agent surface                                                                                                | Skills surface              | Status                     |
| ---------------- | ------------------------------------------ | ------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------- | --------------------------- | -------------------------- |
| Claude Code      | No — reads `CLAUDE.md` (shim `@AGENTS.md`) | `CLAUDE.md`, `.claude/`                                             | `.mcp.json`                          | `.claude/agents/*.md`                                                                                               | `.claude/skills/*/SKILL.md` | Active                     |
| OpenCode         | Yes                                        | `.opencode/agents/` (auto-synced); reads `.claude/skills/` natively | `opencode.json`                      | `.opencode/agents/*.md`                                                                                             | reads `.claude/skills/`     | Active                     |
| OpenAI Codex CLI | Yes (since Apr 2025)                       | `AGENTS.override.md` (overrides), `.codex/config.toml`              | `.codex/config.toml` `[mcp_servers]` | `[agents.<name>]` in `config.toml` (with optional `config_file` pointer to a TOML layer, e.g. `.codex/<name>.toml`) | `.agents/skills/`           | Partial (`.codex/` exists) |

### Root instruction file hierarchy

Platforms that read `AGENTS.md` natively require no additional binding directory — the native read
is sufficient. Platforms that predate the `AGENTS.md` standard (or that require a harness-specific
entry point) receive either a shim that imports `AGENTS.md` (Claude Code's `CLAUDE.md`) or a
generated bridge file.

Some harnesses rank a tool-specific file **above** `AGENTS.md` when both are present. Those files
must never carry content that diverges from `AGENTS.md`. See the
[No-shadowing note](#no-shadowing-note) below.

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
hand-authored in this repo. The Nx MCP tooling's editor-assistant artifacts that previously lived
there (the `nx-*` agent skills under `.github/skills/`, plus `.github/agents/ci-monitor-subagent.agent.md`
and `.github/prompts/monitor-ci.prompt.md`) were removed; the repo reads Nx skills via the `nx-mcp`
plugin and monitors CI via the `gh` CLI.

The `.codex` files are safe to leave in place; they serve the Nx CI-monitoring capability and do not
affect the canonical `AGENTS.md` instruction surface.

### Generated bindings

Every generated-tier harness in `repo-config.yml` receives its binding mechanically from
`rhino-cli harness bindings generate` — never by hand:

- **`.opencode/agents/*.md`** — mirrors of `.claude/agents/**/*.md`, flattened to one level, with
  color, model, and tool frontmatter translated (see Translation Artifacts below).
- **`.codex/`** — declared at the generated tier in the registry; its emitter is not wired yet, so
  no file under `.codex/` is generator-owned today beyond the vendored Nx entries described above.

These files are deterministic and idempotent — never hand-edit them. The companion guard
`rhino-cli harness bindings validate` enforces byte-for-byte parity against the generator and runs in
the pre-push pipeline. The same guard asserts that every present binding directory under `.claude`,
`.opencode`, `.codex`, `.agents`, and `.github` is referenced in this catalog.

### No-shadowing note

Some harnesses rank a tool-specific file **above** the canonical `AGENTS.md` when both files are
present in the repository. These higher-precedence files silently override `AGENTS.md` for that
tool only, producing divergent behavior invisible to contributors using any other harness.

The following files trigger this rule:

- `AGENTS.override.md` — OpenAI Codex CLI ranks this above `AGENTS.md` when present.

Shadow files belonging to harnesses this repository does not support are out of scope: the rule
applies to the supported set only.

**The repo's default is not to create any of these files.** If a future operational need forces one
to exist, it must be implemented as a pure pointer or import directive referencing `AGENTS.md` —
never as a file with independent prose. Any exception must be recorded in this catalog with an
explicit justification.

See [Multi-Harness Binding Convention](../../repo-governance/conventions/structure/multi-harness-binding.md)
for the full no-shadowing rule (Rule 3 / AD3) and the two-tier binding model that governs all
harness integrations.

### Optional thin pointers

OpenCode and the OpenAI Codex CLI read the root `AGENTS.md` natively, so neither needs a
tool-specific instruction file to receive the canonical instructions. Claude Code is the one
exception, and its `CLAUDE.md` shim is a pure `@AGENTS.md` import.

**Decision: the repo ships no optional thin pointer files** by default. Rationale: each would be
either redundant (the native `AGENTS.md` read already applies) or a drift/shadowing risk. If a thin
pointer is added later, it must be a pure `AGENTS.md` pointer emitted by
`rhino-cli harness bindings generate` and covered by `rhino-cli harness bindings validate`.

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
