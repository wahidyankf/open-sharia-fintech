---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**Why hash the header as well as content?**

<details><summary>Answer</summary>It binds object type and byte length to the identity, so equal
payload bytes cannot be silently confused across types.</details>

**Why keep a teaching object store isolated?**

<details><summary>Answer</summary>Exercises must never mutate the repository that hosts course
content.</details>

## Calculation practice

For blob text hi, form the header blob, space, payload length, NUL, then payload before hashing.

## Scenario judgment

A commit needs a stable tree and deterministic author metadata for a repeatable fixture. Do not use
a wall-clock value when the test asserts a hash.

## Design exercise

Build an isolated store that writes a blob, creates a one-entry tree, records a commit, and moves a
branch ref to it.

## Automaticity checklist

- [ ] I can distinguish blob, tree, commit, and ref.
- [ ] I can describe index versus working tree.
- [ ] I can explain why a hash is content addressing.
- [ ] I can trace a parent chain.
- [ ] I can name the mutation boundary.

## Why / why not prompts

- Why not store object IDs in a database row?
- Why not write into this repository's .git directory?
- Why not compute a commit hash from its message only?
- Why not use a branch name as immutable history?
- Why does deterministic metadata help tests?
