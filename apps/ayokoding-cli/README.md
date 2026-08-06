# ayokoding-cli

`ayokoding-cli` is the small Rust companion to AyoKoding. It checks links inside the learning
content before a reader discovers a dead end. It is a repository tool, not a separately published
product. 🧭

## Run a link check

From the repository root, this is the usual command:

```bash
npm exec nx -- run ayokoding-cli:run -- links check
```

The command scans `apps/ayokoding-www/content` by default. Check another content directory when
you are working with a focused fixture or a future content set:

```bash
npm exec nx -- run ayokoding-cli:run -- links check --content path/to/content
```

Use `--output json` or `--output markdown` when another tool needs the result, and `--quiet` when
only failures should be printed. A successful check exits with `0`; broken links or an unreadable
content directory exit non-zero.

## Build and verify

```bash
# Build the local binary in apps/ayokoding-cli/dist/
npm exec nx -- run ayokoding-cli:build

# Run the fast project-quality gate
npm exec nx -- run ayokoding-cli:test:quick

# Exercise the filesystem-backed integration suite
npm exec nx -- run ayokoding-cli:test:integration
```

For the site-level check that normally uses this tool, run:

```bash
npm exec nx -- run ayokoding-www:test:quick
```

## What it checks

The checker reads Markdown files and follows repository-internal links. It ignores external URLs
and same-page anchors, so it stays focused on whether AyoKoding content routes resolve inside this
checkout. The behavior contract lives in
[the CLI Gherkin specs](../../specs/apps/ayokoding/behavior/ayokoding-cli/gherkin/README.md).

## Useful source locations

- `src/cli.rs` — command-line arguments and exit behavior
- `src/commands/links.rs` — the `links check` command
- `tests/` — end-to-end command coverage
- `project.json` — Nx targets used from the workspace root
