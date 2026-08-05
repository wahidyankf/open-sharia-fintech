---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

## Notes Linux: CLI and Daemon

The capstone is a packaged `notes-linux` CLI plus Unix-socket daemon. The CLI places replies on stdout, diagnostics on stderr, and returns non-zero on failure. The daemon accepts a small request/reply protocol and responds to SIGTERM by setting a stop flag and cleaning up its socket at a safe point.

## Run it

From `learning/capstone/code/`:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
pytest
```

Run `python -m notes_linux.daemon --socket /tmp/notes-linux.sock`, then use `notes-linux status --socket /tmp/notes-linux.sock`. The included `notes-linux.service` is a minimal systemd template; adapt user and executable paths before installing it.

## Acceptance criteria

The package installs in a clean virtual environment, tests pass, the CLI separates stdout and stderr, socket status succeeds, and SIGTERM stops the daemon cleanly.
