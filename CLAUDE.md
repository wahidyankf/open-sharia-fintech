# CLAUDE.md

@AGENTS.md

## Platform Binding Examples

This file is the Claude Code platform-binding shim. The `@AGENTS.md` directive above imports the
canonical, vendor-neutral instruction surface; the rest of this file is vendor-specific. Per the
[Governance Vendor-Independence Convention](./repo-governance/conventions/structure/governance-vendor-independence.md),
the vendor-audit scanner skips every line under this heading.

### Markdown Quality

A Claude Code hook auto-formats and lints after Edit/Write, alongside the standard
Prettier + markdownlint pipeline (requires `jq`).

### Working with `.claude/` and `.opencode/`

Edit both with normal `Write`/`Edit` tools — pre-authorized in `.claude/settings.json`, no approval
prompt fires.

- `.claude/agents/<role-subfolder>/*.md` — agent definitions, nested into role subfolders
- `.claude/skills/*/SKILL.md` — source of truth for both Claude Code and OpenCode (OpenCode reads
  natively, no mirror)
- `.claude/skills/*/reference/*.md` — skill reference modules
- `.opencode/agents/*.md` — auto-synced OpenCode mirrors, flattened to one level

**See**: [primary binding agent catalog](./.claude/agents/README.md)

### Delivery Mode default

`worktree-to-pr` is inherited from `AGENTS.md` §Git Workflow §Delivery Mode. The PR-review-cycle
agents are ordinary `.claude/agents/pr-review/*.md` files under this binding.

**See**: [AGENTS.md §AI Agents](./AGENTS.md#ai-agents)

### Multi-harness configuration

Repo supports exactly three harnesses — Claude Code, OpenCode, and OpenAI Codex CLI. The
`harness:` registry in `repo-config.yml` is authoritative; adding a fourth is one entry there.

- **`.claude/`**: source of truth (PRIMARY)
- **`.opencode/`**, **`.codex/`**, **`.agents/`**: auto-generated (SECONDARY) via
  `npm run generate:bindings`, landing in the **same commit** as the `.claude/` source.
  `npm run validate:sync` verifies only the OpenCode agent mirror and the `.agents/skills/` mirror;
  `npm run harness:bindings-validation` additionally verifies `.codex/agents/` and the
  `.codex/config.toml` generated region. Never hand-edit a mirror — except a path a harness entry's
  `ownership:` list declares `vendored` (e.g. `.codex/config.toml`'s hand-authored tables outside
  its delimited region), which is hand-maintained by design (see
  [the two subclasses](./repo-governance/glossary/vendored-exception-subclasses.md));
  `repo-config.yml` is authoritative on which paths those are.

Claude Code uses tool arrays and named colors; OpenCode uses a `permission` object and theme tokens
(translated by `rhino-cli harness bindings generate`). Model tiers map to concrete vendor IDs — see
[model-selection.md](./repo-governance/development/agents/model-selection.md). OpenCode reads
`.claude/skills/{name}/SKILL.md` natively; Codex reads the `.agents/skills/` mirror. Only use skills
from trusted sources; all skills here are maintained by the project team.

**See**: [Platform Binding Color Translation](./repo-governance/development/agents/ai-agents/agent-color-categorization.md#platform-binding-color-translation)

### organiclever-www skill

[apps-organiclever-www-developing-content/SKILL.md](./.claude/skills/apps-organiclever-www-developing-content/SKILL.md)

<!-- nx configuration start-->
<!-- Leave the start & end comments to automatically receive updates. -->

### Nx-related notes

Nx tooling guidelines, generator usage, and `nx_docs` policy are documented in
[AGENTS.md](./AGENTS.md) and apply identically here.

<!-- nx configuration end-->

### caveman — Token Compression

Compresses agent output ~75% via terse caveman-speak; stacks with RTK for compounded savings.
Installed 2026-05-03. `/caveman` toggles; `/caveman lite|full|ultra` sets mode; `/caveman-stats`
shows savings; `/caveman-commit` generates a terse commit message.
