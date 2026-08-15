---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Run a single-source example from its directory with:

```bash
c++ -std=c++17 -Wall -Wextra -Wpedantic main.cpp -o example && ./example
```

The CMake examples state their build commands. Each source comment is part of the lesson: `// =>`
marks the ownership, state, or observable result that matters at that line. Every example uses only
the C++17 standard library and is independent of earlier examples.

For a sanitizer posture, add `-fsanitize=address,undefined -fno-omit-frame-pointer` to a supported
compiler invocation, then run the binary. Treat warnings as defects to fix, not noise to ignore.
