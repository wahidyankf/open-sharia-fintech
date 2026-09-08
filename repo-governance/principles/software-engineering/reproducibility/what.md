---
description: Defines reproducibility and non-reproducibility and contrasts their environment, build, and documentation characteristics.
when_to_use: Use when clarifying the precise meaning of "reproducible environment" before applying the principle.
---

# What

**Reproducibility** means:

- Same repository clone produces identical environment
- Same inputs produce identical builds
- Version-controlled environment configuration
- Explicit dependency versions (no "latest")
- Documented setup process
- Deterministic builds (same commit = same artifact)

**Non-reproducibility** means:

- "Works on my machine" problems
- Different builds from same code
- Implicit system dependencies
- Floating version numbers
- Undocumented setup steps
- Non-deterministic builds
