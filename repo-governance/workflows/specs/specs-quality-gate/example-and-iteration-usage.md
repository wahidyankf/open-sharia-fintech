---
description: "Worked usage examples across all four modes (single folder, cross-folder, strict, ocd), plus a full traced iteration example showing the check-fix loop converging."
when_to_use: "Use when you need a concrete example of invoking this workflow at a given mode, or want to see how consecutive-zero convergence plays out across iterations."
---

# Example and Iteration Usage

## Example Usage

### Single Folder (Normal Strictness)

```
User: "Run specs validation for specs/apps/organiclever"
```

The AI will:

- Validate `specs/apps/organiclever/` and all its subfolders
- Fix CRITICAL and HIGH findings (missing READMEs, wrong counts, broken links)
- Report MEDIUM/LOW findings without fixing them
- Skip cross-folder consistency (only one folder listed)

### Multiple Folders — Cross-Folder Consistency

```
User: "Run specs validation for specs/apps/organiclever and specs/apps/ose"
```

The AI will:

- Validate each folder independently (Categories 1-3, 5-7)
- Check cross-folder consistency between the two application spec trees (Category 4):
  contradictions, coverage gaps, terminology drift, C4 coherence
- Fix CRITICAL and HIGH findings
- Iterate until zero CRITICAL/HIGH findings

### Strict Mode After Refactor

```
User: "Run specs validation for specs/apps/organiclever, specs/apps/ose in strict mode"
```

The AI will:

- Fix CRITICAL/HIGH/MEDIUM findings (includes naming conventions, color palette)
- Check cross-folder consistency
- Report LOW findings without fixing them

### Comprehensive Audit (OCD Mode with Bounds)

```
User: "Run specs validation for specs/apps/organiclever, specs/apps/ose, specs/apps/ayokoding in ocd mode with max-iterations=10"
```

The AI will:

- Validate all 3 listed folders and check consistency across all pairs
- Fix ALL findings at all levels
- Cap at 10 iterations to prevent infinite loops
- Report final status (pass/partial)

## Iteration Example

Typical execution flow (folders: `[specs/apps/organiclever, specs/apps/ose]`):

```
Iteration 1:
  Check organiclever → 4 findings (1 CRITICAL, 2 HIGH, 1 MEDIUM)
    Examples: "Adoption rationale does not explain why the journal context lacks Gherkin [HIGH]",
              "Feature terminology contradicts the bounded-context glossary [HIGH]"
  Check ose → 3 findings (0 CRITICAL, 2 HIGH, 1 LOW)
    Example: "Implementation Alignment: routes-and-screens.md names an unsupported user journey [HIGH]"
  Cross-folder check → 5 findings (0 CRITICAL, 3 HIGH, 1 MEDIUM, 1 LOW)
  Total: 12 findings (1 CRITICAL, 7 HIGH, 2 MEDIUM, 2 LOW)
  [normal mode] Fix 8 (1 CRITICAL + 7 HIGH)
    Note: Fix only retained semantic findings; delegated lifecycle predicates remain outside the
          finding loop and keep their current verified or pending ledger state
  Re-check → 4 findings (0 CRITICAL, 1 HIGH, 2 MEDIUM, 1 LOW)

Iteration 2:
  Fix 1 (1 HIGH — cross-ref broken by README update in iteration 1)
  Re-check → 3 findings (0 CRITICAL, 0 HIGH, 2 MEDIUM, 1 LOW) (consecutive_zero: 1)

Iteration 3 (confirmation):
  Re-check → 3 findings (0 CRITICAL, 0 HIGH, 2 MEDIUM, 1 LOW) (consecutive_zero: 2 — double-zero confirmed)

Result: SUCCESS (3 iterations, 3 below-threshold findings reported)
```
