---
description: Documents how to trigger the workflow (with or without parameters) and the loop-prevention, convergence, false-positive, error-recovery, and user-control safety mechanisms it relies on.
when_to_use: Use when you need the exact invocation syntax, or when you need to understand how the workflow protects against runaway iteration or unsafe auto-fixes.
---

# Workflow Invocation and Safety Features

## Agent Delegation (Preferred)

**User triggers workflow execution**:

```
User: "Run ayokoding-web annotated-concept quality gate workflow for computer-science-foundations/learning/"
```

**AI orchestrates all phases**:

1. **Create content** (if needed): User writes worked examples or uses maker agent
2. **Validate**: Invoke `apps-ayokoding-www-annotated-concept-checker` via Agent tool
3. **Review**: User reads audit report from local-tmp/ayokoding-web-annotated-concept/
4. **Fix**: Invoke `apps-ayokoding-www-annotated-concept-fixer` via Agent tool
5. **Re-validate**: Invoke checker via Agent tool again
6. **Iterate**: Repeat validation-fixing until clean or max-iterations

**With parameters**:

```
User: "Run ayokoding-web annotated-concept quality gate workflow for computer-science-foundations/learning/ in strict mode with max-iterations=10"
```

The AI invokes agents with mode-based fixing and iteration limits.

## Safety Features

**Infinite Loop Prevention**:

- max-iterations defaults to 7 (override with higher value for more attempts)
- When provided, workflow terminates with `needs-improvement` if limit reached
- Tracks iteration count and finding trends
- Use max-iterations when fix convergence is uncertain

**Convergence Safeguards**:

- Checker loads `.known-false-positives.md` skip list at start of each iteration
- Fixer persists new FALSE_POSITIVEs to skip list after each run
- Re-validation uses scoped scan (changed files only) to prevent scope expansion
- Escalation after repeated checker-fixer disagreements on the same finding

**False Positive Protection**:

- Fixer re-validates findings before applying
- Skips FALSE_POSITIVE findings automatically
- Progressive writing ensures audit history survives

**Error Recovery**:

- Continues to finalization even if fixer partially fails
- Reports which fixes succeeded/failed
- Generates final reports regardless of status

**User Control**:

- Auto-fix-level parameter controls automation degree
- Manual decision points at user review step
- Can abort and return to maker for major rework
