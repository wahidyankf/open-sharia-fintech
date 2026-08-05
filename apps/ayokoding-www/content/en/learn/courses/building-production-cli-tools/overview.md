---
title: "Overview"
date: 2026-08-04T00:00:00+07:00
draft: false
weight: 1
---

Production CLI tools are contracts for both people and automation: they make commands discoverable,
keep data on stdout and diagnostics on stderr, report useful exit codes, and remain predictable in a
terminal or a pipeline. This course presents paired Go and Rust examples where comparing their tooling
sharpens the design lesson.

## Prerequisites

- Complete [Just Enough Go](../just-enough-go/learning/overview.md). It supplies the Go executable
  examples and basic toolchain fluency used throughout this course.
- Just Enough Rust is scheduled independently in Plan 07. The declared prerequisite resolves when that
  course lands; until then, use the Rust examples as comparisons alongside the Go route.
- Be comfortable with shell pipelines, command exit codes, and the difference between stdout and
  stderr.

## What you will build

The learning track contains annotated examples for parsing arguments, subcommands, configuration
precedence, terminal-aware output, testing, cross-compilation, and packaging. The capstone is a small
production-style CLI with a clean core/CLI boundary and cross-build verification.

## Scope boundary

This is a CLI design and delivery course, not a Go or Rust language primer. Just Enough Go and the
scheduled Just Enough Rust own the prerequisite language foundations; the paired snippets reinforce
the CLI contract rather than replacing either curriculum. Shell syntax is assumed, and GUI, service,
and web application interfaces remain out of scope.
