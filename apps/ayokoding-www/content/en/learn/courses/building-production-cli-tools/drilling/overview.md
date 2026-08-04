---
title: "Five Production CLI Drills"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Use these five drills as short, repeatable implementation exercises. Do each from an empty directory;
compare behavior with the stated contract before looking at the examples again.

## Recall Q&A

1. Which stream should carry machine-readable command output?
   <details><summary>Answer</summary>Standard output. Diagnostics belong on standard error so a pipe
   can consume only the intended data.</details>
2. Why is an exit code part of a command's public interface?
   <details><summary>Answer</summary>Scripts and users need a stable success or failure signal even
   when the human-readable message changes.</details>
3. Where should flag, environment, and default precedence be decided?
   <details><summary>Answer</summary>In one pure resolution boundary that every command path shares.</details>

## Applied problems

1. A JSON consumer breaks because progress text is mixed into its input. Separate human diagnostics
   to standard error and make `--json` emit only the documented object.
2. A deployment command accepts contradictory configuration sources. Define one precedence function
   and table-test every source combination before calling the network.
3. A release works on a developer laptop but not in CI. Record the target, artifact name, help
   contract, and version output as observable release requirements.

## Code katas

### Kata 1: Preserve a Pipe

Write `count` in Go. It accepts words on standard input, writes only the number of words to standard
output, and writes a `read N bytes` diagnostic to standard error. Verify that `printf 'a b\n' | count | xargs`
receives only `2`.

### Kata 2: Define an Exit Contract

Write a Rust `check FILE` command. It exits `0` and prints `ok` when `FILE` exists; it prints a useful
error naming the file to standard error and exits `2` when the argument is absent, and `1` when the
file cannot be read.

### Kata 3: Resolve Configuration Once

Write a Go `deploy` command with `--region`, `DEPLOY_REGION`, and a `local` default. Put precedence
resolution in one pure function and add a table-driven test for all four combinations.

### Kata 4: Separate Human and Machine Modes

Write a Rust `status --json` command. Its default mode says `service api: healthy`; JSON mode emits
exactly `{"service":"api","healthy":true}` and no headings, colors, or progress text.

### Kata 5: Release the Same Interface Everywhere

Extend the capstone with `--version`, `completion bash`, and a `GOOS=linux GOARCH=arm64 go build`
release command. Record the exact command and artifact name in a release note, then test help, JSON,
and the missing-argument exit status as separate contracts.

## Self-check checklist

- [ ] I can keep data, diagnostics, and exit status as three separate CLI contracts.
- [ ] I can resolve configuration once and exercise the resolver with a table-driven test.
- [ ] I can make human and machine output modes incompatible by design rather than convention.
- [ ] I can reproduce a release with an explicit target and artifact name.

## Elaborative interrogation and self-explanation

1. Why can a command look successful to a person while still being broken for a script?
2. Why does one configuration resolver reduce release risk more than duplicating precedence rules?
3. Why should a JSON command avoid headings even when the human mode benefits from them?

← Previous: [Capstone](../../learning/capstone/overview) · Next: [Courses](/en/learn/courses)
