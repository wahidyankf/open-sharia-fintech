# Phase 1 Drift Dimensions: Catalog Source, D1-D3

## Harness Catalog Source

Read `docs/reference/platform-bindings.md` to obtain the canonical list of supported harnesses.
For each row, extract: harness name (Claude Code, OpenCode, or OpenAI Codex CLI),
binding directory (e.g., `.claude/`, `.opencode/`), root instruction file name (e.g., `CLAUDE.md`,
`AGENTS.md`), MCP config path (if documented), custom-agent surface (directory
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
