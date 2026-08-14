---
title: "No Time Estimates"
description: "The rule prohibiting time-based framing in educational content, with its rationale and where it does and does not apply"
category: explanation
subcategory: conventions
tags:
  - content-quality
  - markdown
  - writing-standards
  - accessibility
  - documentation
created: 2025-12-07
when_to_use: "Read this before writing tutorial or how-to content that might mention a duration, or when reviewing content for time-estimate language."
---

# No Time Estimates

**Do NOT include time estimates in educational or tutorial content.**

**Rationale**:

- Time estimates create artificial pressure on learners
- Everyone learns at different speeds
- Focus should be on WHAT learners accomplish, not HOW LONG it takes
- Makes content evergreen (no need to update time claims)
- Reduces anxiety and creates pressure-free learning environment

**Forbidden Time Estimates**:

FAIL: **Avoid (time-based claims)**:

```markdown
This tutorial takes 2-3 hours to complete.
Estimated time: 45 minutes
Duration: 1-2 hrs
You'll learn this in 30 minutes.
Time needed: 20 min
```

PASS: **Good (focus on outcomes, not duration)**:

```markdown
By the end of this tutorial, you'll be able to...
This tutorial covers the fundamentals of...
You'll learn how to build a complete application.
Coverage: 60-85% of domain knowledge (intermediate depth)
```

**Exception - Coverage Percentages Allowed**:

Coverage percentages are allowed because they indicate **depth/scope**, not **time**:

- PASS: "Coverage: 0-5%" (indicates initial setup scope)
- PASS: "Coverage: 60-85%" (indicates intermediate depth)
- PASS: "Coverage: 85-95%" (indicates advanced depth)

**Where This Applies**:

- All tutorial content (`docs/tutorials/`)
- Educational content in ayokoding-www
- How-to guides that teach concepts
- Reference documentation with learning components

**Where This Does NOT Apply**:

- Project planning documents (`plans/`) - can estimate implementation time
- Development task tracking - can estimate effort
- Meeting agendas - can allocate time slots

PASS: **Good (Well-Structured Paragraphs)**:

```markdown
Authentication tokens provide secure access to protected resources. Each
token includes user identity, permissions, and expiration time.

Tokens expire after 1 hour of inactivity. Before expiration, clients can
request a new token using the refresh token endpoint. This extends the
session without requiring re-authentication.

Failed refresh attempts trigger automatic logout. The user must log in
again to continue. This security measure prevents unauthorized access
attempts.
```

FAIL: **Avoid (Wall of Text)**:

```markdown
Authentication tokens provide secure access to protected resources and
each token includes user identity, permissions, and expiration time and
tokens expire after 1 hour of inactivity so before expiration clients can
request a new token using the refresh token endpoint which extends the
session without requiring re-authentication but if refresh attempts fail
then automatic logout is triggered and the user must log in again to
continue which is a security measure that prevents unauthorized access
attempts.
```
