---
title: "AI Agent Model Selection Convention"
description: Standards for selecting the appropriate model tier (planning-grade, execution-grade, fast) for AI agents based on task complexity
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - standards
  - development
created: 2026-04-03
---

# AI Agent Model Selection Convention

This document defines the standards for selecting the appropriate model tier when creating or updating AI agents. The governing principle is **match model capability to task complexity** -- use the most capable model only when the task demands it, and use lighter models for structured or mechanical work.

> **Note on terminology**: "planning-grade", "execution-grade", and "fast" are **internal repo vocabulary**, not an externally-recognized cross-vendor standard. Web research (2026-05-03) found no community usage of these tier names outside this repository. They serve as a vendor-neutral capability axis used by `repo-governance/` prose; concrete vendor model IDs (e.g., `claude-opus-4-7`, `zai-coding-plan/glm-5.2`) live in platform-binding agent frontmatter and in the [AI Model Benchmarks Reference](../../../docs/reference/ai-model-benchmarks.md).

## Principles Implemented/Respected

This practice implements the following core principles:

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Select the simplest model that can accomplish the task. Avoid using opus-tier reasoning for tasks that follow fixed patterns or templates. Simpler models reduce latency and resource consumption without sacrificing quality on structured work.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Every agent MUST declare its model tier in frontmatter and include a `Model Selection Justification` comment explaining why that tier was chosen. No implicit defaults -- the reasoning is transparent and auditable.

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Model selection requires deliberate analysis of what cognitive capabilities the task demands. Agents should not default to the highest tier "just in case" -- each selection reflects a considered judgment about the task's actual requirements.

## Conventions Implemented/Respected

This practice respects the following conventions:

- **[Content Quality Principles](../../conventions/writing/quality.md)**: Agent frontmatter and model justification comments follow active voice and clarity standards.

## Purpose

Model selection directly affects agent quality, latency, and resource efficiency. Selecting too powerful a model wastes resources on simple tasks; selecting too weak a model produces poor results on complex work. This convention establishes clear criteria for matching model tiers to task types, ensuring consistent and justified model assignments across all agents.

## Scope

### What This Convention Covers

- Model tier definitions and their cognitive capabilities
- Decision criteria for selecting each tier
- Task-to-tier mapping with concrete examples
- Justification requirements for model selection

### What This Convention Does NOT Cover

- Tool permission selection (see [AI Agents Convention](./ai-agents.md))
- Agent color categorization (see [AI Agents Convention](./ai-agents.md))
- Agent naming and file structure (see [AI Agents Convention](./ai-agents.md))
- Workflow orchestration (see [Agent Workflow Orchestration](./agent-workflow-orchestration.md))

## Model Tiers

### Planning-Grade (Inherit / No Model Specified)

**When to use**: Tasks requiring creative reasoning, architectural decisions, code generation, multi-step judgment calls, or nuanced content creation.

**Cognitive profile**: Deep analytical reasoning, novel problem-solving, multi-step planning, creative synthesis across domains, nuanced judgment under ambiguity.

**Task characteristics**:

- Open-ended problems without a single correct answer
- Architectural decisions requiring trade-off analysis
- Code generation across multiple languages and paradigms
- Content creation requiring domain expertise and originality
- Multi-step planning with conditional branching
- Tasks where the agent must invent approaches, not follow templates

**Agent examples**:

- **SWE developers** (all language-specific agents) -- generate and refactor production code across diverse language ecosystems, requiring deep understanding of idioms, patterns, and trade-offs
- **plan-maker** -- creates project plans requiring scope analysis, dependency mapping, and strategic sequencing
- **docs-tutorial-maker** -- produces tutorial content requiring pedagogical reasoning, narrative flow, and learning progression design
- **swe-ui-maker** -- creates UI components requiring CVA variants, Radix composition, accessibility, tests, and stories in one pass

**Frontmatter**: Omit the `model` field. This is intentional — the agent inherits the
session's active model.

```yaml
---
name: swe-typescript-dev
description: Expert TypeScript/Node.js developer...
tools: [Read, Write, Edit, Glob, Grep, Bash]
color: purple
---
```

**Budget-Adaptive Inheritance**: Omitting `model` is a deliberate design choice, not an
oversight. The agent inherits the calling session's model, which adapts to the user's
account tier and token budget:

| Session plan               | Inherited model | Output quality |
| -------------------------- | --------------- | -------------- |
| Max / Team Premium         | `Opus 4.7`      | Highest        |
| Pro / Standard / API       | `Sonnet 4.6`    | High           |
| Bedrock / Vertex / Foundry | `Sonnet 4.5`    | High           |

This means a Max-plan user gets planning-grade plans, architecture, and code generation,
while a Pro-plan user gets execution-grade output — proportional to their purchasing
decision. Do NOT add `model: opus` to these agents. Doing so overrides budget-adaptive
behavior and forces planning-grade API charges regardless of the user's account tier (see Common
Mistakes).

### Execution-Grade

**When to use**: Rule-based validation, applying validated fixes from audit reports, template-driven output, and structured pattern-following tasks.

**Cognitive profile**: Strong pattern recognition, reliable rule application, structured output generation, systematic validation against defined criteria.

**Task characteristics**:

- Validating content against a defined checklist or ruleset
- Applying fixes identified by a prior audit (checker output drives fixer input)
- Generating output from templates with variable substitution
- Following a documented procedure step-by-step
- Tasks where correctness means conforming to explicit rules, not inventing solutions

**Agent examples**:

- **All checkers** -- validate content against conventions using defined rulesets and produce structured audit reports (docs-checker, docs-tutorial-checker, docs-software-engineering-separation-checker, readme-checker, specs-checker, repo-rules-checker, repo-workflow-checker, plan-checker, plan-execution-checker, swe-code-checker, swe-ui-checker, ci-checker, apps-\*-checker)
- **Most fixers** -- apply corrections from checker audit reports following documented fix procedures (docs-fixer, docs-tutorial-fixer, docs-software-engineering-separation-fixer, readme-fixer, specs-fixer, repo-rules-fixer, repo-workflow-fixer, plan-fixer, swe-ui-fixer, ci-fixer, apps-\*-fixer)
- **social-linkedin-post-maker** -- generates social media posts following a defined template and tone guidelines
- **Structured makers** -- makers with tight, well-defined skills that pin down most decisions, making them rule-following rather than open-ended creation (docs-maker, readme-maker, agent-maker, specs-maker, repo-workflow-maker, apps-ose-www-content-maker, apps-ayokoding-www-by-example-maker, apps-ayokoding-www-general-maker, apps-ayokoding-www-in-the-field-maker, repo-rules-maker)
- **swe-e2e-dev** -- writes Playwright E2E tests following a dedicated skill with defined patterns (locators, fixtures, waits); lower stakes than production code written by language developer agents

**Frontmatter**: Specify `model: sonnet` explicitly.

```yaml
---
name: docs-checker
description: Expert documentation validator...
tools: [Read, Glob, Grep, Write, Bash]
model: sonnet
color: green
---
```

### Fast

**When to use**: Purely mechanical tasks with no reasoning required -- simple automation, URL validation, deployment scripts, and straightforward command execution.

**Cognitive profile**: Fast execution of simple, well-defined operations. No analytical reasoning needed. Input-output mapping is deterministic or near-deterministic.

**Task characteristics**:

- Running predefined shell commands in sequence
- Validating URLs against HTTP status codes
- Executing deployment scripts with known parameters
- Simple file existence or format checks
- Tasks where the entire procedure is a fixed script with no branching logic

**Agent examples**:

- **Deployers** (apps-ayokoding-www-deployer, apps-ose-www-deployer, apps-organiclever-app-web-deployer, apps-wahidyankf-www-deployer) -- execute git branch operations and deployment commands following a fixed procedure
- **Link checkers** (docs-link-checker, apps-ayokoding-www-link-checker) -- validate URLs by checking HTTP status codes and managing cache files
- **apps-ayokoding-www-link-fixer** -- applies checker-identified broken links via deterministic URL replacement; no independent analysis required
- **docs-file-manager** -- performs deterministic file operations (move, rename, delete) with `git mv`, kebab-case pattern matching, and mechanical link updates; no judgment calls required

**Frontmatter**: Specify `model: haiku` explicitly.

```yaml
---
name: apps-ayokoding-www-deployer
description: Expert deployment orchestrator...
tools: [Bash, Read, Glob, Grep]
model: haiku
color: purple
---
```

## Model Selection Decision Tree

```
Start: Choosing Agent Model
    |
    +-- Does the task require creative reasoning, code generation,
    |   architectural decisions, or nuanced content creation?
    |   |
    |   +-- Yes --> Opus (omit model field)
    |   |
    |   +-- No --> Does the task require applying rules, validating
    |              against checklists, or following structured procedures?
    |              |
    |              +-- Yes --> Sonnet (model: sonnet)
    |              |
    |              +-- No --> Is the task purely mechanical with
    |                         no reasoning required?
    |                         |
    |                         +-- Yes --> Haiku (model: haiku)
    |                         |
    |                         +-- No --> Default to Sonnet
    |                                    (safer than haiku for
    |                                     ambiguous cases)
```

## Justification Requirement

Every agent MUST include a **Model Selection Justification** block in its markdown body explaining why the chosen tier is appropriate. This block appears near the top of the agent file, after the frontmatter metadata section.

**Format**:

```markdown
**Model Selection Justification**: This agent uses `model: sonnet` because it requires:

- [Capability 1] to [accomplish task aspect]
- [Capability 2] to [accomplish task aspect]
```

**Examples**:

For a checker agent:

> **Model Selection Justification**: This agent uses `model: sonnet` because it requires:
>
> - Systematic rule application to validate content against defined checklists
> - Structured report generation following the audit report template
> - Pattern recognition to identify convention violations across files

For a developer agent (omit model field — inherits opus):

> **Model Selection Justification**: This agent uses inherited `model: opus` (omit model field) because it requires:
>
> - Advanced reasoning to generate idiomatic code across language paradigms
> - Multi-step problem decomposition for complex refactoring tasks
> - Creative synthesis to design APIs and data models

For a deployer agent:

> **Model Selection Justification**: This agent uses `model: haiku` because it requires:
>
> - Execution of predefined git and deployment commands
> - No analytical reasoning beyond following a fixed procedure

## Tier Comparison Summary

| Dimension              | Planning-Grade (inherit)                                                                    | Execution-Grade                                                                               | Fast                                                                                         |
| ---------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Reasoning depth**    | Deep, multi-step                                                                            | Moderate, rule-based                                                                          | Minimal, mechanical                                                                          |
| **Creativity**         | High (novel solutions)                                                                      | Low (follows templates)                                                                       | None (fixed procedures)                                                                      |
| **Task ambiguity**     | Handles open-ended problems                                                                 | Handles structured problems                                                                   | Requires deterministic flow                                                                  |
| **Output originality** | Creates new content/code                                                                    | Transforms per rules                                                                          | Executes predefined steps                                                                    |
| **Error recovery**     | Adapts to unexpected states                                                                 | Follows fallback rules                                                                        | Fails or retries                                                                             |
| **Typical agents**     | Creative makers, developers                                                                 | Checkers, fixers, structured makers                                                           | Deployers, link checkers, file manager                                                       |
| **SWE-bench Verified** | [87.6%](../../../docs/reference/ai-model-benchmarks.md#claude-opus-47) (Verified, Apr 2026) | [79.6%](../../../docs/reference/ai-model-benchmarks.md#claude-sonnet-46) (Verified, Feb 2026) | [73.3%](../../../docs/reference/ai-model-benchmarks.md#claude-haiku-45) (Verified, Oct 2025) |

## Common Mistakes

| Mistake                                           | Problem                                                                          | Correction                                                          |
| ------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Using opus for validation tasks                   | Wastes resources; opus may over-interpret instead of checking                    | Use execution-grade tier for checkers and fixers                    |
| Using fast tier for content creation              | Fast tier lacks reasoning depth for original content                             | Use planning-grade (inherit) for makers and developers              |
| Using execution-grade tier for deployment scripts | Execution-grade tier is overqualified for deterministic command sequences        | Use fast tier for deployers and link checkers                       |
| Omitting model justification                      | Future maintainers cannot assess whether the tier is appropriate                 | Always include Model Selection Justification block                  |
| Defaulting to planning-grade "just in case"       | Violates Simplicity Over Complexity principle                                    | Analyze task requirements; use the simplest adequate tier           |
| Using fast tier for tasks with error handling     | Fast tier cannot reason about unexpected states                                  | Use execution-grade or planning-grade depending on error complexity |
| Adding `model: opus` to planning-grade agents     | Bypasses budget-adaptive inheritance; forces planning-grade API charges on users | Omit the field — inherit session model to match user's tier         |

## Current Model Versions (April 2026)

| Agent config alias | Model ID                    | Context     | Notes                 | Benchmark                                                                     |
| ------------------ | --------------------------- | ----------- | --------------------- | ----------------------------------------------------------------------------- |
| `opus` (inherit)   | `claude-opus-4-7`           | 1M tokens   | Current top tier      | [Benchmarks](../../../docs/reference/ai-model-benchmarks.md#claude-opus-47)   |
| `sonnet`           | `claude-sonnet-4-6`         | 1M tokens   | Daily driver          | [Benchmarks](../../../docs/reference/ai-model-benchmarks.md#claude-sonnet-46) |
| `haiku`            | `claude-haiku-4-5-20251001` | 200k tokens | v3 retired 2026-04-19 | [Benchmarks](../../../docs/reference/ai-model-benchmarks.md#claude-haiku-45)  |

Aliases (`opus`, `sonnet`, `haiku`) automatically track future model versions within each
tier. The model IDs above are current as of April 2026.

## Platform Binding Examples

Agents in the primary binding directory are auto-synced to the secondary binding directory by rhino-cli
(`npm run generate:bindings`). The sync translates primary binding model aliases to
secondary binding model IDs.

### Model ID Mapping

| Primary binding                                  | Secondary binding         | Capability notes                                                                   |
| ------------------------------------------------ | ------------------------- | ---------------------------------------------------------------------------------- |
| `model: opus` (thinking-grade)                   | `zai-coding-plan/glm-5.2` | Zhipu GLM via GLM Coding Plan primary provider; all tiers map to the same model ID |
| omit (execution-grade inherit) / `model: sonnet` | `zai-coding-plan/glm-5.2` | Same model as thinking-grade (intentional full-tier collapse)                      |
| `model: haiku` (fast)                            | `zai-coding-plan/glm-5.2` | Fast tier also collapses onto glm-5.2 via the primary provider                     |

### Tier Collapse

The primary binding has three tiers (planning-grade/thinking > execution-grade > fast). The secondary
binding's `convert_model()` maps all three tiers to `zai-coding-plan/glm-5.2` via the GLM Coding Plan
primary provider. The `opencode-go` provider remains configured in `.opencode/opencode.json` for
`/models` roster access but is not used in agent tier mapping.

Tier assignments govern behavior in primary binding sessions (the primary runtime, where `opus`
genuinely resolves to a stronger model than `sonnet`). The secondary binding collapses every tier
onto the same GLM Coding Plan model.

### Why glm-5.2 as the Default

`zai-coding-plan/glm-5.2` is the GLM Coding Plan primary provider model for all agent tiers.
The `opencode-go` provider remains available for `/models` roster access. If the primary provider
or model changes, update `convert_model()` in `apps/rhino-cli/src/application/agents/converter.rs`
and re-run `npm run generate:bindings`.

### Model ID Mapping (Claude Code → Cursor)

| Primary binding                                  | Cursor binding | Capability notes                                                    |
| ------------------------------------------------ | -------------- | ------------------------------------------------------------------- |
| `model: opus` (thinking-grade)                   | `composer-2.5` | Full tier collapse — thinking collapses onto execution              |
| omit (execution-grade inherit) / `model: sonnet` | `composer-2.5` | Same pin as thinking-grade (intentional full-tier collapse)         |
| `model: haiku` (fast)                            | `composer-2.5` | Fast tier also collapses — avoids the 6× `composer-2.5-fast` toggle |

**Prohibition**: `rhino-cli` must never emit `composer-2.5-fast` into `.cursor/agents/`. That slug
is the priced-fast inference toggle this binding exists to avoid.

### Cursor Full-Tier Collapse

Every non-fast Claude alias resolves to `composer-2.5`. Unlike OpenCode (where fast maps to a
lighter model), Cursor's fast toggle is a latency/price choice on identical weights — so haiku-grade
agents trade hypothetical input-cost savings for deterministic first-party pinning off the fast tier.

## Special Considerations

### Borderline Cases

Some agents straddle tier boundaries. When uncertain:

1. **Analyze the core loop** -- what does the agent do repeatedly? If the core loop is rule application, use execution-grade even if setup requires some reasoning.
2. **Consider the failure mode** -- if the agent picks a wrong approach, how bad is the outcome? Higher-stakes failures justify a higher tier.
3. **Start lower, promote if needed** -- begin with execution-grade; promote to planning-grade only if quality issues emerge in practice.

### Link Checkers as Fast-Tier

Link checker agents (docs-link-checker, apps-ayokoding-www-link-checker) use the fast tier despite being categorized as checkers (green). This is because their validation is purely mechanical (HTTP status code checking), not rule-based reasoning. The checker color reflects their role in the maker-checker-fixer workflow, while the model reflects their cognitive requirements.

### Social Media Maker as Execution-Grade

The social-linkedin-post-maker uses execution-grade despite being a "maker" agent. This is because LinkedIn post generation follows a rigid template and tone guide, making it a structured pattern-following task rather than creative content creation.

### Structured Makers as Execution-Grade

Several maker agents use execution-grade because their output is structured by tight skills with well-defined rubrics (docs-maker, readme-maker, agent-maker, specs-maker, repo-workflow-maker, apps-ose-www-content-maker, apps-ayokoding-www-by-example-maker, apps-ayokoding-www-general-maker, apps-ayokoding-www-in-the-field-maker, repo-rules-maker). Each has an execution-grade checker and execution-grade fixer in its maker-checker-fixer trio, and the skill pins down most decisions. Contrast with planning-grade makers (plan-maker, docs-tutorial-maker, swe-ui-maker) where the creative work is open-ended, pedagogically demanding, or multi-concern.

### E2E Test Developer as Execution-Grade

The swe-e2e-dev uses execution-grade despite the other 12 language developer agents being planning-grade. Playwright E2E tests are pattern-driven (locators, fixtures, waits) with a dedicated skill, and test code regressions surface fast in CI. Production application code written by the language developers has higher stakes and unforgiving idioms, justifying their continued planning-grade tier.

### File Manager as Fast-Tier

The docs-file-manager uses the fast tier despite being categorized as a fixer (yellow). This is because its operations are deterministic file manipulation (`git mv`, `git rm`, find-and-replace link updates) with no judgment calls. The `agent-developing-agents` skill cites it as the canonical fast-tier example.

### Link Fixer as Fast-Tier

The apps-ayokoding-www-link-fixer uses the fast tier despite being a fixer (yellow) — previously execution-grade. Its work is deterministic URL replacement driven entirely by a checker audit report: no independent link analysis, no content reasoning, just old-URL → new-URL substitution followed by an HTTP status re-check. The fast-tier model (73.3% SWE-bench Verified — [benchmark reference](../../../docs/reference/ai-model-benchmarks.md#claude-haiku-45)) is fully sufficient and costs 5× less per token than the execution-grade tier. This is the fixer analogue of the Link Checkers as Fast-Tier rule above.

## Tools and Automation

The following agents enforce or assist with model selection:

- **agent-maker** -- applies these guidelines when creating new agents
- **repo-rules-checker** -- validates that all agents have model justification blocks and appropriate tier assignments
- **repo-rules-fixer** -- corrects model selection issues identified by the checker

## References

**Related Development Practices:**

- [AI Agents Convention](./ai-agents.md) -- Complete agent standards including frontmatter, naming, and tool permissions
- [Best Practices](./best-practices.md) -- Recommended agent development patterns
- [Anti-Patterns](./anti-patterns.md) -- Common agent development mistakes

**Related Principles:**

- [Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md) -- Use the simplest model that works
- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) -- Justify model selection transparently
- [Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md) -- Analyze task requirements before selecting

**Related Conventions:**

- [Content Quality Principles](../../conventions/writing/quality.md) -- Quality standards for justification text

**Agents:**

- `agent-maker` -- Creates agents following these model selection standards
- `repo-rules-checker` -- Validates model selection compliance
- `repo-rules-fixer` -- Fixes model selection issues
