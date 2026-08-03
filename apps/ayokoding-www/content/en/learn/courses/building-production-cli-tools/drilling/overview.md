---
title: "Five Production CLI Drills"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Use these five drills as short, repeatable implementation exercises. Do each from an empty directory;
compare behavior with the stated contract before looking at the examples again.

## Drill 1: Preserve a Pipe

Write `count` in Go. It accepts words on standard input, writes only the number of words to standard
output, and writes a `read N bytes` diagnostic to standard error. Verify that `printf 'a b\n' | count | xargs`
receives only `2`.

## Drill 2: Define an Exit Contract

Write a Rust `check FILE` command. It exits `0` and prints `ok` when `FILE` exists; it prints a useful
error naming the file to standard error and exits `2` when the argument is absent, and `1` when the
file cannot be read.

## Drill 3: Resolve Configuration Once

Write a Go `deploy` command with `--region`, `DEPLOY_REGION`, and a `local` default. Put precedence
resolution in one pure function and add a table-driven test for all four combinations.

## Drill 4: Separate Human and Machine Modes

Write a Rust `status --json` command. Its default mode says `service api: healthy`; JSON mode emits
exactly `{"service":"api","healthy":true}` and no headings, colors, or progress text.

## Drill 5: Release the Same Interface Everywhere

Extend the capstone with `--version`, `completion bash`, and a `GOOS=linux GOARCH=arm64 go build`
release command. Record the exact command and artifact name in a release note, then test help, JSON,
and the missing-argument exit status as separate contracts.

← Previous: [Capstone](../../learning/capstone/overview) · Next: [Courses](/en/learn/courses)
