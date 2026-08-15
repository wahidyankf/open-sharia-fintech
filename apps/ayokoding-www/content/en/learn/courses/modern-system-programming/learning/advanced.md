---
title: "Advanced Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 30
---

Examples 53–78 establish the safety boundary. A raw pointer is not permission to ignore an
invariant: every dereference needs a local proof. The FFI lessons use a Rust-defined C ABI symbol
so all 78 examples stay portable and runnable without a platform library. Async examples explain
the shape without adding a runtime dependency; the capstone is standard-library-first.
