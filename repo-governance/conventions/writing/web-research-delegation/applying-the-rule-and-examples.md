---
description: How agent, skill, and workflow files should cite the delegation rule, with worked good/bad examples
when_to_use: Read this when writing or reviewing the Web Research Delegation subsection of an agent, skill, or workflow file.
---

# Applying the Rule and Examples

## How Agents Apply This Rule

### In an agent definition file

Agents with `WebSearch` or `WebFetch` in their `tools:` list include a short **Web Research Delegation** subsection citing this convention and the delegation threshold. The subsection sits near the "External Information" responsibility or before the core loop.

### In a skill file

Agent skills that describe web verification (for example `docs-validating-factual-accuracy`) do not re-state the delegation rule inline; they cite this convention as the authoritative source and keep only the skill-specific integration notes (for example, how returned confidence tags map to audit-report dual-labels).

### In a workflow

Workflows under `repo-governance/workflows/` that include factual verification steps point to this convention at the relevant step rather than duplicating the threshold.

## Examples

### Good — a checker delegating multi-page research

```markdown
### External Information

For single-shot verification against a known authoritative URL, use `WebFetch` in-context.
For multi-page research (2+ searches or 3+ fetches per claim), delegate to the
[`web-researcher`](../agents/web-researcher.md) subagent per the
[Web Research Delegation Convention](../../repo-governance/conventions/writing/web-research-delegation.md).
```

### Good — a link-checker stating its exception explicitly

```markdown
### Web Research Delegation

This agent is exempt from the [Web Research Delegation Convention](../../repo-governance/conventions/writing/web-research-delegation.md)
default. Its domain is URL reachability (HTTP status, redirect chains), not content research. It invokes
`WebFetch` directly against the URL under test. If content-level research is required (for example, to rewrite
a broken reference), escalate to the maker or checker family, which delegates to `web-researcher`.
```

### Bad — silent ad-hoc searching

```markdown
### Verification

Use WebSearch and WebFetch to check the claim, then write the finding.
```

**Problems:** no threshold, no delegation default, no citation to the convention or the delegated agent. An author reading this has no guidance on when to delegate and no paper trail justifying the choice either way.
