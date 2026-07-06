# CLAUDE.md

@AGENTS.md

## Platform Binding Examples

This file is the Claude Code platform-binding shim. The single-line `@AGENTS.md` directive above imports the canonical, vendor-neutral instruction surface. The rest of this file documents Claude-Code-specific binding details and is intentionally vendor-specific. Per the
[Governance Vendor-Independence Convention](./repo-governance/conventions/structure/governance-vendor-independence.md),
the vendor-audit scanner skips every line under this heading until the next same-level heading or end of file.

### Markdown Quality (Claude Code hook)

In addition to the standard Prettier + markdownlint pipeline, a Claude Code hook auto-formats and lints after Edit/Write operations (requires `jq`).

### Working with `.claude/` and `.opencode/` directories

Edit `.claude/` and `.opencode/` files with normal `Write` / `Edit` tools. Both paths pre-authorized in `.claude/settings.json` (`Write(.claude/**)`, `Edit(.claude/**)`, `Write(.opencode/**)`, `Edit(.opencode/**)`), no approval prompt fires. `Bash` heredoc and `sed` remain fine for bulk mechanical substitutions, but no rule against direct edits.

**Applies to all paths**:

- `.claude/agents/*.md` — agent definition files (Claude Code format)
- `.claude/skills/*/SKILL.md` — agent skill files (source of truth for both Claude Code AND OpenCode; OpenCode reads natively per [opencode.ai/docs/skills](https://opencode.ai/docs/skills/), no mirror)
- `.claude/skills/*/reference/*.md` — skill reference modules
- `.opencode/agents/*.md` — OpenCode agent mirrors (auto-synced from `.claude/agents/`)

**See**: [primary binding agent catalog](./.claude/agents/README.md)

### Delivery Mode default (Claude-Code binding)

`worktree-to-pr` is inherited as the plan default from `AGENTS.md` §Git Workflow §Delivery Mode (no
local override in this file — direct push to `main` is no longer the assumed default). The two
PR-review-cycle agents, `pr-review-maker` and `pr-review-fixer`, are ordinary `.claude/agents/*.md`
files under this binding; `pr-review-maker` writes only via the GitHub Reviews API (no local `git
push`), while `pr-review-fixer` pushes commits to the PR branch through the same git tooling as any
other agent in this repo.

### Multi-harness configuration (Claude Code + OpenCode + Amazon Q)

Repo maintains **multi-harness compatibility** with Claude Code, OpenCode, and Amazon Q Developer:

- **`.claude/`**: Source of truth (PRIMARY) — All updates happen here first
- **`.opencode/`**: Auto-generated (SECONDARY) — Synced from `.claude/`
- **`.amazonq/`**: Auto-generated (SECONDARY) — Emitted from `.claude/`

**Making changes:**

1. Edit agents/skills in `.claude/` first
2. Run sync: `npm run generate:bindings`
3. All secondary binding artifacts stay synced automatically

**Format differences:**

- **Tools**: Claude Code uses arrays `[Read, Write]`; OpenCode uses a `permission` object `{ read: allow, write: allow }` (current convention per [opencode.ai/docs/agents](https://opencode.ai/docs/agents/)). The older boolean flags form `{ read: true, write: true }` is deprecated/legacy — still accepted by OpenCode but no longer emitted by `rhino-cli agents sync`.
- **Models**: Claude Code uses `sonnet`/`opus`/`haiku` (or omits for budget-adaptive opus-inherit — intentional, not legacy); OpenCode uses a 3-tier mapping — thinking (`opus`) and execution (`sonnet`/omitted) both resolve to `opencode-go/glm-5.2` (intentionally identical: no opencode-go roster model separately clears Claude Opus 4.8's tier), fast (`haiku`) resolves to `opencode-go/minimax-m3`. See [model-selection.md](./repo-governance/development/agents/model-selection.md) for full capability-tier mapping.
- **Skills**: NOT mirrored — OpenCode reads `.claude/skills/{name}/SKILL.md` natively per [opencode.ai/docs/skills](https://opencode.ai/docs/skills/). The validate:sync `No Synced Skill Mirror` check fails if a stale `.opencode/skill/` or `.opencode/skills/<claude-name>` mirror reappears.
- **Permissions**: Claude Code uses `settings.json` permissions, OpenCode uses `opencode.json` permission block (both configured with equivalent access)
- **Colors**: Claude Code agents use named colors (`blue`, `green`, `yellow`, `purple`, etc.) written by hand in `.claude/agents/*.md`. `rhino-cli agents sync` translates these to OpenCode theme tokens (`primary`, `success`, `warning`, `secondary`, etc.) when generating `.opencode/agents/*.md` — current OpenCode rejects named colors. See [Platform Binding Color Translation](./repo-governance/development/agents/ai-agents.md#platform-binding-color-translation) for the full mapping.
- **MCP/Plugins**: Claude Code uses plugins (Context7, Playwright, Nx, LSPs), OpenCode uses MCP servers (Playwright, Nx, Perplexity)

**Security policy**: Only use skills from trusted sources. All skills in this repo maintained by project team.

**See**: [primary binding agent catalog](./.claude/agents/README.md)

### organiclever-www skill

The organiclever-www content development skill is at [.claude/skills/apps-organiclever-www-developing-content/SKILL.md](./.claude/skills/apps-organiclever-www-developing-content/SKILL.md).

<!-- nx configuration start-->
<!-- Leave the start & end comments to automatically receive updates. -->

### Nx-related notes (Claude-Code binding)

The Nx tooling guidelines, generator usage, and `nx_docs` policy are documented in [`AGENTS.md`](./AGENTS.md) and apply identically here. The `<!-- nx configuration -->` markers above are preserved so the Nx auto-injection tool can refresh content if needed.

<!-- nx configuration end-->

<!-- rtk-instructions v2 -->

### RTK (Rust Token Killer) — Token-Optimized Commands (Claude-Code binding)

RTK is a CLI wrapper that reduces token usage by filtering AI output. See [github.com/rtk-ai/rtk](https://github.com/rtk-ai/rtk) for full details. The `<!-- rtk-instructions -->` markers are preserved so the RTK auto-injection tool can refresh content if needed.

**Always prefix commands with `rtk`**. If RTK has a dedicated filter, it uses it. If not, passes through unchanged. RTK is always safe to use.

```bash
rtk gain              # Show token savings analytics
rtk gain --history    # Show command usage history with savings
rtk discover          # Analyze Claude Code history for missed opportunities
rtk proxy <cmd>       # Execute raw command without filtering (for debugging)
```

<!-- /rtk-instructions -->

### caveman — Token Compression (Claude-Code binding)

**caveman** compresses agent output by ~75% via terse caveman-speak. Works with OpenCode via skill injection. Stacks with RTK (output filtering) for compounded savings. MIT licensed. Installed 2026-05-03.

**Usage**: In OpenCode, type `/caveman` in chat. Modes: `lite`, `full` (default), `ultra`.

**Commands**:

- `/caveman` — toggle on/off
- `/caveman lite|full|ultra` — set mode
- `/caveman-stats` — show token savings
- `/caveman-commit` — generate terse commit message
- `/caveman-review` — one-line PR comments

**Skills installed**: 8 skills in `.agents/skills/caveman-*`. Auto-loads when mentioned or triggered.

**Stack with RTK**: RTK filters CLI output (git/npm commands); caveman compresses agent prose output. Both run simultaneously for compounded savings.

**Verification**: `opencode stats` shows token usage per session.
