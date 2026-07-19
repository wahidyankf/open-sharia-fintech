# 77 · Building Production CLI Tools (By Example, Go + Rust †)

**prd row**: Pass 4 · Concurrency & Systems · By Example · Go + Rust † · Learn 177 / Drill 277 · Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: CLIs people actually enjoy using — argument parsing, subcommands, the config/flags/env
precedence chain, good help/errors/exit codes, honest TTY-vs-pipe behavior, and distribution as a single
binary. Cross-platform and anchored in Go and Rust, the two languages that dominate modern CLI tooling.
The telemetry instincts from [`63-analytics-and-experimentation`](./63-analytics-and-experimentation.md)
inform how a tool reports itself, and the shell fluency from
[`05-just-enough-bash`](./05-just-enough-bash.md) is what your tool has to compose with. `†`: Go and Rust
building native, statically-linkable binaries.

## Why this exists · the big idea

- **The problem before the solution**: the terminal is full of tools that are technically correct and
  miserable to use — cryptic flags, no `--help`, silent failures, exit code 0 on error, color codes dumped
  into a pipe, and installation that means "clone this and hope." A tool that ignores CLI convention becomes
  a tool people avoid or misuse.
- **Keep-this-if-you-forget-everything**: a good CLI is a contract with both a human at a keyboard and a
  script in a pipeline — it obeys convention (flags, exit codes, stdout-for-data/stderr-for-messages),
  detects whether it is talking to a terminal or a pipe, and fails loudly and specifically. Design for the
  pipe as carefully as for the person.
- **Big ideas touched**: `mechanism-vs-policy` (the tool's engine is the mechanism; flags, config, and env
  vars are how the user sets policy — keeping them separate is what makes a tool scriptable and
  composable), `coupling-vs-cohesion` (subcommands keep each verb's logic cohesive, while a clean core/CLI
  boundary keeps the tool's engine decoupled from its argument-parsing shell).

## Prerequisites

- **Prior topics**: [topic 63 Analytics & Experimentation](./63-analytics-and-experimentation.md)
  (honest measurement and self-reporting) and [topic 5 Just Enough Bash](./05-just-enough-bash.md) (pipes,
  exit codes, stdout/stderr, the shell environment a CLI lives in).
- **Tools & environment**: a macOS/Linux/Windows terminal; the **Go toolchain** (`go`) and/or the **Rust
  toolchain** (`cargo`), pinned to a current stable; a mature arg-parsing library per language (a
  `cobra`/`urfave`-style parser for Go, a `clap`-style parser for Rust); Neovim/VSCode with the Go/Rust LSP
  (DD-17).
- **Assumed knowledge**: pipes, exit codes, and stdout-vs-stderr (topic 05); building and running a native
  binary (topics 64/82); reading Go or Rust well enough to follow a small program (topics 64/82).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the design conventions are stable and correctly unpinned — POSIX/GNU argument
  syntax, the flags-over-env-over-config precedence idea, `0`-for-success exit codes, stdout-for-data /
  stderr-for-diagnostics, and TTY detection (`isatty`) for color/progress are long-settled and documented
  in `clig.dev` and the POSIX Utility Conventions. Keep both toolchains at "a current stable" in shipped
  text.
- 2026-07-12 — verified (GAP for plan owner): the body references arg-parsing libraries by role rather than
  a pinned version — re-verify the specific Go and Rust parser package names/versions once the worked
  examples are drafted; their public API is stable but the exact version should be current at authoring
  time.

### DD-35 primary-source citations (fetched-and-read)

Per DD-35, every convention/library claim below traces to a primary source; anything version-pinned is
flagged for re-pull at authoring time.

- **CLI design conventions** — `[Verified]` POSIX/GNU argument syntax, the flags→env→config→defaults
  precedence idea, `0`-for-success exit codes, stdout-for-data / stderr-for-diagnostics, and `isatty`-based
  TTY detection are documented in `clig.dev` and the POSIX Utility Conventions
  (pubs.opengroup.org/onlinepubs/9699919799 §12, clig.dev). These are long-settled — keep unpinned.
- **clig.dev authorship** — `[Verified]` the Command Line Interface Guidelines are authored by **Aanand
  Prasad, Ben Firshman, Carl Tashian, Eva Parish** (clig.dev). (Corrected a prior citation error that named
  a non-existent author.)
- **Go arg-parsers** — `[Verified]` at 2026-07-12, `cobra` latest is **v1.10.2**, `urfave/cli` latest is
  **v3.10.1** (note: v3 is a major bump from v2 with breaking API changes) (github.com/spf13/cobra/releases,
  github.com/urfave/cli/releases). **`[Needs Verification]` at authoring** — re-pull both before drafting
  code; do NOT pin a version in shipped prose, keep the toolchain at "a current stable".
- **Rust arg-parser** — `[Verified]` at 2026-07-12, `clap` latest is **v4.6.1** and `clap_complete` (shell
  completion) is **v4.6.7** (crates.io/crates/clap, crates.io/crates/clap_complete). **`[Needs
Verification]` at authoring** — re-pull before drafting; keep unpinned in prose.
- **TTY detection** — `[Verified]` `isatty(3)` / the Go `term.IsTerminal` / Rust `std::io::IsTerminal`
  (stable since Rust 1.70) are the standard interactive-terminal checks (man7.org/linux/man-pages/man3/
  isatty.3, doc.rust-lang.org/std/io/trait.IsTerminal.html). Exact Go helper package is `[Needs
Verification]` at authoring (`golang.org/x/term` vs a parser-provided helper).
- **Cross-compilation** — `[Verified]` Go uses `GOOS`/`GOARCH` env vars; Rust uses `cargo build --target
<triple>` with `rustup target add` (go.dev/doc, doc.rust-lang.org/rustc/targets). Single static binaries
  are the distribution model for both.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject). Each example below cites the co-NN it exercises. -->

- **co-01 · arg-parsing** — a CLI parses positional arguments and short/long flags into a typed command.
- **co-02 · subcommands** — a subcommand tree (`tool verb`) organizes related commands.
- **co-03 · flag-types** — flags carry bool/string/int/repeated values, optionally required.
- **co-04 · double-dash** — `--` ends flag parsing so trailing args pass through literally.
- **co-05 · generated-help** — the parser auto-generates discoverable `--help` / usage text.
- **co-06 · version-flag** — `--version` reports the tool's version.
- **co-07 · config-precedence** — configuration resolves flags → environment → config-file → defaults, in that order.
- **co-08 · env-config** — environment variables (often namespaced) supply configuration.
- **co-09 · config-file** — a config file supplies configuration below env/flags in precedence.
- **co-10 · defaults** — sensible defaults apply when nothing else sets a value.
- **co-11 · exit-codes** — `0` signals success, non-zero signals failure, with meaningful codes per failure class.
- **co-12 · stdout-data** — the tool's data output goes to stdout so it composes in pipes.
- **co-13 · stderr-diagnostics** — errors and human messages go to stderr, keeping stdout clean.
- **co-14 · error-messages** — errors are actionable: they name what failed and suggest a fix.
- **co-15 · tty-detection** — `isatty`-style detection tells the tool whether it talks to a terminal or a pipe.
- **co-16 · color-output** — color is emitted only on a TTY (and suppressed when piped or via `--color`).
- **co-17 · progress-bars** — progress indicators show interactively but never pollute piped output.
- **co-18 · prompts** — interactive prompts appear only on a TTY.
- **co-19 · quiet-verbose** — `--quiet`/`--verbose` modes control output volume.
- **co-20 · shell-completion** — the tool generates shell-completion scripts.
- **co-21 · machine-output** — a `--json`/machine mode emits clean, parseable output for scripts.
- **co-22 · single-binary** — the tool builds to a single static binary with no runtime install.
- **co-23 · cross-compilation** — the binary is cross-compiled for multiple OS/arch targets.
- **co-24 · packaging-install** — the tool ships via packaging/install paths (archives, PATH placement).
- **co-25 · go-cobra** — Go builds CLIs with a mature parser (`cobra`/`urfave`).
- **co-26 · rust-clap** — Rust builds CLIs with `clap` (derive API) + `clap_complete`.
- **co-27 · core-cli-boundary** — the tool's engine (core) is separated from its argument-parsing shell.
- **co-28 · signal-handling** — Ctrl-C / SIGINT interrupts the tool cleanly.
- **co-29 · testing-cli** — CLI behaviour (exit codes, output) is tested, often with golden files.
- **co-30 · posix-gnu-convention** — flag syntax follows POSIX/GNU convention (short clustering, long `--flags`).

## Tensions & trade-offs — when NOT to reach for this

- **When a script would do**: not every automation deserves a compiled, flag-parsed, cross-compiled binary.
  A twenty-line shell or Python script is the right tool for a one-off or a personal utility — building a
  "production CLI" for it is over-engineering.
- **Feature creep kills composability**: the Unix philosophy is do-one-thing-well for a reason. A CLI that
  grows an interactive menu, its own config DSL, and a plugin system becomes an application wearing a
  terminal costume — harder to script and harder to reason about than the small tools it replaced.
- **Convention over cleverness**: reinventing flag syntax, exit-code meanings, or output format because you
  think you can do better breaks every user's muscle memory and every downstream script. The "when not" here
  is: do not deviate from POSIX/GNU convention without a reason your users will thank you for.

## Lineage — why it beat the alternative

- CLI conventions were forged in early Unix: small single-purpose tools composed through pipes, with stdout
  as the data channel and exit codes as the success signal — the design that made the shell a programmable
  environment. The scripting-language era (Perl/Python CLIs) added rich arg-parsing but often shipped as
  "install the interpreter and these dependencies first." The Go and Rust generation closed that last gap:
  a single statically-linked binary you can drop onto any machine, with mature parser libraries
  (`cobra`/`clap`) that make convention the path of least resistance. Each step kept the Unix contract and
  removed a distribution or ergonomics tax. The mechanism/policy separation and clean binaries built here
  carry straight into the lower-level tooling of [`78-just-enough-c`](./78-just-enough-c.md) and every
  systems tool you ship afterward.

## Worked examples

Colocated under `building-production-cli-tools/learning/code/`; each runnable, built and exercised from the CLI in Go and/or Rust (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · go-hello-cli** — a Go single-command CLI printing output — verify `go run` output. (co-01, co-25)
- **ex-02 · rust-hello-cli** — a Rust CLI with `clap` printing output — verify `cargo run` output. (co-01, co-26)
- **ex-03 · bool-flag** — a `--verbose` bool flag — verify it toggles. (co-03)
- **ex-04 · string-flag** — a `--name` string flag — verify the value. (co-03)
- **ex-05 · int-flag** — a `--count` int flag — verify parsing. (co-03)
- **ex-06 · positional-arg** — a positional argument — verify it's read. (co-01)
- **ex-07 · short-long-flag** — `-v`/`--verbose` alias — verify both work. (co-01, co-30)
- **ex-08 · double-dash** — `--` stops flag parsing — verify trailing args pass through. (co-04)
- **ex-09 · go-help** — Go generated `--help` — verify the usage text. (co-05, co-25)
- **ex-10 · rust-help** — `clap` generated `--help` — verify the usage text. (co-05, co-26)
- **ex-11 · version-flag** — `--version` prints the version — verify output. (co-06)
- **ex-12 · exit-zero** — exit 0 on success — verify `$?` is 0. (co-11)
- **ex-13 · exit-nonzero** — exit non-zero on error — verify `$?` is non-zero. (co-11)
- **ex-14 · stdout-data** — print data to stdout — verify capture. (co-12)
- **ex-15 · stderr-error** — print an error to stderr — verify separation. (co-13)
- **ex-16 · error-message** — an actionable error message — verify it names the fix. (co-14)
- **ex-17 · unknown-flag** — an unknown flag exits non-zero with a message — verify the error. (co-14, co-11)
- **ex-18 · default-value** — a flag's default when unset — verify the default runs. (co-10)
- **ex-19 · env-read** — read a config value from an env var — verify it's used. (co-08)
- **ex-20 · go-subcommand** — a Go subcommand (`cobra`) — verify dispatch. (co-02, co-25)
- **ex-21 · rust-subcommand** — a `clap` subcommand — verify dispatch. (co-02, co-26)
- **ex-22 · subcommand-help** — per-subcommand help — verify each renders. (co-02, co-05)
- **ex-23 · required-flag** — a required flag missing errors — verify the error. (co-03, co-14)
- **ex-24 · repeated-flag** — `-v -v` repeated / count flag — verify the count. (co-03)
- **ex-25 · posix-cluster** — POSIX flag clustering `-abc` — verify it parses. (co-30)
- **ex-26 · go-build-binary** — `go build` a single binary — verify it runs. (co-22, co-25)

### Intermediate

- **ex-27 · config-file-load** — load a config file (toml/yaml) — verify values. (co-09)
- **ex-28 · flag-over-env** — a flag overrides an env var — verify the flag wins. (co-07, co-08)
- **ex-29 · env-over-config** — env overrides the config file — verify env wins. (co-07, co-09)
- **ex-30 · config-over-default** — config overrides the default — verify config wins. (co-07, co-10)
- **ex-31 · full-precedence** — the full flags→env→config→default chain resolved — verify the winner. (co-07)
- **ex-32 · subcommand-tree** — a nested subcommand tree — verify deep dispatch. (co-02)
- **ex-33 · subcommand-flags** — subcommand-local flags — verify scoping. (co-02, co-03)
- **ex-34 · persistent-flags** — a global/persistent flag across subcommands — verify inheritance. (co-02, co-03)
- **ex-35 · tty-detect** — `isatty` detection — verify the TTY-vs-pipe branch. (co-15)
- **ex-36 · color-on-tty** — color only when interactive — verify no codes when piped. (co-16, co-15)
- **ex-37 · color-force-flag** — a `--color=always/never/auto` flag — verify the override. (co-16)
- **ex-38 · progress-on-tty** — a progress bar only on a TTY — verify none when piped. (co-17, co-15)
- **ex-39 · machine-json** — a `--json` clean machine output — verify parseable JSON. (co-21)
- **ex-40 · pipe-clean-output** — piping stdout yields no decoration — verify clean data. (co-21, co-16)
- **ex-41 · quiet-mode** — `--quiet` suppresses non-errors — verify only errors show. (co-19)
- **ex-42 · verbose-mode** — `--verbose` adds detail to stderr — verify extra logs. (co-19, co-13)
- **ex-43 · prompt-on-tty** — an interactive prompt only when a TTY — verify it's skipped when piped. (co-18, co-15)
- **ex-44 · go-completion** — generate Go shell completion (`cobra`) — verify a completion script. (co-20, co-25)
- **ex-45 · rust-completion** — generate `clap` completion (`clap_complete`) — verify a completion script. (co-20, co-26)
- **ex-46 · exit-code-map** — distinct exit codes per failure class — verify the mapping. (co-11)
- **ex-47 · stderr-vs-stdout-pipe** — data piped while errors still show — verify separation under a pipe. (co-12, co-13)
- **ex-48 · core-function** — the tool's engine as a testable core function — verify it's callable headless. (co-27)
- **ex-49 · cli-calls-core** — the CLI shell calls the core — verify the boundary. (co-27, co-02)
- **ex-50 · sigint-handling** — Ctrl-C interrupts cleanly — verify graceful exit. (co-28)
- **ex-51 · go-test-cli** — a Go test of exit code + output — verify green. (co-29, co-25)
- **ex-52 · rust-test-cli** — a Rust integration test (assert_cmd-style) — verify green. (co-29, co-26)
- **ex-53 · golden-output-test** — a golden-file output test — verify stable output. (co-29)
- **ex-54 · help-snapshot-test** — snapshot the `--help` text — verify it matches. (co-29, co-05)

### Advanced

- **ex-55 · cross-compile-go** — `GOOS`/`GOARCH` cross-compile — verify a foreign-target binary. (co-23, co-22)
- **ex-56 · cross-compile-rust** — `cargo build --target` cross-compile — verify a foreign-target binary. (co-23, co-26)
- **ex-57 · static-binary** — a fully static binary (no libc dep) — verify it runs standalone. (co-22)
- **ex-58 · two-platform-build** — build for two platforms — verify both artifacts. (co-23)
- **ex-59 · install-path** — an install path / PATH placement — verify the command resolves. (co-24)
- **ex-60 · package-release** — a release archive with the binary + completion — verify the contents. (co-24, co-20)
- **ex-61 · config-precedence-full** — the full precedence chain in a subcommand — verify resolution. (co-07, co-02)
- **ex-62 · tty-color-progress** — color + progress interactively, clean when piped — verify both modes. (co-16, co-17, co-15)
- **ex-63 · json-and-human** — dual human/`--json` output modes — verify each. (co-21, co-12)
- **ex-64 · actionable-errors** — errors that name the flag + suggest a fix — verify the message. (co-14, co-13)
- **ex-65 · exit-code-discipline** — a script consuming the tool's exit codes — verify branching. (co-11)
- **ex-66 · completion-both-shells** — bash + zsh completion — verify both scripts. (co-20)
- **ex-67 · signal-cleanup** — SIGINT mid-work cleans up temp state — verify no leftovers. (co-28)
- **ex-68 · verbose-quiet-combo** — verbose/quiet with correct precedence — verify the resolved level. (co-19)
- **ex-69 · posix-gnu-parity** — GNU long + POSIX short parity — verify both syntaxes. (co-30, co-01)
- **ex-70 · go-vs-rust-same-cli** — the same CLI in Go and Rust — verify identical behaviour. (co-25, co-26)
- **ex-71 · core-cli-test-split** — test the core headless + the CLI end-to-end — verify both. (co-27, co-29)
- **ex-72 · env-prefix** — a namespaced env prefix (`TOOL_*`) — verify only prefixed vars apply. (co-08, co-07)
- **ex-73 · machine-pipe-integration** — pipe the tool's JSON into `jq` — verify the pipeline. (co-21, co-12)
- **ex-74 · completion-install** — install completion into the shell — verify tab-complete. (co-20, co-24)
- **ex-75 · error-to-stderr-code** — an error prints to stderr AND sets a non-zero code — verify both. (co-13, co-11)
- **ex-76 · subcommand-plus-precedence** — a subcommand tool with full precedence + help — verify the whole. (co-02, co-07, co-05)
- **ex-77 · integration-tty-slice** — a TTY-aware subcommand tool with color/progress/json — verify all modes. (co-15, co-16, co-17, co-21)
- **ex-78 · capstone-production-cli** — a production CLI: subcommand tree, full precedence, stdout/stderr + exit codes, TTY-aware output, `--version` + completion, cross-compiled to two platforms — verify subcommands/help, precedence order, pipe-clean output, both binaries run. (co-02, co-07, co-11, co-13, co-15, co-16, co-06, co-20, co-23)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: ship one small production-quality CLI (Go or Rust) with a subcommand tree, the full
  configuration-precedence chain, discoverable help and meaningful exit codes, TTY-aware output that stays
  clean in a pipe, and a cross-compiled single-binary release for at least two platforms.
- **Concepts exercised**: [ ] subcommands + flags + generated help (co-02, co-03, co-05) [ ] flags → env →
  config → defaults precedence (co-07) [ ] stdout-for-data / stderr-for-diagnostics + non-zero exit codes
  (co-12, co-13, co-11) [ ] TTY-vs-pipe detection for color/progress (co-15, co-16, co-17) [ ] `--version` +
  shell completion (co-06, co-20) [ ] a cross-compiled single-binary build for two targets (co-22, co-23).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a subcommand tree with flags, `--help`, and `--version`. Verify each
     subcommand's help renders and an unknown flag exits non-zero.
  2. Implement the config precedence chain. Verify a flag overrides an env var, which overrides a config
     file, which overrides the default — and that the resolved value is what runs.
  3. Split output: data on stdout, diagnostics on stderr, meaningful exit codes. Verify piping stdout yields
     clean machine-readable output while errors still surface on stderr with a non-zero code.
  4. Add TTY-aware color/progress and cross-compile a single binary for two platforms with completion.
     Verify color/progress appear interactively but not when piped, and that both binaries run on their
     targets.
- **Acceptance criteria**: subcommands and help work; precedence resolves in the documented order;
  stdout/stderr and exit codes obey convention; output adapts to TTY vs pipe; the tool builds to a single
  binary on two platforms.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **The Art of Unix Programming** — Eric S. Raymond (2003, Addison-Wesley; free CC-licensed edition
  author-hosted). The classic articulation of the Unix philosophy underlying good CLI tool design.
  <http://www.catb.org/esr/writings/taoup/html/>

**Papers & articles**

- **Command Line Interface Guidelines** — Aanand Prasad, Ben Firshman, Carl Tashian, Eva Parish (ongoing,
  open source). The modern, widely cited canonical guide to designing CLI tools. <https://clig.dev/>
- **POSIX.1 / The Open Group Base Specifications (Utility Conventions)** — IEEE / The Open Group, official
  standard. The formal standard defining conventional CLI argument syntax that most Unix-family tools
  follow. <https://pubs.opengroup.org/onlinepubs/9699919799/>
- **The Linux man-pages project** — Michael Kerrisk et al., official (kernel.org project). The canonical
  documentation model and reference for well-documented CLI tools on Linux.
  <https://man7.org/linux/man-pages/>

---

← Previous: [76 · Linux App Development](./76-linux-app-development.md) · Next: [78 · Just Enough C](./78-just-enough-c.md) →
