---
description: Pass/fail examples for tutorials, how-tos, coverage percentages, and the project-planning exception.
when_to_use: Use when writing or reviewing tutorial, how-to, or plan content for time-estimate violations.
---

# How It Applies

## Tutorial Content

**Context**: Educational documentation and learning materials.

PASS: **Outcome-Focused (Correct)**:

```markdown
# React Quick Start

By the end of this tutorial, you'll be able to:

- Create React components
- Manage state with hooks
- Handle user events
- Build a simple interactive app

Coverage: 5-30% of React fundamentals
```

**Why this works**: Describes WHAT you'll learn. No pressure. Clear outcomes.

FAIL: **Time-Based (Avoid)**:

```markdown
# React Quick Start

️ Estimated time: 2-3 hours

This tutorial will teach you React basics in under 3 hours.
```

**Why this fails**: Creates anxiety if you take longer. Inaccurate for most learners.

## How-To Guides

**Context**: Problem-solving documentation.

PASS: **Outcome-Focused (Correct)**:

```markdown
# How to Deploy to Production

This guide walks through production deployment steps:

1. Configure environment variables
2. Set up database
3. Deploy application
4. Verify deployment

You'll have a working production deployment by the end.
```

**Why this works**: Describes outcome (working deployment). No time pressure.

FAIL: **Time-Based (Avoid)**:

```markdown
# How to Deploy to Production

️ Takes approximately 30-45 minutes

Quick 30-minute deployment guide.
```

**Why this fails**: 30 minutes for expert, 4 hours for beginner. Creates false expectations.

## Coverage Percentages (Allowed)

**Context**: Indicating tutorial depth.

PASS: **Coverage Percentages (Correct)**:

```markdown
# Beginner Tutorial

Coverage: 0-60% of domain knowledge

Teaches fundamentals needed for 90% of real-world use cases.
```

**Why this works**: Indicates **depth/scope**, not duration. No time pressure.

**Important**: Coverage percentages describe **how much of the domain** you'll learn, not **how long it takes**.

## Project Planning (Exception)

**Context**: Project management documents in `plans/`.

PASS: **Time Estimates Allowed (In Planning Context)**:

```markdown
# Project Plan

Implementation estimate: 2-3 weeks

Tasks:

- Database schema: 2 days
- API endpoints: 1 week
- Frontend: 1 week
```

**Why this is acceptable**: Project planning requires resource allocation. This is for team coordination, not learner pressure.

**Not applicable to**: Educational content, tutorials, documentation, how-to guides.
