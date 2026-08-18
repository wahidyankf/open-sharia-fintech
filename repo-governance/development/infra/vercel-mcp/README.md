---
title: "Vercel MCP Capability Convention"
description: "The Vercel MCP server is an assumed capability for plans touching a Vercel-deployed surface, probed at planning time and again at execution Phase 0"
when_to_use: "Read this index to find the right Vercel MCP Capability Convention child document."
---

# Vercel MCP Capability Convention

- [Principles, Conventions, and Core Rule](./principles-conventions-and-core-rule.md) — The assumption that Vercel MCP is available, the principles and conventions behind it, and the two-gate rule that resolves it for a plan. Use when you need the core assumed-availability rule and its two gates, or the principles/conventions this convention builds on.
- [Scope and the Probe](./scope-and-the-probe.md) — How to decide mechanically whether a plan is in scope for this convention, and how to probe whether Vercel MCP is connected and authenticated. Use when checking whether a plan's surface makes it in scope, or when running the probe for Vercel MCP connection state.
- [Capability Boundary and Operational Limits](./capability-boundary-and-operational-limits.md) — The exact boundary of what an agent may read or do through Vercel MCP, and the query-window and truncation limits on its tools. Use when checking whether a planned step falls inside or outside the capability boundary, or when writing acceptance commands against Vercel MCP tools.
- [Identifier Hygiene, Degraded Mode, and When to Check](./identifier-hygiene-degraded-mode-and-when-to-check.md) — Slug-over-ID addressing for Vercel projects and teams, the fallbacks a plan uses when Vercel MCP is absent, and the four moments to re-run the probe. Use when naming a project or team in a committed artifact, planning around an absent Vercel MCP server, or deciding when to re-probe.
- [Examples](./examples.md) — Worked PASS and FAIL examples of applying the Vercel MCP capability boundary and probe-recording rule. Use when checking a plan against worked examples of correct and incorrect Vercel MCP usage.
- [Validation, References, and Platform Binding](./validation-references-and-platform-binding.md) — The agents that validate this convention, related standards and workflows, and the platform-binding details for listing MCP servers. Use when looking up which agent validates this convention, finding related documentation, or checking the MCP-listing binding for a harness.
