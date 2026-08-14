# Phase 1: External Harness Drift Dimensions

## Harness Catalog Source

Read `docs/reference/platform-bindings.md` to obtain the canonical list of supported harnesses.
For each row, extract: harness name (e.g., Claude Code, OpenCode, Aider, OpenAI Codex CLI),
binding directory (e.g., `.claude/`, `.opencode/`), root instruction file name (e.g., `CLAUDE.md`,
`AGENTS.md`, `CONVENTIONS.md`), MCP config path (if documented), custom-agent surface (directory
path or `n/a`), skills surface (directory path or `n/a`).

## D1 — Root instruction file name

**Check**: fetch the harness's official docs and confirm the currently documented root
instruction filename against the catalog row. **Drift indicator**: docs now specify a different
or additional filename. **Default criticality**: HIGH — wrong filename means the agent cannot
find instructions. **Fix**: update the catalog's "Root instruction file" column. **Confidence**:
HIGH only when `[Verified]`.

## D2 — Rules/config directory path

**Check**: confirm the binding directory (e.g., `.claude/`, `.opencode/`) still matches the
harness's documented config directory. **Drift indicator**: harness renamed/deprecated its
config directory. **Default criticality**: HIGH. **Fix**: update the catalog's "Binding
directory" column; if the directory moved, also update `CLAUDE.md`/`AGENTS.md` cross-references
found via Grep. **Confidence**: HIGH only when `[Verified]`; MEDIUM if cross-reference impact is
large (flag for manual review).

## D3 — MCP/plugin config path

**Check**: confirm the MCP/plugin config file path (e.g., `.claude/settings.json`,
`opencode.json`) matches the harness's documented location. **Drift indicator**: harness moved
its config file. **Default criticality**: MEDIUM. **Fix**: update the catalog's "MCP config
path" column. **Confidence**: HIGH for catalog update; MEDIUM if committed config files also
need renaming.

## D4 — Custom-agent surface

**Check**: confirm the directory path and file format for custom agent definitions match the
harness docs. **Drift indicator**: harness changed the directory path, YAML/frontmatter schema,
or discovery mechanism. **Default criticality**: HIGH — incorrect surface means agents are
silently ignored. **Fix**: update catalog row; for each committed agent file flagged in D6,
add/remove/rename frontmatter fields per the new schema; run `npm run generate:bindings` after
editing `.claude/agents/`. **Confidence**: HIGH for catalog-only; MEDIUM for schema migration of
committed files (each must be re-validated individually).

## D5 — Skills surface

**Check**: confirm the skill discovery path and loading mechanism match the harness docs.
**Drift indicator**: harness changed how skills are discovered/loaded. **Default criticality**:
MEDIUM. **Fix**: update the catalog's "Skills surface" column.

## D6 — Committed binding file conformance

**Check**: beyond catalog-vs-docs drift, inspect committed binding files for structural
violations — agent definitions must match the harness's current required frontmatter schema;
config files must not use fields the harness has removed/deprecated. **Drift indicator**: a
field present in committed files is no longer valid per current docs. **Default criticality**:
MEDIUM (runtime behaviour may silently degrade). **Fix**: remove or rename deprecated fields; do
not add undocumented fields. **Confidence**: HIGH only when the deprecated field is explicitly
documented in a `[Verified]` source; MEDIUM otherwise (skip for safety).

## D7 — Cursor model-pin conformance (Cursor only)

**Check**: every `.cursor/agents/*.md` file's `model:` field must match the pinned literal
(`composer-2.5` per `apps/rhino-cli/src/application/agents/cursor.rs`). **Tool**:
`grep -h "^model:" .cursor/agents/*.md | sort -u` and
`grep -rE '^model: composer-2\.5-fast' .cursor/agents/` (the prohibited fast-variant pin). **Pass**:
exactly one distinct value equal to the pin, fast-variant absent. **Fail**: any other value or a
fast-variant line. **Default criticality**: HIGH (wrong pin may bill at 6× fast rates).
**Confidence**: HIGH (mechanical comparison).
