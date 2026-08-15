# Phase 0 — Cursor Subdirectory-Recursion Research Refresh

**Access date**: 2026-08-13

**Result**: No change from the prior finding. Subdirectory-nested agent discovery under
`.cursor/agents/<group>/<name>.md` remains **unsupported / not confirmed** by Cursor.

## Sources

1. [Subagents | Cursor Docs](https://cursor.com/docs/subagents) — official docs confirm project
   subagent locations (`.cursor/agents/`, `.claude/agents/`, `.codex/agents/`, with `.cursor/`
   taking precedence on name conflicts) but are silent on subdirectory/nested-folder discovery.
2. [Nested directory support for subagents](https://forum.cursor.com/t/nested-directory-support-for-subagents/151298)
   (forum.cursor.com, filed 2026-02-09) — an open, unresolved community feature request. The
   original poster states plainly: "our subagents are only picked up by the IDE when they are
   located directly within `.cursor/agents`." No official Cursor team reply grants support.
3. Cursor changelog (`2.5`, Feb 2026) mentions "nested subagents" — verified this refers to
   **runtime agent-call hierarchies** (a subagent spawning its own subagents during execution),
   not file-discovery in nested directories. Not applicable here.
4. No changelog entry from July–Aug 2026 addresses `.cursor/agents/` directory structure.

## Conclusion

The plan proceeds with flat mirrors, per `prd.md` §FR-3.16, which treats Cursor as unsupported
until proven otherwise. This is informational only — it does not block Phase 6/14's mirror
generator work, which flattens grouped `.claude/agents/<group>/<name>.md` sources into
`.cursor/agents/<name>.md` regardless of source directory structure.
