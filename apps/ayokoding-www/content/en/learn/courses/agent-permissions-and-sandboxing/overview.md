---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Why this course exists

A tool-equipped agent can edit files, run commands, and access networks faster than an operator can repair a mistake. Permission policy, sandboxing, and guardrails must therefore be enforced by the harness around an untrusted model and its untrusted inputs, not by asking the model to behave.

## Permission asymmetry

Training or exploration harnesses may deliberately grant broad permissions to observe failure modes, but that permissiveness is a **permission asymmetry** and a risk distinction, not a capability distinction. Production must instead use deny/ask/allow policy, constrained filesystem and network access, auditability, and an explicit approval boundary.

## Prerequisites

Complete [The Agent Loop](../the-agent-loop/learning/overview.md). Familiarity with tool dispatch, filesystem permissions, and the no-secrets-in-git rule is assumed.
