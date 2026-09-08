---
description: "Clarifies that annotation density is measured per individual example rather than as a file average, and gives the validation and content-creation approach."
when_to_use: "Read when validating or creating example content, to confirm density must be checked per example and not averaged across a file."
---

# Self-Containment Rules: Per-Example Annotation Density Measurement

**CRITICAL: Density is measured PER INDIVIDUAL EXAMPLE, not as file average**

This is a CRITICAL distinction that affects validation and content creation:

- PASS: **CORRECT**: Each example (Example 1, Example 2, etc.) must individually achieve 1.0-2.25 comment lines per code line
- FAIL: **INCORRECT**: Averaging density across entire file (beginner.md, intermediate.md, advanced.md)

**Why per-example measurement matters**:

1. **Consistent learning experience**: Users learn from individual examples. Every example should have consistent annotation depth.
2. **Quality enforcement**: File averages hide problems - a few over-annotated examples can mask many under-annotated ones.
3. **Fixer precision**: Validation reports must identify which specific examples need more/fewer annotations, not just file totals.

**Validation approach**:

- Measure code lines and comment lines for EACH example separately
- Flag examples below 1.0 density (under-annotated, needs enhancement)
- Flag examples above 2.5 density (over-annotated, needs condensing)
- Target range: 1.0-2.25 per example (optimal educational value)
- File averages are informative but NOT the validation criteria

**Content creation approach**:

When creating examples, ensure EACH example meets density target:

- Simple example (basic variable assignment): ~1.0 density
- Complex example (concurrency with channels): ~2.0-2.25 density
- Do NOT rely on file averages to "balance out" sparse examples
