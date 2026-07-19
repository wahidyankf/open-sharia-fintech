# 76 · Linux App Development ◆ (By Example, Python)

**prd row**: Pass 4 · Concurrency & Systems · By Example · Python · Learn 176 / Drill 276 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: `◆` app-domain — building real Linux applications (CLIs and daemons) as an app developer:
the process/runtime model, filesystem & I/O, argument parsing/config/logging, IPC/subprocess, packaging &
distribution, and daemons/scheduling with graceful shutdown — in Python (no `†`: Python is the native
teaching language here). The kernel-level view is [`79-linux-os`](./79-linux-os.md).

## Why this exists · the big idea

- **The problem before the solution**: a CLI that ignores exit codes or mixes errors into stdout, and a
  daemon that dies mid-work on a signal, are unusable in the pipelines and init systems they live in —
  this topic exists to build programs that behave correctly as citizens of the Unix process model.
- **Keep-this-if-you-forget-everything**: a well-behaved Linux program honours the contract the OS already
  defines — args, exit codes, stdout-vs-stderr, and signals — so it composes in pipelines and shuts down
  cleanly under `systemd`.
- **Big ideas touched**: `layering-and-leaks` — an app rides on the process/runtime model (env, file
  descriptors, signals), and those OS-level contracts leak straight into how your program must behave;
  `coupling-vs-cohesion` — config, logging, and IPC kept as separable concerns let a CLI and its daemon
  share one core without tangling.

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./04-just-enough-python.md),
  [topic 5 Just Enough Bash](./05-just-enough-bash.md) (env/args/exit codes/
  signals), and [topic 11 Backend Essentials](./11-backend-essentials.md) (long-running service intuition).
- **Tools & environment**: a **Linux** machine (or WSL/VM); **Python 3.x**; virtualenv/packaging tooling;
  `systemd` (for the daemon lifecycle example) or an equivalent init; Neovim/VSCode (DD-17).
- **Assumed knowledge**: Python functions + files (topic 04); shell env/args/exit codes/signals (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: `pyproject.toml`-based packaging (PEP 517/518/621) + `venv` remain the current
  standard; `subprocess`/signal-handling stdlib idioms, systemd-unit basics, Unix exit-code + stdio
  conventions, and `pytest` are all evergreen/unchanged. No version/license-sensitive claims to correct.

### DD-35 primary-source citations (fetched-and-read)

Per DD-35, every API/spec/tool claim below traces to a primary source; anything not directly confirmed is
flagged `[Needs Verification]` for the authoring pass.

- **Packaging** — `[Verified]` `pyproject.toml` with a `[project]` table (PEP 621) is the current standard
  metadata format; PEP 517/518 define the build-backend interface; `venv` is the stdlib virtual-environment
  tool (packaging.python.org/en/latest/specifications/pyproject-toml, docs.python.org/3/library/venv).
  Console-script entry points via `[project.scripts]`
  (packaging.python.org/en/latest/specifications/entry-points).
- **subprocess** — `[Verified]` `subprocess.run(..., check=True)` raises `CalledProcessError` on non-zero
  exit; `capture_output=True` captures stdout/stderr; `timeout=` raises `TimeoutExpired`
  (docs.python.org/3/library/subprocess). `Popen` for streaming/pipes.
- **signals** — `[Verified]` `signal.signal(signal.SIGTERM, handler)` installs a handler; the graceful-flag
  idiom (handler sets a flag the loop polls) is the standard pattern (docs.python.org/3/library/signal).
  Note the Python constraint (`[Verified]`, same page): handlers run in the main thread only.
- **argparse / sys** — `[Verified]` `argparse` auto-generates `--help`, supports subparsers; `sys.exit(n)`
  sets the exit code; `sys.stdout`/`sys.stderr` are the standard streams
  (docs.python.org/3/library/argparse, docs.python.org/3/library/sys).
- **logging** — `[Verified]` the `logging` module provides levels (DEBUG/INFO/WARNING/ERROR) and
  `basicConfig` (docs.python.org/3/library/logging).
- **pathlib / tempfile / os** — `[Verified]` `pathlib.Path`, `tempfile.NamedTemporaryFile`, `os.environ`,
  `os.chmod` are the stdlib file/env primitives (docs.python.org/3/library/pathlib, …/tempfile, …/os).
- **systemd** — `[Verified]` a `.service` unit with `[Service] ExecStart=` / `Restart=` and `Type=` is the
  standard unit format; SIGTERM is systemd's default stop signal (freedesktop.org systemd.service(5),
  systemd.kill(5)). Exact directive semantics beyond ExecStart/Restart are `[Needs Verification]` at
  authoring — confirm against the man page.
- **pytest** — `[Verified]` `pytest` discovers `test_*` functions; `capsys` fixture captures stdout/stderr;
  `monkeypatch` patches subprocess (docs.pytest.org). Exact pytest major version is `[Needs Verification]` —
  do not pin; the fixtures used here are long-stable.
- **XDG base dirs** — `[Verified]` `XDG_CONFIG_HOME` (default `~/.config`) governs config location
  (specifications.freedesktop.org/basedir/latest).
- **GTK/Qt desktop GUI** — kept at survey depth; no specific toolkit version pinned (`[Needs Verification]`
  if authored content quotes a version). References in `## Read more`.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · process-model** — a Linux app is a process bound by the OS contract: env, args, exit codes, standard streams, and signals.
- **co-02 · argv** — command-line arguments arrive via `sys.argv`.
- **co-03 · argparse** — `argparse` parses arguments, auto-generates `--help`, and supports subcommands.
- **co-04 · exit-codes** — `sys.exit(n)` sets the process exit code; 0 = success, non-zero = failure.
- **co-05 · stdout-stderr** — data goes to stdout, diagnostics/errors to stderr, so pipelines stay clean.
- **co-06 · environment-variables** — `os.environ` reads environment configuration.
- **co-07 · config-files** — apps load config from files (XDG base dirs govern location).
- **co-08 · logging** — the `logging` module emits levelled diagnostics.
- **co-09 · file-io** — `open`/`pathlib.Path` read and write files.
- **co-10 · file-permissions** — file mode bits (`os.chmod`/`stat`) control access.
- **co-11 · file-descriptors** — stdin/stdout/stderr are file descriptors; streams can be redirected.
- **co-12 · temp-files** — `tempfile` creates auto-cleaned temporary files.
- **co-13 · subprocess** — `subprocess.run`/`Popen` launch and capture child processes.
- **co-14 · subprocess-errors** — `check=True` / `returncode` / `timeout=` surface child failures.
- **co-15 · pipes** — processes are wired together via pipes (child stdin/stdout).
- **co-16 · signals** — `signal.signal` installs handlers for SIGTERM/SIGINT.
- **co-17 · graceful-shutdown** — a signal handler flips a flag so the app finishes cleanly and releases resources.
- **co-18 · daemon-basics** — a long-running service loops, logs, and stays up until told to stop.
- **co-19 · systemd-unit** — a `.service` unit (`ExecStart`/`Restart`/`Type`) manages the daemon's lifecycle.
- **co-20 · cron-scheduling** — cron runs scheduled jobs (contrast with an always-on daemon).
- **co-21 · venv** — `venv` isolates an app's dependencies.
- **co-22 · pyproject-packaging** — `pyproject.toml` (`[project]`, PEP 621) declares package metadata.
- **co-23 · dependencies** — dependencies are declared in `pyproject.toml` and installed via pip.
- **co-24 · entry-points** — `[project.scripts]` console entry points install the CLI as a command.
- **co-25 · sockets-ipc** — Unix/TCP sockets carry IPC between processes (survey).
- **co-26 · gui-survey** — GTK/Qt provide native Linux desktop GUIs (surveyed).
- **co-27 · containers-survey** — an app can be containerized for distribution (surveyed).
- **co-28 · pytest** — `pytest` tests the CLI and daemon behaviour.
- **co-29 · testing-subprocess** — subprocess calls are tested via patching/capture.
- **co-30 · testing-signals** — signal handling is tested by sending signals to a subprocess.

## Worked examples

Colocated under `linux-app-development/learning/code/`; each runnable + tested on Linux (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · sys-argv** — read `sys.argv` — verify args print. (co-02)
- **ex-02 · argparse-basic** — `argparse` with one positional — verify it parses. (co-03)
- **ex-03 · argparse-help** — auto-generated `--help` — verify the usage text. (co-03)
- **ex-04 · argparse-optional** — an optional `--verbose` flag — verify default + set. (co-03)
- **ex-05 · argparse-subcommand** — subparsers — verify subcommand dispatch. (co-03)
- **ex-06 · exit-zero** — `sys.exit(0)` on success — verify `$?` is 0. (co-04)
- **ex-07 · exit-nonzero** — `sys.exit(1)` on error — verify `$?` is non-zero. (co-04)
- **ex-08 · stderr-write** — write errors to `sys.stderr` — verify stream separation. (co-05)
- **ex-09 · stdout-vs-stderr** — data to stdout, logs to stderr — verify a pipe keeps them apart. (co-05)
- **ex-10 · read-env** — `os.environ.get` — verify the env value is read. (co-06)
- **ex-11 · env-default** — a default when the env var is unset — verify the fallback. (co-06)
- **ex-12 · read-file** — open + read a file — verify the contents. (co-09)
- **ex-13 · write-file** — write a file — verify persistence. (co-09)
- **ex-14 · pathlib** — `pathlib.Path` operations — verify path joins. (co-09)
- **ex-15 · file-mode** — `os.chmod` / `stat` a file — verify the permission bits. (co-10)
- **ex-16 · temp-file** — `tempfile.NamedTemporaryFile` — verify it's created + cleaned. (co-12)
- **ex-17 · logging-basic** — `logging.basicConfig` + a logger — verify a log line. (co-08)
- **ex-18 · logging-levels** — DEBUG/INFO/ERROR levels — verify filtering. (co-08)
- **ex-19 · config-file** — load a config file (toml/ini) — verify the values. (co-07)
- **ex-20 · xdg-config** — resolve `XDG_CONFIG_HOME` — verify the config path. (co-07)
- **ex-21 · fd-stdin** — read from stdin — verify piped input. (co-11)
- **ex-22 · fd-redirect** — redirect a stream to a file descriptor — verify redirection. (co-11)
- **ex-23 · subprocess-run** — `subprocess.run(["ls"])` — verify output. (co-13)
- **ex-24 · subprocess-output** — capture stdout — verify the captured text. (co-13)
- **ex-25 · venv-create** — `python -m venv` — verify an isolated env. (co-21)
- **ex-26 · pytest-first** — a `pytest` test of a pure function — verify green. (co-28)

### Intermediate

- **ex-27 · subprocess-check** — `check=True` raises on failure — verify `CalledProcessError`. (co-14)
- **ex-28 · subprocess-returncode** — inspect `returncode` — verify the error branch. (co-14)
- **ex-29 · subprocess-stderr** — capture child stderr — verify the error is surfaced. (co-14, co-05)
- **ex-30 · pipe-processes** — pipe one subprocess into another — verify the piped result. (co-15)
- **ex-31 · popen-stdin** — `Popen` writing to child stdin — verify the child reads it. (co-15, co-13)
- **ex-32 · signal-sigint** — handle SIGINT — verify a clean exit on Ctrl-C. (co-16)
- **ex-33 · signal-sigterm** — handle SIGTERM — verify the handler runs. (co-16)
- **ex-34 · graceful-flag** — a signal sets a stop flag the loop checks — verify graceful exit. (co-17, co-16)
- **ex-35 · cleanup-on-signal** — release resources in the handler — verify cleanup ran. (co-17)
- **ex-36 · daemon-loop** — a long-running loop with `sleep` — verify it stays up. (co-18)
- **ex-37 · daemon-log** — the daemon logs each cycle — verify the log output. (co-18, co-08)
- **ex-38 · daemon-signal-stop** — SIGTERM stops the daemon loop — verify a clean shutdown. (co-18, co-17)
- **ex-39 · systemd-unit** — write a systemd `.service` unit — verify the unit fields. (co-19)
- **ex-40 · systemd-lifecycle** — `ExecStart`/`Restart` semantics — verify the lifecycle intuition. (co-19)
- **ex-41 · cron-entry** — a crontab entry for a script — verify the schedule syntax. (co-20)
- **ex-42 · pyproject-min** — a minimal `pyproject.toml` — verify it's valid. (co-22)
- **ex-43 · pyproject-metadata** — `[project]` name/version/deps — verify the metadata. (co-22)
- **ex-44 · declare-dependency** — add a dependency in `pyproject.toml` — verify pip installs it. (co-23)
- **ex-45 · install-editable** — `pip install -e .` — verify it's importable. (co-23, co-21)
- **ex-46 · console-script** — a `[project.scripts]` entry point — verify the command runs. (co-24)
- **ex-47 · entry-point-invoke** — invoke the installed CLI by name — verify it dispatches. (co-24)
- **ex-48 · config-plus-logging** — the config file drives the log level — verify the wiring. (co-07, co-08)
- **ex-49 · unix-socket** — a Unix-domain-socket server + client — verify a message round-trip. (co-25)
- **ex-50 · tcp-socket** — a TCP socket survey example — verify connect/send. (co-25)
- **ex-51 · pytest-cli** — `pytest` invoking the CLI via subprocess — verify exit code + output. (co-28, co-13)
- **ex-52 · pytest-capsys** — capture stdout/stderr with `capsys` — verify separation. (co-28, co-05)
- **ex-53 · mock-subprocess** — patch subprocess in a test — verify no real call. (co-29)
- **ex-54 · test-exit-code** — assert the CLI's exit code — verify the discipline. (co-28, co-04)

### Advanced

- **ex-55 · full-cli** — args + config + logging + exit codes together — verify a well-behaved CLI. (co-03, co-07, co-08, co-04)
- **ex-56 · cli-bad-input** — bad input exits non-zero to stderr — verify the OS process contract. (co-04, co-05, co-01)
- **ex-57 · subprocess-timeout** — a subprocess with a `timeout=` — verify `TimeoutExpired` is handled. (co-14)
- **ex-58 · pipe-error-handling** — a broken pipe handled — verify graceful failure. (co-15, co-14)
- **ex-59 · daemon-systemd** — the daemon under a systemd unit with graceful SIGTERM — verify a managed lifecycle. (co-18, co-19, co-17)
- **ex-60 · daemon-restart** — `Restart=on-failure` behaviour — verify the restart intuition. (co-19)
- **ex-61 · cron-vs-daemon** — the same job as cron vs daemon — verify the tradeoff. (co-20, co-18)
- **ex-62 · signal-during-work** — a signal mid-task defers to a safe point — verify no corruption. (co-16, co-17)
- **ex-63 · tempfile-atomic** — atomic write via temp + rename — verify no partial file. (co-12, co-09)
- **ex-64 · permissions-enforce** — check/enforce file permissions — verify the mode. (co-10)
- **ex-65 · socket-ipc-daemon** — the daemon accepts commands over a Unix socket — verify a command round-trip. (co-25, co-18)
- **ex-66 · gui-gtk-survey** — a minimal GTK window (survey) — verify it opens. (co-26)
- **ex-67 · gui-qt-survey** — a minimal Qt window (survey) — verify it opens. (co-26)
- **ex-68 · container-package** — a Dockerfile for the app (survey) — verify it builds. (co-27)
- **ex-69 · container-run** — run the containerized CLI — verify output. (co-27)
- **ex-70 · package-distribute** — build a wheel/sdist — verify the artifact. (co-22, co-23)
- **ex-71 · install-clean-venv** — install the package into a fresh venv — verify it runs. (co-21, co-24)
- **ex-72 · test-signal-handling** — a test sending SIGTERM to a subprocess daemon — verify graceful shutdown. (co-30, co-16)
- **ex-73 · test-daemon-lifecycle** — start/stop the daemon in a test — verify a clean lifecycle. (co-30, co-18)
- **ex-74 · test-subprocess-error** — test error handling of a failing child — verify the error path. (co-29, co-14)
- **ex-75 · structured-logging** — JSON/structured logs — verify machine-readable output. (co-08)
- **ex-76 · cli-daemon-shared-core** — CLI + daemon share one core module — verify cohesion. (co-18, co-03)
- **ex-77 · integration-ipc-slice** — the CLI sends a command to the daemon over a socket + gets a reply — verify end-to-end. (co-25, co-18, co-15)
- **ex-78 · capstone-cli-and-daemon** — a well-behaved CLI + companion daemon: args/config/logging/exit codes, subprocess/IPC, SIGTERM graceful shutdown, systemd lifecycle, packaged + `pytest` — verify install into a clean venv + tests pass. (co-03, co-04, co-08, co-13, co-16, co-17, co-19, co-22, co-28)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a well-behaved Linux CLI **and** a companion long-running daemon in Python — proper
  argument parsing/config/logging, exit-code discipline, `subprocess`/IPC, and a signal-handled graceful
  shutdown with a systemd-style lifecycle — packaged as a distributable, covered by `pytest`.
- **Concepts exercised**: [ ] a CLI with args/`--help`/exit codes/stdio discipline (co-03, co-04, co-05)
  [ ] config + logging (co-07, co-08) [ ] `subprocess`/pipe IPC with error handling (co-13, co-14, co-15)
  [ ] a long-running daemon (co-18) [ ] signal-handled graceful shutdown (co-16, co-17) [ ] packaging
  (venv/pyproject) (co-21, co-22) [ ] `pytest` over the CLI + daemon (co-28).
- **Ordered steps**:
  1. `.../learning/capstone/code/cli.py` — the CLI (args, `--help`, exit codes, stderr/stdout, config,
     logging). Verify `--help` works and a bad input exits non-zero to stderr.
  2. Add `subprocess`/pipe IPC with error handling. Verify a failed child process is handled and surfaced.
  3. `daemon.py` — a long-running daemon with a SIGTERM-handled graceful shutdown + a systemd-style
     lifecycle. Verify it starts, logs, and shuts down cleanly on signal.
  4. Package it (venv/pyproject) + `pytest`. Verify it installs into a clean venv and the tests (incl.
     signal handling) pass.
- **Acceptance criteria**: the CLI follows exit-code + stdio discipline; IPC errors are handled; the daemon
  shuts down gracefully on SIGTERM; the package installs cleanly; `pytest` passes.
- **Done bar**: runnable end-to-end (Linux) + tests green + web-verified.

## Read more

**Books**

- **GTK+/Gnome Application Development** — Havoc Pennington (1999, New Riders). A classic, widely cited GTK/GNOME app-development book written by a core GNOME developer.

**Papers & articles**

- **GTK documentation** — The GTK Project, official. The authoritative API reference for the GTK toolkit. <https://docs.gtk.org/>
- **Qt documentation** — The Qt Project, official. The authoritative reference for the Qt cross-platform toolkit. <https://doc.qt.io/>
- **XDG Base Directory Specification** — freedesktop.org, official standard. The canonical spec governing where Linux apps store config, data, and cache files. <https://specifications.freedesktop.org/basedir/latest/>
- **Debian Policy Manual** — The Debian Project, official. The canonical packaging standard referenced across Debian-derived Linux distributions. <https://www.debian.org/doc/debian-policy/>

---

← Previous: [75 · Windows App Development](./75-windows-app-development.md) · Next: [77 · Building Production CLI Tools](./77-building-production-cli-tools.md) →
