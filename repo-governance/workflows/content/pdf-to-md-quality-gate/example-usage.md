---
description: "Worked example invocations covering standard runs, force regeneration, lax mode, custom output paths, and iteration bounds."
when_to_use: "Use when looking for a concrete invocation pattern to copy for a specific scenario."
---

# Example Usage

## Standard Invocation

```
User: "Run pdf-to-md quality gate for docs/reference/nist-sp-800-53-rev5.pdf"
```

AI will:

- Check if MD exists; skip maker if it does
- Validate fidelity in strict mode (default)
- Fix CRITICAL/HIGH/MEDIUM findings
- Iterate until zero CRITICAL/HIGH/MEDIUM findings on 2 consecutive checks

## Force Regeneration

```
User: "Run pdf-to-md quality gate for nist.pdf with force-remake=true"
```

AI will:

- Re-run maker even if MD already exists (full re-conversion)
- Validate and fix as normal

## Quick Critical-Only Check (Lax Mode)

```
User: "Run pdf-to-md quality gate for nist.pdf in lax mode"
```

AI will:

- Fix CRITICAL findings only
- Report HIGH/MEDIUM/LOW without fixing them
- Success when zero CRITICAL findings on 2 consecutive checks

## Custom Output Path

```
User: "Run pdf-to-md quality gate for /data/source.pdf with md-file=/docs/reference/source.md"
```

AI will:

- Generate Markdown at specified output path
- Validate against PDF source

## With Iteration Bounds

```
User: "Run pdf-to-md quality gate for nist.pdf in normal mode with min-iterations=2 and max-iterations=10"
```
