---
title: "Projects with Integration Tests"
description: "Applicability and runtime contract for local-resource Integration targets"
category: explanation
subcategory: development
tags: [nx, targets, integration-testing]
created: 2026-02-23
when_to_use: "Use when implementing or reviewing test:integration."
---

# Projects with Integration Tests

Expose `test:integration` only when a project owns a real local-resource boundary. Integration may
use isolated files, local databases, environment state, child processes, and standard streams. It
must not use HTTP, TCP, UDP, loopback, `localhost`, `127.0.0.1`, or any local server. Setup,
assertions, isolation, and cleanup are part of this boundary.

The target runs only Integration tests. `test:coverage:integration` statically proves that each
applicable Gherkin scenario has exactly one Integration implementation or valid exemption; it does
not execute the suite. During development/review, select impacted scenarios manually. Scheduled
full-quality CI runs the complete suite before E2E.

Projects without this boundary omit both targets and explain why in their README. In-process mocks
belong to Unit; public HTTP/UI journeys belong to E2E.
