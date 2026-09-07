---
description: The mandatory infinite-loop and false-positive safety features, plus how the mode parameter's four levels (lax/normal/strict/ocd) control fix scope.
when_to_use: Use when implementing loop-safety guards or the mode parameter in a new *-check-fix workflow.
---

# \*-check-fix Workflow Pattern — Safety Features and Strictness Parameter

## Safety Features (Mandatory)

**Infinite Loop Prevention**:

- MUST include `max-iterations` parameter (default: 7)
- MUST terminate with `partial` if limit reached
- MUST track iteration count

**False Positive Protection**:

- Fixer MUST re-validate each finding before applying
- Fixer MUST skip FALSE_POSITIVE findings
- Checker MUST use progressive writing

## Strictness Parameter Usage

The `mode` parameter controls which criticality levels must reach zero for workflow success.

**Lax Mode** (minimal validation):

```
User: "Run [workflow-name] in lax mode"
```

Fixes CRITICAL only, reports HIGH/MEDIUM/LOW. Success when zero CRITICAL findings remain.

**Normal Mode** (everyday validation):

```
User: "Run [workflow-name] in normal mode"
```

Fixes CRITICAL/HIGH, reports MEDIUM/LOW. Success when zero CRITICAL/HIGH findings remain.

**Strict Mode** (pre-release validation):

```
User: "Run [workflow-name] in strict mode"
```

Fixes CRITICAL/HIGH/MEDIUM, reports LOW. Success when zero CRITICAL/HIGH/MEDIUM findings remain.

**OCD Mode** (comprehensive audit):

```
User: "Run [workflow-name] in ocd mode"
```

Fixes all levels, zero tolerance. Success when zero findings at all levels.

**Combined with iteration bounds**:

```
User: "Run [workflow-name] in strict mode with min-iterations=2 and max-iterations=7"
```

Applies mode-based fixing with iteration limits.
