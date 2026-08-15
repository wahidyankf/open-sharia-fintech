---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

This capstone assembles the agent loop, tools, context, permissions, and observability courses into a
local coding assistant. It is an integration project, not a source of new agent concepts.

## Prerequisites

Bring the full harness cluster, async Python, and test-driven development. The optional browser-MCP
extension belongs to `browser-automation-with-cdp`; it must remain explicitly approved and scoped.

## Done bar

Given a failing local test, the fake-provider agent reads an approved workspace, proposes a patch,
runs the test, records a trace and audit event, and stops at its budget. No live model, secret, or
unapproved command is required for the deterministic suite.
