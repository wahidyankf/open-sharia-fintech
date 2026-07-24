# Just Enough Bash (Primer, Bash/shell)

**Course ID**: `just-enough-bash` · **Format**: Primer · **Language**: Bash/shell.

**Short summary**: Shell scripting, pipes, redirection, composition

**Scope note**: just enough Bash to drive builds, tests, and tooling from the terminal in every later
topic (the raw-form stance, DD-17); PowerShell is folded into [`80-windows-os`](./windows-os.md), not
taught here. All tooling is OSS (Tier-1, DD-21).

## Why this exists · the big idea

- **The problem before the solution**: every later topic drives builds, tests, and tooling from the
  terminal (DD-17); without shell fluency you cannot glue those tools together or automate the loop.
- **Keep-this-if-you-forget-everything**: small single-purpose tools piped together beat one big program —
  each command does one thing, and the pipe composes them.
- **Big ideas touched**: `coupling-vs-cohesion` — the Unix pipeline is the idea in miniature: highly
  cohesive tools (`grep`, `sort`, `awk`) loosely coupled through plain text streams.

## Prerequisites

- **Prior topics**: [topic 1 Just Enough Nvim](./just-enough-nvim.md) (to edit scripts).
- **Tools & environment**: a macOS/Linux terminal with **Bash** (`bash --version`); the `shellcheck` and
  `shfmt` CLIs installed; standard Unix text tools (`grep`/`sed`/`awk`/`find`). (Windows readers use WSL2
  — DD-25.)
- **Assumed knowledge**: basic terminal navigation; no prior shell scripting required.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28). Re-confirm version pins at authoring.

- 2026-07-12 — verified: current Bash stable **5.3** (July 2025); `set -euo pipefail`, `[[ ]]`, `getopts`
  behavior unchanged; POSIX-`sh`-vs-Bash caveats accurate. (lwn.net / phoronix.com, secondary)
- 2026-07-12 — verified: `shellcheck` **0.11.0** (2025-08-03, still latest). `shfmt` **v3.13.1** (mvdan/sh, latest
  release) — the earlier v3.9.0 pin was stale; re-confirmed against github.com/mvdan/sh/releases.
  (github.com koalaman/shellcheck, mvdan/sh)
- 2026-07-14 — re-confirmed (Phase 6 authoring sweep, `web-researcher`): Bash **5.3** (2025-07-30) is
  still the latest tarball at [ftp.gnu.org/gnu/bash](https://ftp.gnu.org/gnu/bash/), no newer
  `bash-announce` thread exists; `shellcheck` **0.11.0** still the latest
  [release](https://github.com/koalaman/shellcheck/releases); `shfmt` **v3.13.1** still the newest
  [tag](https://api.github.com/repos/mvdan/sh/tags); no breaking changes to `set -euo pipefail`,
  `[[ ]]`, or `getopts` per the [Bash 5.2/5.3 NEWS file](https://tiswww.case.edu/php/chet/bash/NEWS);
  SC2086's wiki title unchanged; _The Linux Command Line_ still the 7th internet edition (version
  25.12) at [linuxcommand.org/tlcl.php](https://linuxcommand.org/tlcl.php). One pre-existing citation
  nuance found (not a 07-12→07-14 change): the POSIX citations below point to the 2017 edition path
  (`9699919799`); the currently-published edition is **Issue 8 / POSIX.1-2024**
  (`9799919799`, published 2024-06-14) at
  [pubs.opengroup.org](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html) —
  the same conclusion (`[[ ]]`/arrays/`<<<` are Bash extensions, absent from POSIX) holds under either
  edition, so no content correction is needed, only a citation-currency note. Bonus finding: POSIX.1-2024
  newly standardizes `set -o pipefail` (absent from the 2017 edition) — this does not contradict
  anything in this syllabus, since co-04's Bash-extensions list never claimed `pipefail` as
  Bash-only, but is noted here for completeness.

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary source fetched and read in the retroactive grounding sweep
> (2026-07-12, `web-researcher`). Sources: GNU Bash Manual (`gnu.org/software/bash/manual` + Chet Ramey's
> maintainer mirror `tiswww.case.edu`), POSIX spec (`pubs.opengroup.org`), `man7.org`, and project GitHub
> releases. 23/25 checkable claims verified; 2 corrected (below).

- **Versions** — Bash **5.3** (2025-07-30, [ftp.gnu.org/gnu/bash](https://ftp.gnu.org/gnu/bash/) +
  [bash-announce](https://lists.gnu.org/archive/html/bash-announce/2025-07/msg00000.html); no 5.4 exists);
  `shellcheck` **0.11.0** (2025-08-03, [release](https://github.com/koalaman/shellcheck/releases/tag/v0.11.0)
  — date corrected from erroneous 2026-01-05); `shfmt` **v3.13.1** ([mvdan/sh tags](https://api.github.com/repos/mvdan/sh/tags)).
- **Strict mode + POSIX delta (co-03/04)** —
  [Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) verbatim for
  `-e`/`-u`/`pipefail`; [POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html)
  (Issue 8 / POSIX.1-2024, the currently-published edition, re-verified 2026-07-14) confirms `[[ ]]`,
  arrays, `<<<` are Bash extensions (absent from the standard).
- **Expansion, conditionals, redirection (co-05/10/14/16)** —
  [Parameter Expansion](https://www.gnu.org/software/bash/manual/bash.html#Shell-Parameter-Expansion)
  (`${v:-}`/`${v:?}`/`${p##*/}`) + [Arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html);
  [Conditional Expressions](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html)
  (`-eq`/`-f`/`-d`/`-z`); [Redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)
  (unquoted-vs-quoted heredoc expansion, `<<<` here-string) — all verbatim.
- **Functions, params, exit codes, getopts, trap, mktemp, braces, regex, process-sub (co-09/13/19/20/21/22/23/24/26)** —
  Chet Ramey's [Bash Reference Manual](https://tiswww.case.edu/php/chet/bash/bashref.html) (`local`, `$?`,
  `$0`/`$@`/`$#`, `{1..5}` inclusive brace expansion, Exit Status);
  [Bourne Shell Builtins](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html)
  (`getopts` colon=arg, `trap` `0`/`EXIT`); [mktemp(1)](https://man7.org/linux/man-pages/man1/mktemp.1.html)
  (`-d`); [grep(1)](https://man7.org/linux/man-pages/man1/grep.1.html) (BRE/ERE/`-E`);
  [Process Substitution](https://www.gnu.org/software/bash/manual/html_node/Process-Substitution.html)
  (`<(…)`/`>(…)`, non-POSIX) — all verbatim.
- **shellcheck SC2086 (co-25, ex-76)** — [SC2086 wiki](https://www.shellcheck.net/wiki/SC2086) title
  "Double quote to prevent globbing and word splitting" — exact match to the unquoted-`$var` scenario.
- **Read more** — _The Linux Command Line_, William Shotts, **latest internet edition (7th, version
  25.12, re-confirmed 2026-07-14)** ([linuxcommand.org/tlcl.php](https://linuxcommand.org/tlcl.php) —
  edition generalized, was stale "5th"); GNU Bash Reference Manual (Chet Ramey), **POSIX.1-2024 /
  Issue 8** (the currently-published edition; superseded IEEE Std 1003.1-2017 — same conclusions on
  Bash-vs-POSIX apply under either edition)
  ([Open Group](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/contents.html)), Google Shell
  Style Guide ([google.github.io](https://google.github.io/styleguide/shellguide.html)) — all confirmed.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 8 (Primer). Each example below cites the co-NN it exercises. -->

- **co-01 · shebang-and-execution** — `#!/usr/bin/env bash` plus `chmod +x` makes a file a runnable
  program; a script can also be run directly with `bash file.sh`.
- **co-02 · interactive-vs-script** — the same shell serves an interactive prompt and non-interactive
  script execution, but scripts run start-to-finish and inherit the calling environment.
- **co-03 · strict-mode** — `set -euo pipefail` makes a script fail fast: abort on any error, treat
  unset variables as errors, and propagate failures through pipelines.
- **co-04 · bash-vs-posix** — Bash adds features (`[[ ]]`, arrays, `<<<`) over portable POSIX `sh`;
  knowing which is which keeps scripts portable when it matters.
- **co-05 · variables-and-expansion** — assignment (`name=value`, no spaces) and expansion
  (`$name`/`${name}`), plus parameter-expansion forms (`${v:-default}`, `${v:?msg}`, `${p##*/}`) and
  arrays.
- **co-06 · quoting** — single quotes are literal, double quotes expand but preserve spacing, and
  unquoted `$var` is word-split and glob-expanded — the source of most shell bugs.
- **co-07 · command-substitution** — `$(...)` captures a command's stdout into a value for use in
  assignments and arguments.
- **co-08 · arithmetic-expansion** — `$(( ))` evaluates integer arithmetic and comparisons without an
  external `expr`.
- **co-09 · exit-codes** — every command returns a status (`0` success, non-zero failure) readable via
  `$?`; `exit N` sets a script's own status.
- **co-10 · conditionals** — `if` with `test`/`[ ]`/`[[ ]]` branches on string, numeric, and file
  tests (`-eq`, `==`, `-f`, `-d`, `-z`).
- **co-11 · case-statement** — `case … esac` matches a value against glob patterns for multi-way
  branching, clearer than an `if`/`elif` chain.
- **co-12 · loops** — `for`, `while`, and `until` iterate over lists, conditions, or ranges, with
  `break`/`continue` controlling flow.
- **co-13 · functions** — functions group reusable commands, take positional parameters, return an
  exit status, and use `local` to scope variables.
- **co-14 · io-redirection** — the three standard streams (stdin/stdout/stderr) redirect with
  `>`, `>>`, `<`, `2>`, and `2>&1` to and from files.
- **co-15 · pipes** — `|` connects one command's stdout to the next command's stdin, composing small
  tools into a pipeline.
- **co-16 · here-docs-and-strings** — `<<EOF` feeds a multi-line block (expanded, or literal with
  `<<'EOF'`) and `<<<` feeds a single string as stdin.
- **co-17 · read-input** — `read -r` consumes a line of stdin into one or more variables, the basis of
  interactive prompts and line-by-line file loops.
- **co-18 · text-pipeline-tools** — `grep`, `sed`, `awk`, `cut`, `sort`, `uniq`, `tr`, `xargs`, and
  `find` are the composable single-purpose filters that pipelines chain together.
- **co-19 · positional-parameters** — `$1`…`$9`, `$@`, `$#`, `$0`, and `shift` expose a script's
  arguments; `"$@"` preserves each argument's word boundaries.
- **co-20 · getopts** — the `getopts` builtin parses short options (`-v`, `-o value`) into a loop,
  pairing with a `--help`/usage message.
- **co-21 · trap-and-cleanup** — `trap` registers handlers that run on `EXIT`, `INT`, or `ERR`,
  guaranteeing cleanup and error reporting even when a script aborts.
- **co-22 · mktemp** — `mktemp`/`mktemp -d` create collision-safe temporary files and directories for
  scratch work, paired with `trap` cleanup.
- **co-23 · globbing** — filename expansion (`*`, `?`, `[...]`) matches paths on the command line;
  quoting and empty-match handling keep loops safe.
- **co-24 · regular-expressions** — POSIX BRE/ERE (via `grep -E`/`sed -E`) use character classes,
  anchors (`^`/`$`), quantifiers (`+`/`*`/`{n}`), and capture groups — the pattern language under the
  pipeline tools.
- **co-25 · shellcheck-and-shfmt** — `shellcheck` statically finds shell bugs (unquoted vars, unset
  refs) and `shfmt` formats scripts, the same gates this repo enforces.
- **co-26 · process-substitution** — `<(cmd)` and `>(cmd)` expose a command's stdout/stdin as a
  filename (`/dev/fd/*`), letting tools that expect file arguments (`diff`, `comm`, `paste`) read from
  live pipelines without a temp file — a Bash extension, not POSIX `sh`.

## Worked examples

Colocated under `just-enough-bash/learning/code/`; each is a complete executable script run with
`bash <file>` (DD-20/DD-30), `shellcheck`-clean, and cites the `co-NN` it exercises. Contiguous
`ex-01..ex-83`.

### Beginner

- **ex-01 · shebang-script** — a script with `#!/usr/bin/env bash` that prints a greeting — verify
  `bash hello.sh` prints exactly `Hello, world!`. (co-01)
- **ex-02 · make-executable** — `chmod +x hello.sh` then `./hello.sh` — verify it runs and prints the
  greeting without an explicit `bash`. (co-01)
- **ex-03 · strict-mode-header** — a script beginning `set -euo pipefail` — verify it runs clean and
  `echo $?` prints `0`. (co-03)
- **ex-04 · unset-var-fails** — reference an undefined variable under `set -u` — verify the script exits
  non-zero and stderr contains `unbound variable`. (co-03, co-05)
- **ex-05 · assign-and-echo** — assign `name="Ada"` and `echo "$name"` — verify stdout is `Ada`.
  (co-05)
- **ex-06 · brace-var-expansion** — use `${name}` inside a string — verify stdout is `Hi Ada`. (co-05)
- **ex-07 · single-vs-double-quote** — `echo '$name'` vs `echo "$name"` — verify stdout is the literal
  `$name` then the expanded `Ada`. (co-06)
- **ex-08 · quoting-spaces** — loop over a variable holding `"a b"` quoted vs unquoted — verify the
  quoted form is one word and the unquoted form splits into two. (co-06, co-23)
- **ex-09 · command-substitution** — `year="$(date +%Y)"; echo "$year"` — verify stdout is a 4-digit
  year. (co-07)
- **ex-10 · arithmetic** — `echo $(( 6 * 7 ))` — verify stdout is `42`. (co-08)
- **ex-11 · arithmetic-increment** — increment `i=$(( i + 1 ))` inside a loop — verify the final printed
  value is the loop count. (co-08, co-12)
- **ex-12 · exit-code-success** — run `true; echo $?` — verify stdout is `0`. (co-09)
- **ex-13 · exit-code-failure** — run `false; echo $?` — verify stdout is `1`. (co-09)
- **ex-14 · explicit-exit** — a script ending `exit 3` — verify `bash s.sh; echo $?` prints `3`.
  (co-09)
- **ex-15 · if-string-test** — `if [[ "$a" == "$b" ]]` on equal values — verify it prints `equal`.
  (co-10)
- **ex-16 · if-numeric-test** — `if [[ $n -gt 10 ]]` for `n=20` — verify it prints `big`. (co-10)
- **ex-17 · if-file-test** — `if [[ -f data.txt ]]` on an existing file — verify it prints `exists`.
  (co-10)
- **ex-18 · test-vs-bracket** — compare `test -d dir` and `[ -d dir ]` on the same directory — verify
  both branches print the same result. (co-10, co-04)
- **ex-19 · for-loop-list** — `for x in a b c; do echo "$x"; done` — verify stdout is `a`, `b`, `c`.
  (co-12)
- **ex-20 · for-loop-range** — `for i in {1..5}; do echo -n "$i "; done` — verify stdout is `1 2 3 4 5`.
  (co-12)
- **ex-21 · while-loop** — a `while` loop counting to 3 — verify stdout is `1`, `2`, `3`. (co-12)
- **ex-22 · until-loop** — an `until` loop that stops when a counter reaches 3 — verify stdout is `0`,
  `1`, `2`. (co-12)
- **ex-23 · break-continue** — a loop that `continue`s on even and `break`s at 5 — verify only the
  expected odd values before 5 print. (co-12)
- **ex-24 · echo-to-stdout** — `echo` a line — verify stdout matches the argument exactly. (co-14)
- **ex-25 · redirect-to-file** — `echo hi > out.txt` — verify `out.txt` contains exactly `hi`. (co-14)
- **ex-26 · append-to-file** — `echo more >> out.txt` after the previous write — verify `out.txt` now
  holds two lines. (co-14)
- **ex-27 · redirect-stderr** — send an error to `2> err.txt` — verify `err.txt` is non-empty and
  stdout stays clean. (co-14)
- **ex-28 · simple-pipe** — `printf 'b\na\n' | sort` — verify stdout is `a` then `b`. (co-15)

### Intermediate

- **ex-29 · case-statement** — `case "$1" in start|stop|*)` dispatching on the first argument — verify
  each input routes to the matching branch. (co-11)
- **ex-30 · function-define-call** — define `greet() { echo "Hi $1"; }` and call it — verify stdout is
  `Hi Ada`. (co-13)
- **ex-31 · function-local-var** — a function setting a `local` variable — verify the same-named outer
  variable is unchanged after the call. (co-13)
- **ex-32 · function-return-status** — a function that `return 1` and a caller that checks it — verify
  the failure branch runs. (co-13, co-09)
- **ex-33 · positional-params** — a script echoing `$1`, `$2`, and `$#` — verify counts and values for
  a sample invocation. (co-19)
- **ex-34 · all-args-quoted** — loop over `"$@"` with an argument containing a space — verify each
  argument prints on its own line intact. (co-19, co-06)
- **ex-35 · shift-args** — consume arguments with `shift` in a loop — verify each argument is processed
  once and none remain. (co-19)
- **ex-36 · read-from-stdin** — `read -r line` from piped input — verify it echoes the piped line.
  (co-17)
- **ex-37 · read-loop-file** — `while read -r line; do …; done < file` — verify each file line is
  processed in order. (co-17, co-12)
- **ex-38 · heredoc** — a `cat <<EOF` block referencing `$name` — verify the multi-line output has the
  variable expanded. (co-16)
- **ex-39 · heredoc-quoted** — a `cat <<'EOF'` block — verify `$name` prints literally, unexpanded.
  (co-16)
- **ex-40 · here-string** — `grep foo <<< "$text"` — verify it matches when `$text` contains `foo`.
  (co-16, co-18)
- **ex-41 · pipe-grep** — `printf '...\n' | grep pattern` — verify only matching lines print. (co-15,
  co-18)
- **ex-42 · grep-count** — `grep -c pattern file` — verify stdout is the exact match count. (co-18)
- **ex-43 · sed-substitute** — `sed 's/old/new/g'` over a line — verify every `old` becomes `new`.
  (co-18)
- **ex-44 · sed-delete-lines** — `sed '/DROP/d'` — verify lines containing `DROP` are removed. (co-18)
- **ex-45 · awk-field** — `awk '{print $2}'` on space-separated input — verify the second column prints.
  (co-18)
- **ex-46 · awk-sum** — `awk '{sum+=$1} END{print sum}'` over numbers — verify the printed total is
  correct. (co-18)
- **ex-47 · cut-columns** — `cut -d, -f2` on a CSV line — verify the second field prints. (co-18)
- **ex-48 · sort-uniq-count** — `sort | uniq -c` on repeated lines — verify each line prints with its
  count. (co-18)
- **ex-49 · tr-translate** — `tr 'a-z' 'A-Z'` — verify lowercase input prints uppercased. (co-18)
- **ex-50 · find-files** — `find . -name '*.txt'` — verify it lists every matching path. (co-18)
- **ex-51 · find-exec-delete** — `find . -name '*.tmp' -delete` — verify the `.tmp` files are gone
  afterward. (co-18)
- **ex-52 · xargs-pipeline** — `find . -name '*.txt' | xargs grep -l TODO` — verify it lists files
  containing `TODO`. (co-18, co-15)
- **ex-53 · pipeline-chore** — a `find | grep | awk | sort` chain solving a real chore — verify the
  final aggregated output. (co-15, co-18)
- **ex-54 · stderr-to-stdout** — `cmd 2>&1 | grep error` merging streams into a pipe — verify the error
  line is captured. (co-14, co-15)
- **ex-55 · devnull-discard** — `noisy_cmd > /dev/null 2>&1` — verify no output prints while the exit
  status is preserved. (co-14)
- **ex-56 · getopts-flags** — parse `-v` and `-o file` with `getopts` — verify the parsed flag and value
  print correctly. (co-20)
- **ex-57 · getopts-usage** — print usage on `-h` or an invalid option — verify `-h` exits 0 and a bad
  option exits non-zero. (co-20, co-09)
- **ex-58 · default-value-param** — use `${1:-default}` for a missing argument — verify the default is
  used when no argument is passed. (co-05, co-19)
- **ex-59 · check-command-success** — `if grep -q pattern file; then` guarding on exit status — verify
  the correct branch runs. (co-09, co-10)
- **ex-60 · pipefail-catches-failure** — a pipeline whose first stage fails under `set -o pipefail` —
  verify the pipeline's exit status is non-zero. (co-03, co-15)

### Advanced

- **ex-61 · trap-exit-cleanup** — `trap 'rm -f "$tmp"' EXIT` around some work — verify the temp file is
  gone after the script finishes. (co-21)
- **ex-62 · mktemp-file** — `tmp="$(mktemp)"` used then cleaned via `trap` — verify a unique temp file
  is created and removed on exit. (co-22, co-21)
- **ex-63 · mktemp-dir** — `dir="$(mktemp -d)"` scratch directory — verify it is created, used, and
  removed on exit. (co-22, co-21)
- **ex-64 · trap-signal-int** — `trap 'echo interrupted' INT` — verify sending `SIGINT` prints the
  handler message instead of silently dying. (co-21)
- **ex-65 · regex-grep-ere** — `grep -E '^[0-9]{3}-[0-9]{4}$'` over mixed lines — verify only
  phone-shaped lines match. (co-24, co-18)
- **ex-66 · regex-char-class** — `grep -E '[[:digit:]]+'` — verify lines containing digits match.
  (co-24)
- **ex-67 · regex-anchors** — `grep -E '^ERROR'` — verify only lines starting with `ERROR` match, not
  mid-line occurrences. (co-24)
- **ex-68 · regex-capture-sed** — `sed -E 's/(foo)bar/\1baz/'` backreference — verify `foobar` becomes
  `foobaz`. (co-24, co-18)
- **ex-69 · regex-quantifiers** — `grep -E 'ab+c'` — verify `abc` and `abbc` match but `ac` does not.
  (co-24)
- **ex-70 · safe-glob-loop** — `for f in ./*.txt; do [[ -e "$f" ]] || continue; …` — verify the loop
  skips cleanly when no `.txt` files exist. (co-23, co-12)
- **ex-71 · array-iteration** — define `arr=(a b c)` and loop `"${arr[@]}"` — verify each element prints
  on its own line. (co-05, co-12)
- **ex-72 · array-length** — print `${#arr[@]}` for a 3-element array — verify stdout is `3`. (co-05)
- **ex-73 · param-expansion-required** — `: "${INPUT:?input required}"` when unset — verify the script
  exits non-zero and stderr shows `input required`. (co-05, co-09)
- **ex-74 · string-manipulation** — `${path##*/}` for basename and `${file%.*}` to strip an extension —
  verify both extractions print correctly. (co-05)
- **ex-75 · shellcheck-clean** — run `shellcheck good.sh` on a correct script — verify it reports no
  findings and exits 0. (co-25)
- **ex-76 · shellcheck-catches-bug** — run `shellcheck` on a script with an unquoted `$var` — verify it
  reports `SC2086`. (co-25, co-06)
- **ex-77 · shfmt-format** — `shfmt -d messy.sh` shows a diff, then `shfmt -w` fixes it — verify a
  re-run of `shfmt -d` reports no diff. (co-25)
- **ex-78 · robust-arg-parser** — a `getopts` parser with usage plus validation of a required option —
  verify it exits non-zero with a message when the required option is missing. (co-20, co-09)
- **ex-79 · temp-pipeline-atomic** — write output to a `mktemp` file then `mv` it to the final path only
  on success — verify no partial output file exists after a mid-run failure. (co-22, co-21, co-09)
- **ex-80 · trap-err-report** — `trap 'echo "failed at line $LINENO"' ERR` — verify a failing command
  prints the offending line number. (co-21, co-03)
- **ex-81 · full-report-tool** — an end-to-end script combining `getopts`, a text pipeline, `trap`+
  `mktemp`, and exit codes — verify correct output for valid input plus cleanup and non-zero exit on
  error. (co-20, co-18, co-21, co-22, co-09)
- **ex-82 · posix-portable-script** — a script using only POSIX `sh` constructs — verify it produces
  identical output under both `sh script.sh` and `bash script.sh`. (co-04)
- **ex-83 · process-substitution-diff** — `diff <(sort a.txt) <(sort b.txt)` comparing two live
  pipelines without temp files — verify the diff output matches what temp-file staging would produce,
  and that `diff <(sort a.txt) <(sort a.txt)` reports no differences. (co-26, co-18)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: write one robust, `shellcheck`-clean Bash tool (~60–120 lines) that parses options with
  `getopts`, processes text through a pipeline, cleans up with `trap`+`mktemp`, and returns correct exit
  codes — the kind of helper later topics reuse.
- **Concepts exercised**: [ ] `set -euo pipefail` [ ] `getopts` + `--help` [ ] safe quoting [ ] a
  `grep`/`awk`/`sort` pipeline [ ] `trap` cleanup + `mktemp` [ ] correct exit codes.
- **Ordered steps**:
  1. `just-enough-bash/learning/capstone/code/report.sh` — parse `-i <input> -o <output>` via `getopts`,
     print usage on `-h`/bad args. Verify `./report.sh -h` prints usage, exits 0.
  2. Implement the pipeline writing to a `mktemp` scratch file, moved to `-o` on success; `trap` removes
     scratch on any exit. Verify `shellcheck report.sh` is clean and the output file matches expected.
  3. Verify a missing input exits non-zero with a stderr message and leaves no scratch file behind.
- **Acceptance criteria**: `shellcheck` clean; correct output for valid input; correct non-zero exit +
  cleanup on error.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **The Linux Command Line: A Complete Introduction** — William Shotts (latest internet edition, free; 7th as of 2026-07-12). Comprehensive free intro from basics through real shell scripting. <https://linuxcommand.org/tlcl.php>

**Papers & articles**

- **GNU Bash Reference Manual** — FSF / Chet Ramey. Official canonical reference for Bash syntax, builtins, behavior. <https://www.gnu.org/software/bash/manual/bash.html>
- **POSIX Shell & Utilities (IEEE Std 1003.1)** — The Open Group / IEEE. Formal standard defining portable `sh` that Bash supersets. <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/contents.html>
- **Google Shell Style Guide** — Google. Widely adopted pragmatic style guide for maintainable production Bash. <https://google.github.io/styleguide/shellguide.html>

## In which paths

- `interview-ready/software-engineer` — Prologue · Editor foundations (skippable for the experienced).
- `immediately-effective/software-engineer` — Stage 1 · Editor & tooling (get set up fast).
- `fundamentally-strong/software-engineer` — Prologue · Editor & reproducible forge (skippable).

> _Content originated in the now-closed FS-SE plan (topic 5); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
