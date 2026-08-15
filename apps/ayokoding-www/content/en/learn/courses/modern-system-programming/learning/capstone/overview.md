---
title: "Capstone: Safe Concurrent Byte Tool"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Build the four workspace crates in order from `code/`:

1. `core` returns `Result` from its ownership-correct byte parser.
2. `concurrent` moves jobs through channels and aggregates them behind `Arc<Mutex<_>>`.
3. `abstract` makes the aggregation a generic iterator/trait operation with static dispatch.
4. `ffi` calls a C function through a safe wrapper. Its only `unsafe` block is documented with the
   pointer and ABI contract.

Run `cargo build --workspace && cargo test --workspace` from this directory. The FFI build script
uses the host C compiler (`cc`) and archive tool (`ar`); on Windows use an MSVC-compatible developer
shell. The wrapper passes a copied integer, so no allocation ownership crosses the boundary.
