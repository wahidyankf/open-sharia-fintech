# Phase 0: Cross-Vendor Parity Invariants (Deterministic)

Run all five invariants before starting Phase 1. Phase 0 always runs in full, even when Phase 1
is scoped to one harness — checker findings are reported first so the fixer can address
deterministic drift before spending time on web research.

## Invariant 1 — Governance prose vendor-neutrality

- **Tool**: `apps/rhino-cli/scripts/rhino-bin.sh repo-governance vendor validate repo-governance/`
- **Pass**: exits 0 with `GOVERNANCE VENDOR AUDIT PASSED: no violations found`
- **Fail**: any non-zero exit; report each violation with file path, line number, forbidden term,
  suggested replacement (already in tool output)
- **Default criticality**: HIGH. **Confidence**: HIGH (deterministic regex match)
- **Fix scope**: human-required — rewriting governance prose requires judgment per the
  convention's Migration Guidance

## Invariant 2 — Root instruction surface vendor-neutrality

- **Tool**: `apps/rhino-cli/scripts/rhino-bin.sh repo-governance vendor validate AGENTS.md` and
  same for `CLAUDE.md`
- **Pass**: both exit 0 with no violations outside `binding-example` fences and "Platform
  Binding Examples" headings
- **Fail**: any violation in load-bearing prose
- **Default criticality**: HIGH (root surface read by multiple coding agents). **Confidence**:
  HIGH
- **Fix scope**: human-required — same reasoning as Invariant 1

## Invariant 3 — Binding sync no-op

- **Tool**: `npm run generate:bindings && git diff --quiet .opencode/ .amazonq/`
- **Pass**: sync exits 0 AND `git diff --quiet` exits 0 (no changes produced)
- **Fail**: sync produced drift in `.opencode/` — report the changed files
- **Default criticality**: MEDIUM (drift means upstream `.claude/` edits were not synced).
  **Confidence**: HIGH
- **Fix scope**: **auto-fixable** — run `npm run generate:bindings` again, stage the resulting
  `.opencode/` changes, re-run to confirm idempotence, hand staged changes back to the
  orchestrator for commit (message `chore(opencode): re-sync agents from .claude/`)

## Invariant 4 — Agent count parity

- **Tool**: `find .claude/agents -name '*.md' | wc -l` and same for `.opencode/agents/*.md`
  (`.claude/agents/` is nested into role subfolders; `.opencode/agents/` is flat — `find` is
  required on the `.claude/` side, a plain `ls` glob only sees the top-level `README.md`)
- **Pass**: counts equal
- **Fail**: counts differ — diff via
  `comm -3 <(find .claude/agents -name '*.md' -exec basename {} \; | sort) <(ls .opencode/agents | sort)`,
  report only-`.claude` and only-`.opencode` entries
- **Default criticality**: HIGH (sets diverge → contributors get different agent inventories).
  **Confidence**: HIGH
- **Known intentional skip**: `README.md` is present in both directories as an index file, not
  an agent definition — the sync tool (`converter.rs` line ~391) explicitly excludes it. Compare
  filesystem counts to each other, never to the sync tool's conversion count.
- **Fix scope**: human-required — an orphan in `.opencode/` may need deletion OR a missing
  `.claude/` counterpart may need authoring; either choice has product implications

## Invariant 5 — Translation-map coverage

- **Tools**: color map — `grep -rh "^color:" .claude/agents/ | sort -u` (recursive — `.claude/agents/`
  is nested, a non-recursive glob silently returns nothing) vs. the Color Translation Table in
  `repo-governance/development/agents/ai-agents.md`; tier map —
  `grep -rh "^model:" .claude/agents/ .opencode/agents/*.md | sort -u` vs. the capability-tier
  map in `repo-governance/development/agents/model-selection.md`
- **Pass**: every distinct frontmatter value appears in the corresponding map
- **Fail**: any value not in the map — report the missing entry
- **Default criticality**: MEDIUM (sync may produce wrong-translated output for the missing
  entry). **Confidence**: HIGH
- **Fix scope**: human-required — adding a new color/tier requires a role-mapping decision a
  fixer cannot make mechanically
