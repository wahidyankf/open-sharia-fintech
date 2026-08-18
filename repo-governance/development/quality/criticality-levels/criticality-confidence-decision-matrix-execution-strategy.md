---
title: "Decision Matrix: Execution Strategy for Fixers"
description: "Fixer execution strategy per priority."
category: explanation
subcategory: development
tags:
  - criticality
  - validation
  - checker-agents
  - fixer-agents
  - quality-assurance
created: 2025-12-27
when_to_use: "Use for a fixer agent's execution-order rules."
---

# Execution Strategy for Fixers

**Fixer agents should process findings in priority order**:

1. **P0 fixes first** (CRITICAL + HIGH confidence)
   - Apply automatically without prompts
   - Block if any P0 fixes fail
   - Report immediately

2. **P1 fixes second** (HIGH + HIGH confidence OR CRITICAL + MEDIUM confidence)
   - Apply HIGH + HIGH automatically
   - Flag CRITICAL + MEDIUM for urgent manual review
   - Continue on failures (don't block)

3. **P2 fixes third** (MEDIUM + HIGH confidence OR HIGH + MEDIUM confidence)
   - Apply MEDIUM + HIGH if user approved batch fixes
   - Flag HIGH + MEDIUM for standard review
   - Skip if not approved

4. **P3-P4 last** (LOW priority combinations)
   - Include in summary only
   - Apply only if explicitly requested
   - No automatic application

**Example execution log**:

```
Fixer Execution Summary:

P0 (CRITICAL + HIGH): 5 findings
   Fixed 5/5 automatically

P1 (HIGH + HIGH): 12 findings
   Fixed 12/12 automatically

P1 (CRITICAL + MEDIUM): 2 findings
  Flagged for urgent manual review:
    - File X: Ambiguous fix target
    - File Y: Context-dependent correction

P2 (MEDIUM + HIGH): 8 findings
   Fixed 8/8 (user approved batch mode)

P2 (HIGH + MEDIUM): 3 findings
  Flagged for standard review

P3-P4: 15 findings
  Included in summary (no action)

Total: 45 findings processed
  - 25 fixed automatically
  - 5 flagged for manual review
  - 15 suggestions only
```

---
