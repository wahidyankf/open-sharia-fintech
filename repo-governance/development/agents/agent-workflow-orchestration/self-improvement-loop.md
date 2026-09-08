---
description: "Defines the self-improvement process, the lessons file format, and what makes a good lesson."
when_to_use: Use when an agent wants to record a lesson learned from a mistake or a surprising result.
---

# Self-Improvement Loop

After any correction from the user, extract the lesson.

## The Process

1. **Identify the pattern**: What category of mistake was made? (misread requirement, wrong assumption, insufficient verification, scope creep, etc.)
2. **Write a rule**: Write a concrete rule in `local-tmp/lessons.md` that would prevent this mistake
3. **Iterate**: After repeated mistakes of the same type, revise the rule until the mistake stops occurring
4. **Review at session start**: Check `local-tmp/lessons.md` at the beginning of work on a project to activate relevant lessons

## Lessons File Format

```markdown
## Lessons

### [Date] - [Category]

**Mistake**: [What went wrong]
**Rule**: [Specific, actionable rule to prevent recurrence]
**Context**: [What triggered this lesson]
```

## What Makes a Good Lesson

A useful lesson is specific and actionable:

```
FAIL: "Be more careful when reading requirements."

PASS: "When a requirement says 'update the index', read the existing index first
      to understand its structure before making changes. Assumptions about format
      have caused overwrites twice."
```

Rules that are too general provide no guidance when the situation arises again. Rules that name the specific failure mode and the specific check to perform are actionable.
