---
description: "The priority matrix and priority-level explanations."
when_to_use: "Use to map a criticality+confidence pair to a priority."
---

# Criticality x Confidence Decision Matrix: Priority Levels

## Criticality × Confidence Decision Matrix

This matrix shows how criticality and confidence combine to determine **priority** and **fix strategy**.

| Criticality  | HIGH Confidence                                               | MEDIUM Confidence                                   | FALSE_POSITIVE                                             |
| ------------ | ------------------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------------- |
| **CRITICAL** | **P0** - Auto-fix immediately<br>Block deployment until fixed | **P1** - URGENT manual review<br>High priority flag | Report with CRITICAL context<br>Improve checker urgently   |
| **HIGH**     | **P1** - Auto-fix after P0<br>Fix before publication          | **P2** - Standard manual review<br>Normal priority  | Report with HIGH context<br>Improve checker soon           |
| **MEDIUM**   | **P2** - Auto-fix after P1<br>Requires user approval          | **P3** - Optional review<br>Low priority            | Report with MEDIUM context<br>Note for checker improvement |
| **LOW**      | **P3** - Include in batch fixes<br>User decides if/when       | **P4** - Suggestions only<br>No urgency             | Report with LOW context<br>Informational only              |

### Priority Levels Explained

- **P0** (Blocker): Must fix before any publication/deployment
- **P1** (Urgent): Should fix before publication, can proceed with approval
- **P2** (Normal): Fix in current cycle when convenient
- **P3** (Low): Fix in future cycle or batch operation
- **P4** (Optional): Suggestion only, no action required
