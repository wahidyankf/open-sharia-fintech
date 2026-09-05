---
title: "Guarded Admission and Parallelism"
description: One outer HIPPO boundary per compute-bearing DAG node, which reservations each class makes, and the only two worker variables OSE maps.
category: explanation
subcategory: development
tags:
  - resource-management
  - parallelism
  - development
  - tooling
created: 2026-09-05
when_to_use: Use when wiring a build, test, generator, or gate command, or when deciding whether two nodes must be serialized.
---

# Guarded Admission and Parallelism

Run each independent compute-bearing DAG node through one outer HIPPO boundary. Nodes may enter
concurrently; HIPPO atomically admits CPU-and-memory vectors only when shared capacity and host
pressure allow. A build, validation, toolchain, or worktree command is not itself a serial edge.

Serialize only for dependency, shared-output, ordered Rhino byte identity, transaction, or a
documented runtime race. The N=3 agent budget limits agent work streams; it is separate from
HIPPO's child allocation and cannot override admission.

All `service`, `ephemeral`, and `transactional` owners reserve capacity. Automatic `balanced`,
`constrained`, and `minimal` requests use four, two, and one safe-capacity shares. Explicit requests
may be smaller but not below one CPU or 256 MiB. Admission reserves both dimensions under strict
FIFO; pressure may defer a request even when its vector fits.

OSE maps fixed CPU allocation only to `NX_PARALLEL` and `DOTNET_PROCESSOR_COUNT`: missing values
receive it, lower positive values survive, and higher values are clamped. Inner commands inherit
the session; never add another outer guard or an unowned ecosystem mapping.
