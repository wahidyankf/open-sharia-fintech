---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

This course turns a program into a dependable command-line interface: one that people can discover,
scripts can compose, and release automation can ship. The 78 runnable Go and Rust examples deliberately
use the standard libraries so that parsing, output streams, exit statuses, configuration precedence,
TTY behavior, tests, and release artifacts remain visible rather than hidden behind a framework.

The examples build in three passes. Beginner examples establish the command contract. Intermediate
examples resolve configuration and interactive-versus-machine behavior. Advanced examples complete
the operating story: tests, cross-compilation, installation, compatibility, and a production-shaped
capstone preview. Each rendered block is synchronized with the colocated `main.go` or `main.rs` file.

Run Go examples with `go run main.go`. Run Rust examples with `rustc main.rs && ./main`. Examples that
intentionally return a non-zero status say so in their surrounding text; inspect their output rather
than treating that status as a failed lesson.

← Previous: [Courses](/en/learn/courses) · Next: [Beginner Examples](./beginner.md)
