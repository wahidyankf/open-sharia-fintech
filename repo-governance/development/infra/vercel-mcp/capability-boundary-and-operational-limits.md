---
title: "Capability Boundary and Operational Limits"
description: The exact boundary of what an agent may read or do through Vercel MCP, and the query-window and truncation limits on its tools.
category: explanation
subcategory: development
tags:
  - vercel
  - mcp
  - verification
created: 2026-08-01
when_to_use: Use when checking whether a planned step falls inside or outside the capability boundary, or when writing acceptance commands against Vercel MCP tools.
---

# Capability Boundary and Operational Limits

## Capability Boundary

This boundary is the point of the convention. A plan that assumes more than this will write `[AI]`
steps no agent can execute.

**Available** — read and deploy:

- Project and team enumeration; deployment listing, state, and git provenance.
- Runtime logs, including counts grouped by source, route, status code, and deployment — the basis
  for per-project and per-route invocation measurement.
- Build logs and runtime errors.
- Triggering a deployment.
- Deployment-protection settings.

**Not available** — every one of these stays `[HUMAN]`:

- Billing, usage figures, line items, invoices, and any currency value.
- Spend Management.
- Observability settings, including enabling or disabling paid tiers.
- Firewall and WAF managed rulesets.
- The compute-model setting (an agent cannot even read whether it is enabled).
- Domain and DNS configuration, including redirect behaviour.

**The consequence for cost, security, and platform-settings plans**: their dashboard steps do not
become `[AI]` merely because a Vercel MCP is connected. Group every such step into Phase 0 so the
human actions happen in a single sitting, and keep the rest of the plan `[AI]`.

## Operational Limits

Verified against a live project, 2026-08-01. Plans that write acceptance commands must respect these
or the commands fail at execution:

- **Query window**: a 72-hour lookback returns; a 7-day lookback times out. Treat 72h as the widest
  usable window, and never write an acceptance criterion that depends on a longer one.
- **Truncation is silent-ish**: grouped queries return the top _N_ with only a footer saying so.
  Always pass an explicit result limit, or rows vanish without an error.
- **Log events are not billed units.** Counts prove volume and attribution. They never prove cost.
  A plan whose objective is a monetary figure cannot be graded from them.
- **Web Analytics is a separate product** and is not enabled by default. Do not plan around it; a
  query against a project without it fails outright.
