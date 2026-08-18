---
title: "Never guard coverage with a hardcoded count"
description: "Derive a coverage guard's expected set from the source of truth, never a magic count."
category: explanation
subcategory: development
tags:
  - regression
  - testing
  - bug-fix
  - quality
  - gherkin
  - specs
created: 2026-06-22
when_to_use: 'Use when writing a test asserting "nothing escaped the check".'
---

# Never guard coverage with a hardcoded count

When a test asserts "nothing escaped the check", express that as an equality against a **derived
set**, never as a count of members. A magic number fails in exactly the wrong direction on both
sides: it fails **open** in the case that matters (add a command to a target the guard never reads
and the count can still be made to match) and **closed** in the case that does not (any legitimate
restructure trips it).

A real instance: an isolation guard asserted
`assert_eq!(commands.len(), 9, "seven serialized unit commands plus integration and coverage")`. A
later change legitimately collapsed six `cargo test --test X` invocations into one; the guard went
red at 4, reporting a defect where there was only a restructure. The property the guard actually
cared about — every inspected command starts with `env -u GIT_DIR -u GIT_WORK_TREE -u
GIT_COMMON_DIR` — was already asserted on the line above. The count was a proxy for _coverage_: that
the inspected set is the whole set.

The fix is to derive that set from the same source of truth the production code reads — here, an
equality against every `cargo test` / `cargo llvm-cov` string found by scanning all of
`project.json`. It cannot go stale on restructuring, and unlike the count it genuinely fails when a
new direct Cargo command is added to a target the guard does not inspect.

**Whenever a test asserts "how many", ask what set it is really asserting membership of, and derive
that set.**
