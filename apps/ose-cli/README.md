# ose-cli

`ose-cli` keeps OSE website content navigable by checking its internal Markdown links. It is a
local Rust maintenance tool for the public site, not a separately installed product. 🔎

## Run a check

```bash
# Check the default ose-www content directory
npm exec nx -- run ose-cli:run -- links check

# Check a specific content directory
npm exec nx -- run ose-cli:run -- links check --content path/to/content
```

The command can write `text`, `json`, or `markdown` output via `--output`; add `--quiet` when a
script only needs failures. It returns `0` when every internal link resolves, `1` for broken links
or a readable-content problem, and `2` for invalid command arguments.

## Build and verify

```bash
npm exec nx -- run ose-cli:build
npm exec nx -- run ose-cli:test:quick
npm exec nx -- run ose-cli:test:integration
```

The build target creates `apps/ose-cli/dist/ose-cli`. For the website-level quality check that
uses this tool, run `npm exec nx -- run ose-www:test:quick`.

## Where to look next

- `src/cli.rs` — supported commands and exit behavior
- `src/commands/links.rs` — link-check implementation
- `tests/` — command-level coverage
- `project.json` — workspace targets
