---
title: "Build Automation Capstone"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

Build the course-owned polyglot artifact in `learning/capstone/`: Make delegates the JavaScript build to
npm, uses a pattern rule for a second artifact, aggregates them under `all`, and exposes the same work
through just. Run `make`, run it again to observe no work, change one source, then use `make -j` and
`just build` to confirm the graph and aliases agree.

## Build automation capstone

Run the capstone from this directory. The top-level Makefile aggregates an npm-produced JavaScript
artifact and a compiled native artifact. The justfile provides aliases only; Make remains responsible
for timestamp-driven file freshness.

1. Run <code>make -j all</code> to build both independent outputs.
2. Run <code>make</code> again to see the unchanged native file target skipped.
3. Edit <code>native.c</code>, run <code>make</code>, and observe only the native chain rebuild.
4. Run <code>make clean</code> to remove generated output, or <code>just build</code> when just is installed.
