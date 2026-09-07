---
description: "What the pre-commit hook validates."
when_to_use: "Use when debugging a pre-commit check failure."
---

# Git Hook Workflow: Pre-commit Hook (What It Validates)

**What It Validates**:

**Configuration Validation** (Added 2026-01-22):

Validates primary and secondary platform binding directory consistency before commit:

1. Detects if binding directories (`.claude/` or `.opencode/`) are in staged files
2. If changed:
   - Validates primary binding directory (`.claude/`) source format (YAML, tools, model, skills)
   - Syncs primary to secondary binding directory (auto-sync)
   - **Mirrors ship in the same commit as their `.claude/` source** — the hook stages them for you; a follow-up "sync commit" publishes a tree where source and mirror disagree ([File-Touch Discipline](../../practice/file-touch-discipline.md))
   - Validates secondary binding directory (`.opencode/`) output (semantic equivalence)
3. If unchanged: Skips validation (performance)

**Benefits:**

- Catches config errors before commit (earliest possible)
- Prevents invalid commits from being created locally
- Ensures primary and secondary binding directories stay in sync
- Auto-syncs on commit (no manual step)
- Only runs when config files in staged files (~260ms when needed)

**Markdown:**

- Validates Mermaid diagrams in staged `.md` files (width, label length, syntax) — step 6m
- Validates heading hierarchy in staged prose-allowlist `.md` files (single H1, no skipped levels) — step 6h
- Validates markdown links + `#fragment` anchors in staged files only (fast, targeted) — step 7
- Validates all markdown files meet linting standards (comprehensive) — step 8

**What Happens on Failure**:

- Commit is blocked
- Error message shows which check failed (config, formatting, or markdown)
- Fix the issue and try again

**Example**:

```bash
$ git commit -m "feat: add new feature"
🔍 Validating .claude/ and .opencode/ configuration...
✅ Configuration validation passed
⏭️  Skipping docker-compose validation (no docker-compose.yml changes in staged files)
⏭️  Skipping dotnet formatting (no .cs/.fs files staged)
⏭️  Skipping docs naming validation (no docs/ changes in staged files)
[main abc1234] feat: add new feature
```
