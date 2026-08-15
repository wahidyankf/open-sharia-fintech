---
title: "Capstone: CMake Task CLI"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Build and run the light consolidation CLI in [`../code/ex-72-capstone-cpp-cli/`](../code/ex-72-capstone-cpp-cli/). Its library uses a header/source split, RAII
through `unique_ptr`, a template, STL containers and algorithms, a lambda, and exceptions. CMake
builds a library, CLI, and CTest target with `-Wall -Wextra -Wpedantic` enabled for the library.

```bash
cmake -S ../code/ex-72-capstone-cpp-cli -B build
cmake --build build
ctest --test-dir build --output-on-failure
./build/task-cli
```

For supported GCC or Clang sanitizer verification, configure a separate build with address and UB
sanitizer flags, then run the same CTest and CLI commands. No raw `new` or `delete` appears in the
capstone.
