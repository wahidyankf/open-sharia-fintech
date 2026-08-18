---
title: "Iteration Examples 1-2: Clean Path and Issue Path"
description: Two worked examples — a new tutorial that reaches EXCELLENT with deferred items, and an existing tutorial update that surfaces missing imports and annotations.
when_to_use: Use as a worked reference for how a clean-path or minor-issue-path iteration plays out end to end.
---

# Iteration Examples 1-2: Clean Path and Issue Path

## Example 1: New By-Example Tutorial (Clean Path)

**Scenario**: Creating Go by-example tutorial from scratch

**Step 1: Maker** (manual creation)

- Author writes 60 examples across 3 levels
- Includes code, some annotations, few diagrams
- Saves to golang/tutorials/by-example/

**Step 2: Checker** (validation)

```bash
apps-ayokoding-www-by-example-checker validates golang by-example
```

**Results**:

- 60 examples (target: 75-85) ️
- Self-containment: 90%
- Annotations: 70% coverage ️
- Diagrams: 20% frequency ️
- Status: **NEEDS IMPROVEMENT**

**Step 3: User Review**

- Reviews audit report
- Approves HIGH confidence fixes
- Approves MEDIUM confidence annotation additions
- Defers diagram additions (will add manually)
- Defers example count increase (needs content planning)

**Step 4: Fixer** (apply fixes)

```bash
apps-ayokoding-www-by-example-fixer applies fixes from audit
```

**Fixes applied**:

- Added 5 missing imports (HIGH)
- Added annotations to meet 1.0-2.25 comment lines per code line density (target: 1.0-2.25, upper bound: 2.5) (MEDIUM, re-validated)
- Fixed 3 color violations (HIGH)
- Added 2 missing key takeaways (MEDIUM)

**Step 5: Re-validation**

```bash
apps-ayokoding-www-by-example-checker re-validates
```

**Results**:

- Self-containment: 100%
- Annotations: 95% coverage
- Diagrams: 20% (deferred) ️
- Example count: 60 (deferred) ️
- Status: **EXCELLENT** (remaining issues are user decisions)

**Outcome**: Publication ready with notes to add diagrams and examples incrementally

## Example 2: Updating Existing Tutorial (Issue Path)

**Scenario**: Updating Elixir by-example with new language features

**Step 1: Maker** (add 10 new examples)

- Author adds 10 examples for Elixir 1.17 features
- Brings total to 70 examples
- Focused on code, minimal annotations

**Step 2: Checker**

```bash
apps-ayokoding-www-by-example-checker validates elixir by-example
```

**Results**:

- 70 examples (target: 75-85) ️
- New examples missing imports
- New examples no annotations
- Status: **NEEDS IMPROVEMENT**

**Step 3: User Review**

- Approves all HIGH + MEDIUM fixes
- Wants to add 5-10 more examples later

**Step 4: Fixer**

```bash
apps-ayokoding-www-by-example-fixer applies fixes
```

**Fixes applied**:

- Added 10 missing imports (HIGH)
- Added annotations to meet density target for new examples (MEDIUM)
- Added 3 key takeaways (MEDIUM)

**Step 5: Re-validation**

```bash
apps-ayokoding-www-by-example-checker re-validates
```

**Results**:

- 70 examples (still below target, deferred)
- All other metrics
- Status: **EXCELLENT**

**Outcome**: Published with plan to add 5-10 examples in next iteration
