---
title: "Trustworthy Measurement — Rule 5: Probes and Scans Must Assert Their Reach"
description: A falsifiability probe proves nothing unless it moves the byte the check actually guards, and a scan proves nothing unless it asserts where it stopped
category: explanation
subcategory: development
tags:
  - measurement
  - false-zero
  - verification
created: 2026-08-19
when_to_use: Use when proving a guard is falsifiable, or when a script locates a region by walking a file.
---

# Rule 5: Probes and Scans Must Assert Their Reach

## A probe must move the byte the check guards

"Edit a file the guard covers, confirm it fails" is only a proof when the edited file is one the
guard compares. A byte-parity check over generated agent mirrors does not guard the README sitting
beside them, so editing that README leaves the validator at exit 0 — a passing probe certifying
nothing. A probe that picks its target with `git ls-files <dir> | head -1` can land on such a file
every time.

**Do**: name the probe target from the guard's own expected set, and record what the exit code was
before and after.

## A scan must assert where it stopped

A script that locates a region by walking forward to "the last matching line" will happily run past
the block it meant to end at. One marker-insertion script walked to the last line beginning with
`|` and found a different table 230 lines away, which would have swallowed half the document.

Sibling shapes already recorded here: a line-oriented match that misses a wrapped checklist item,
and an index anchored on a heading that recurs earlier in the file.

**Do**: stop at the end of the **contiguous** block and assert its size — a table is header +
separator + N rows — rather than trusting the walk.

## An argument-parser error is not the command's verdict

`clap` exits **2** on an unrecognized subcommand, which reads exactly like a validator reporting
failure. Confirm the subcommand exists before treating its exit code as a verdict.

## A build declaration that matches nothing copies nothing

MSBuild's `<None Update="file">` only modifies an item that already exists. Where the SDK's default
item globs do not create one, the declaration matches nothing and the file never reaches the output
directory — silently, with the build green. One such declaration had sat inert in an F# test project
for as long as it existed.

**Do**: assert the artifact appears where it was supposed to land, not that the build succeeded.
