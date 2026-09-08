---
description: Worked PASS and FAIL examples of applying the Vercel MCP capability boundary and probe-recording rule.
when_to_use: Use when checking a plan against worked examples of correct and incorrect Vercel MCP usage.
---

# Examples

## PASS: a plan that measures its own effect

A plan converting server-rendered pages to static declares in `tech-docs.md` that a Vercel MCP is
available, and its delivery checklist carries an `[AI]` post-deploy step: re-query runtime log counts
grouped by source and route 24 hours after deploying, and require the function-source count to fall
by at least 90% against a baseline captured at Phase 0. The criterion is falsifiable in both
directions and needs no human.

## PASS: a repository with no Vercel surface

`git ls-files | grep 'vercel\.json$'` returns nothing. The plan states that the repository has no
Vercel-deployed surface and skips both gates. Nothing further is required.

## FAIL: assuming the boundary is wider than it is

A cost-reduction plan tags "read the completed cycle's invoice total" as `[AI]` because a Vercel MCP
is connected. No billing tool exists; the step cannot execute, and it is discovered only when the
executor reaches it. The step belonged in Phase 0 as `[HUMAN]`.

## FAIL: an unrecorded probe

A plan's author probes, finds the server available, and writes `[AI]` deployment steps without
recording the dependency anywhere. A later executor in a session without the server sees `[AI]` tags,
cannot perform them, and has no statement to check against.
