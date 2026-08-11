---
title: "Grilling-With-Options Convention"
description: >
  Agents and workflows MUST resolve open design decisions using structured multiple-choice
  questions, not open-ended prose prompts. Every grilling question presents 2-4 concrete
  options, each with its trade-off, and exactly one option marked Recommended. Every question
  also always carries two standing options — a free-form blank-state write-in and a "chat about
  this" path — so the user is never boxed into a listed choice. Applies to
  all agent and workflow contexts: plan creation, design review, stress-testing, and
  requirements clarification.
category: explanation
subcategory: development
tags:
  - planning
  - grill-me
  - user-interaction
  - plan-maker
  - design-decisions
  - interaction
  - agents
created: 2026-05-26
---

# Grilling-With-Options Convention

When an agent or workflow must resolve open design decisions with the user — during plan
creation, design review, stress-testing, or requirements clarification — it MUST present
structured multiple-choice questions, not open-ended prose prompts. This convention defines
the required format, mechanism, and scope for all such interactions.

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**:
  Structured options force the agent to understand the design space before asking, and force
  the user to choose deliberately rather than free-associate. Reversible design branches are
  made explicit so users can reason about them.
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  Each option names its trade-off. The Recommended option names its rationale. Nothing is
  left to the user's imagination or to silent agent inference.
- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: A
  bounded list of options reduces cognitive load. The user selects from prepared choices
  rather than having to generate an answer from scratch.
- **[Progressive Disclosure](../../principles/content/progressive-disclosure.md)**: Options
  start simple (2-3 choices covering 90% of cases) and expose complexity only when the
  user's prior answer opens a new branch. Unrelated decisions never appear in the same
  question.
- **[Accessibility First](../../principles/content/accessibility-first.md)**: Users are never
  locked into a predefined set — the free-form "Other / write-in" path is always available.
  Questions are self-contained so screen-reader users and harness users without rich
  rendering experience the same choice surface.

## Conventions Implemented/Respected

- **[Convention Writing Convention](../../conventions/writing/conventions.md)**: This document
  follows the standard Purpose / Standards / Examples / Validation structure.
- **[Plans Organization Convention](../../conventions/structure/plans.md)**: This convention
  serves the plan creation lifecycle described there — grilling is the first gate before any
  plan files are written.
- **[Governance Vendor-Independence Convention](../../conventions/structure/governance-vendor-independence.md)**:
  All vendor-specific tool names are confined to the Platform Binding Examples section.
- **[Linking Convention](../../conventions/formatting/linking.md)**: All cross-references use
  GitHub-compatible markdown with `.md` extensions.
- **[Content Quality Principles](../../conventions/writing/quality.md)**: Active voice, single
  H1, proper heading nesting.

## Purpose

Open-ended questions ("What approach do you want?") produce vague answers, require follow-up
clarification, and shift cognitive burden from the agent to the user. Structured
multiple-choice grilling resolves this by:

1. Requiring the agent to explore the repo and enumerate concrete options before asking.
2. Giving the user a small, well-defined decision surface rather than a blank canvas.
3. Making trade-offs explicit so decisions are reversible and auditable in the plan.
4. Using the harness's native interactive tool when available, so options are rendered as
   selectable choices rather than prose the user must parse.

## Scope

### What This Convention Covers

- All grilling interactions during plan creation (pre-write and post-write grill sessions).
- All grilling steps in the plan establishment workflow (Steps 1 and 3).
- Pre-execution grilling of unresolved design decisions before plan execution begins.
- Any "grill me" design-review or stress-testing session invoked explicitly by the user.
- The interaction format, option structure, Recommended marking, and mechanism (native tool
  vs. markdown fallback).

### What This Convention Does Not Cover

- The content of individual grilling questions (domain-specific; defined by the agent or
  workflow that invokes the grill).
- Plan document structure (see
  [Plans Organization Convention](../../conventions/structure/plans.md)).
- Agent file structure and frontmatter (see
  [AI Agents Convention](../agents/ai-agents.md)).
- Commit message format for decisions captured in plans (see
  [Commit Message Convention](./commit-messages.md)).

## Standards

### Rule 1 — Explore Before Asking

Before composing any grilling question, the agent MUST read the relevant repo artifacts. If
the answer to a potential question already exists in a convention file, a plan, or the
codebase, the agent MUST use that information directly and MUST NOT ask the user a question
that a file read could answer.

**Rationale**: Every unnecessary question erodes trust and wastes context. The repo is the
ground truth; the user is the tiebreaker for genuinely ambiguous decisions.

### Rule 2 — Structured Options (2-4, Mutually Exclusive)

Every grilling question MUST present between 2 and 4 concrete, mutually exclusive substantive
options. The options MUST collectively cover the realistic decision space. Beyond those
substantive options, every question ALSO carries two standing options — a free-form blank-state
write-in and a "chat about this" path (see Rule 8). The two standing options do NOT count
against the 2-4 substantive cap, and the blank-state write-in MUST be surfaced explicitly,
never left merely implicit.

**Rationale**: Fewer than 2 options is a binary yes/no (use a confirmation prompt instead,
not a grill). More than 4 options overwhelms the user and signals the agent has not pruned
the decision space sufficiently.

### Rule 3 — Trade-Off Per Option

Each option MUST state its implication or trade-off in one sentence. The trade-off must be
specific to this decision context, not generic filler ("Option A is simpler").

**Good trade-off**: "Adds a new `development/workflow/grilling-with-options.md` convention
— layer-coherent and matches adjacent workflow docs, but requires updating the development/
README."

**Bad trade-off**: "This option is simpler." (non-specific, not actionable)

### Rule 4 — Exactly One Recommended Option

Exactly one option MUST be marked as Recommended with a one-line rationale grounded in the
specific context (repo state, existing conventions, the user's stated constraints). Marking
more than one option Recommended is forbidden — if two options are genuinely equal, the
agent must choose one based on context.

**Rationale**: An agent that refuses to recommend abdicates its expertise. Users engage with
AI agents precisely to get a grounded recommendation, not just a menu.

### Rule 5 — One Decision Per Question; Batch Only Tightly Coupled Decisions

Each grilling question MUST resolve exactly one decision branch. Tightly coupled decisions
(where the answer to one necessarily constrains the other) MAY be batched in a single
multi-question prompt. Unrelated decisions MUST NOT be bundled — present them as separate
questions, in the same grill session if needed.

**What counts as tightly coupled**: "Which layer should the convention live in?" and "What
filename should it use?" are tightly coupled (the filename depends on the layer choice).
These may appear together.

**What counts as unrelated**: "Which layer?" and "Should we update the README?" are
independent. Present them separately.

### Rule 6 — Mechanism: Native Interactive Tool First, Markdown Fallback

When the interactive root thread provides a native multiple-choice question tool, grilling MUST
use it. The native tool renders options as selectable UI elements and returns the user's choice as
structured data, eliminating parse ambiguity.

#### User Decisions Required Envelope

A subagent MUST NOT render markdown as if it were asking the user. It returns this exact envelope to
the root orchestrator and stops before work that depends on the answer:

````markdown
## User Decisions Required

```yaml
decisions:
  - id: stable_snake_case_id
    question: One self-contained decision prompt
    recommended:
      option_id: recommended_option_id
      rationale: One context-grounded recommendation rationale
    options:
      - id: recommended_option_id
        label: Recommended option label
        tradeoff: One decision-specific trade-off
      - id: alternative_option_id
        label: Alternative option label
        tradeoff: One decision-specific trade-off
```
````

The stable `id` identifies the decision across reinvocation. `options` exhaustively lists every
substantive leaf with its trade-off; the root adds the standing chat option and relies on the
client's implicit custom answer. After the envelope, the specialist stops. The root presents the
decision through its native UI, then resumes or reinvokes the specialist with the resolved answer.
Direct custom-agent callers receive the same envelope.

#### Resolved User Decisions Envelope

After rendering an outbound envelope, the root MUST return this versioned, harness-neutral payload
to the specialist **verbatim**. It is the only inbound representation of a resolved decision:

````markdown
## Resolved User Decisions

```yaml
schema_version: 1
decisions:
  - id: stable_snake_case_id
    answer:
      kind: selected_option
      option_id: original_option_id
  - id: another_stable_snake_case_id
    answer:
      kind: custom_answer
      value: Exact user-supplied answer
```
````

`id` MUST be the original decision ID from `## User Decisions Required`. A `selected_option`
answer MUST name the original leaf ID in `option_id`, including when staged rendering reaches that
leaf through a branch group. A `custom_answer` MUST preserve the user's answer in `value`; the root
MUST NOT recast a write-in as a selected option because its text resembles an option label. These
two discriminated forms make listed selections and user-authored answers unambiguous across every
harness.

Before performing work that depends on an answer, the receiving specialist MUST validate that the
payload has `schema_version: 1`, contains each requested decision ID exactly once and no unknown ID,
uses a known original leaf ID for every `selected_option`, and carries a non-empty `value` for every
`custom_answer`. On failure, it MUST stop and request a corrected resolved-decision payload; it
MUST NOT infer, normalize, or silently repair an answer. The root constructs this payload only after
rendering is complete and passes it unchanged on every resume or reinvocation.

#### Staged Native Rendering

When a native tool can display only 2–3 substantive options while a decision envelope contains
3–4 substantive leaves, the root MUST render a complete staged decision tree rather than trimming
the envelope. This procedure applies to Claude, Codex, and every other native tool with that
effective limit:

1. Retain every original leaf, its stable ID, trade-off, and the one recommendation in the envelope.
2. Partition the leaves into two named branch groups: one leaf versus the remaining two for three
   leaves, or two leaves versus two leaves for four. Each root-stage label and description MUST name
   every leaf it contains; a grouped branch is navigation, never a collapsed or selected outcome.
3. Render the two branch groups plus **"Let's chat about this"**. The tool-provided free-form
   **"Other"** entry remains the type-your-own blank state. The root-stage recommendation identifies
   the recommended branch and gives its context-grounded rationale.
4. After the user selects a group containing multiple original leaves, render those leaves as the
   next single-choice question, again with chat and type available and exactly one context-grounded
   recommendation. If the selected group contains one original leaf, it is terminal: record that
   original leaf ID immediately and do not pose a singleton follow-up. Continue staging only when a
   selected group has multiple leaves; a write-in that creates a new branch follows Rule 7 before
   continuing.
5. Record the final original leaf ID through the `selected_option` form in the Resolved User
   Decisions Envelope. Every original leaf MUST remain reachable exactly once; the root MUST NOT
   omit, silently collapse, auto-select, or reinterpret any leaf to fit a native tool's limit.

The staged UI is a rendering of the exhaustive envelope, not a weaker substitute for it. Chat and
the blank-state type path are required at every rendered stage, and the resulting final leaf remains
subject to the envelope's one-decision, trade-off, and recommendation requirements. Every staged
root renders two branch groups plus Chat at the first stage, and two leaves plus Chat at a multi-leaf
follow-up; its platform binding defines any additional native-tool constraints.

Only a genuinely non-interactive root or harness without a native tool falls back to inline
markdown options emitted to its caller in the following format:

```markdown
**Question**: [Decision to resolve]

- **Option 1 — [Label]**: [Trade-off sentence] _(Recommended — [rationale])_
- **Option 2 — [Label]**: [Trade-off sentence]
- **Option 3 — [Label]**: [Trade-off sentence]
- **Other — type your own answer**: Free-form write-in; the answer is whatever you type (blank
  state). Always present.
- **Chat about this**: Talk the decision through before deciding instead of picking now. Always
  present.
```

The markdown fallback MUST still satisfy Rules 2–5 (2-4 options, trade-offs, one Recommended,
one decision per question).

### Rule 7 — User Can Always Supply an Unlisted Answer

Options are a structured starting point, not a closed cage. The agent MUST treat a user's
write-in answer with the same weight as a listed option. If the write-in answer opens a new
decision branch, the agent grills on that branch before proceeding.

### Rule 8 — Two Standing Options Always Present: Type (Blank State) and Chat

Beyond its 2-4 substantive options, every grilling question MUST ALWAYS surface two standing
options, on every question, regardless of rendering mechanism:

1. **Type (blank state)** — an explicit free-form write-in path whose answer depends entirely
   on what the user types. This is NOT optional and NOT merely implicit: it MUST be visible on
   every question. When a native tool auto-provides a free-text "Other" entry, that entry
   satisfies this requirement; with the markdown fallback, an explicit
   `**Other — type your own answer**` bullet MUST be listed.
2. **Chat about this** — an explicit option signalling the user wants to discuss the decision
   conversationally before committing, rather than pick a listed option or write a final
   answer. When the user selects it, the agent drops the structured options, talks the branch
   through in prose, then returns to a structured question once the user is ready to decide.

These two standing options do NOT count against the 2-4 substantive cap; they are universal
escape hatches present on every question, not decision branches.

**Rationale**: Structured options accelerate the common path, but a user must never be boxed
in. The blank-state type guarantees the user can always answer in their own words; the chat
option guarantees they can always reopen the decision for discussion. Dropping either —
especially the blank-state type, the single most common omission — turns a grill into a forced
choice.

## When This Convention Applies

Grilling MUST follow this convention in all of the following contexts:

| Context                                | Trigger                                                         |
| -------------------------------------- | --------------------------------------------------------------- |
| **plan-maker pre-write grill**         | Before writing any plan — resolve macro design decisions        |
| **plan-maker post-write grill**        | After writing the plan — validate and stress-test decisions     |
| **plan-planning Step 1**               | First grill: scope, constraints, push target                    |
| **plan-planning Step 3**               | Second grill: post-research validation                          |
| **plan-execution pre-execution grill** | Unresolved design decisions in the plan before execution begins |
| **"Grill me" design review**           | Any explicit "grill me" invocation by the user                  |

## Examples

### PASS: Well-formed grilling question (markdown fallback)

```markdown
**Question**: Where should the new convention live?

- **Option 1 — `development/workflow/grilling-with-options.md`**: Layer-coherent (HOW we
  interact during development); matches adjacent workflow docs; requires updating
  `development/README.md`. _(Recommended — grilling is an interaction workflow, not a
  documentation-writing rule; the conventions/ README explicitly scopes that directory to
  documentation standards)_
- **Option 2 — `conventions/writing/grilling-with-options.md`**: Co-located with other
  writing conventions; simpler path for writers who look in conventions/ first; but fails
  the layer-coherence test because conventions/ is scoped to documentation rules, not
  development workflows.
- **Option 3 — `development/agents/grilling-with-options.md`**: Groups with AI agent
  standards; appropriate if grilling is agent-only; but grilling also applies to
  human-facing orchestration steps, so agents/ is too narrow.
- **Other**: Specify a different path.
```

### PASS: Interactive multiple-choice tool (preferred when available)

When the coding agent supports interactive selection (e.g., via an `AskUserQuestion`-style
tool), use it with 2-4 `options` entries. The platform renders the choices as a single-click
selection UI and always includes a free-form "Other" path.

### FAIL: Open-ended prose question

```markdown
What approach do you want for the grilling convention?
```

**Problems**: No options, no trade-offs, no Recommended, no structure. Shifts cognitive
burden entirely to the user.

### FAIL: Too many options (more than 4)

```markdown
**Question**: Which layer?

- Option 1 — conventions/writing/
- Option 2 — conventions/structure/
- Option 3 — development/workflow/
- Option 4 — development/agents/
- Option 5 — development/pattern/
- Option 6 — development/quality/
```

**Problem**: Six options signals the agent has not pruned the decision space. Maximum is 4.
Narrow the options first by exploring the repo and applying the layer-coherence test, then
ask.

### FAIL: Trade-offs are non-specific filler

```markdown
- **Option 1**: This is the simpler approach.
- **Option 2**: This is the more flexible approach.
```

**Problem**: "Simpler" and "more flexible" are meaningless without context. Each trade-off
must name the specific structural, maintenance, or governance implication for this decision.

### FAIL: Two options marked Recommended

```markdown
- **Option 1**: … _(Recommended)_
- **Option 2**: … _(Also Recommended)_
```

**Problem**: Exactly one option may be Recommended. If options are genuinely equal, the
agent must choose one and state why.

### FAIL: Unrelated decisions bundled

```markdown
**Question**: Which layer? And also, should we update the README? And what filename?
```

**Problem**: Three independent decisions bundled into one prompt. Present "Which layer?" and
"What filename?" together (tightly coupled). Present "Should we update the README?"
separately.

## Validation

A grill question is valid when ALL of the following hold:

- [ ] It presents exactly 2-4 concrete options
- [ ] Each option has a trade-off description (even a brief one)
- [ ] One option is marked **(Recommended)**
- [ ] The question addresses exactly one decision
- [ ] Options are grounded in codebase reality (not invented)
- [ ] An interactive multiple-choice tool is used when the coding agent supports it
- [ ] A free-form blank-state "type your own answer" option is surfaced explicitly (never
      implicit-only)
- [ ] A "chat about this" option is offered

A grill question is invalid when ANY of the following hold:

- No options are presented (open-ended)
- Only one option is presented (not a real choice)
- More than four substantive options are presented (too many; simplify)
- Options are not grounded in codebase reality
- Multiple decisions are bundled into one question
- The blank-state "type your own answer" option is missing or only implicit
- No "chat about this" option is offered

## Special Considerations

### Grilling Within plan-maker

When `plan-maker` is invoked by `plan-planning`, the macro design decisions
are already resolved by Steps 1 and 3 of that workflow. The `plan-maker` grilling sessions
in that context become root-orchestrated **validation passes** for micro-decisions (exact Gherkin
phrasing, section ordering, step granularity). The specialist returns `## User Decisions Required`
and stops; the root resolves it and resumes or reinvokes the specialist. The structured format
(Rules 2–5) still applies, but questions are narrower.

Standalone plan-maker triggers still require full pre-write and post-write grill sessions, but the
calling root orchestrates them. A directly invoked specialist returns the envelope; it never renders
the native UI itself.

### Grilling Is a Process Artifact, Not a Document Artifact

Grilling produces answers that are captured in plan documents (resolved decisions in
`tech-docs.md`, design-decision lists in the plan-establishment handoff). The grill session
itself does not produce a standalone artifact. Compliance with this convention is verified
primarily by checking that plan-creation workflows and agent definitions reference it — not
by inspecting a generated file.

`repo-rules-checker`'s general cross-reference and consistency validation flags a
plan-creation touchpoint that drops its reference to this convention. The touchpoints
expected to reference this convention are:

- The plan-establishment workflow's Step 1 and Step 3 sections.
- The plan-execution workflow's pre-execution grill section.
- The Plans Organization Convention, where design-decision resolution is discussed.
- The development/README.md index.
- The `plan-maker` agent (pre-write grill step and post-write grill step).
- The `grill-me` skill (canonical implementation of this convention's rules).
- The `plan-creating-project-plans` skill (pre-write and post-write grill gates in the plan
  lifecycle).

## Tools and Automation

- **`grill-me` skill** — The canonical implementation of this convention. The
  [grill-me Skill](../../../.claude/skills/grill-me/SKILL.md) provides the grilling
  service used by `plan-planning` and `plan-maker`. This convention governs
  the format and mechanism that `grill-me` MUST use. Platform-specific tool invocations
  live in the Platform Binding Examples section below.
- **`repo-rules-checker`** — Its general cross-reference/consistency validation flags a
  plan-creation touchpoint that has dropped its reference to this convention.
- **`repo-rules-fixer`** — Restores missing convention references to touchpoint files when
  flagged.

## Platform Binding Examples

The content under this heading is intentionally vendor-specific. Per the
[Governance Vendor-Independence Convention](../../conventions/structure/governance-vendor-independence.md),
the vendor-audit scanner skips every line under this heading until the next same-level
heading or end of file.

### Primary Coding Harness — Claude Code

Claude Code exposes `AskUserQuestion` as its native interactive multiple-choice tool. When
grilling inside an interactive Claude Code root session, the `grill-me` skill MUST invoke
`AskUserQuestion`
with:

- `questions`: 1–4 questions (one per tightly-coupled decision cluster)
- `header` per question: a short label of at most 12 characters
- `question` per question: one self-contained decision prompt
- `options` per question: 2–3 substantive `{ label, description }` option objects plus the standing
  `"Let's chat about this"` option (3–4 total)
- `multiSelect` per question: `false`
- The harness's auto-provided free-text `"Other"` entry is the blank-state type option — the
  answer is whatever the user writes; it is always present and satisfies the Rule 8 blank-state
  requirement

`AskUserQuestion` returns a structured response the agent uses directly without parsing
free-text. A delegated agent returns unresolved decisions to the root and stops; only a genuinely
non-interactive root without `AskUserQuestion` emits the markdown fallback to its caller.
For a 3–4-leaf envelope, the root follows [Staged Native Rendering](#staged-native-rendering).

Example invocation shape:

```binding-example
AskUserQuestion({
  questions: [
    {
      header: "Plan scope",
      question: "Where should the new convention live?",
      options: [
        {
          label: "Development workflow (Recommended)",
          description: "Layer-coherent and matches adjacent workflow documentation."
        },
        {
          label: "Writing convention",
          description: "Co-locates writing rules but conflicts with the documentation-only layer."
        },
        {
          label: "Let's chat about this",
          description: "Discuss the placement before selecting an option."
        }
      ],
      multiSelect: false
      // The harness auto-appends a free-text "Other" entry — that is the blank-state type
      // option (answer = whatever the user writes), always present per Rule 8.
    }
  ]
})
```

### Secondary Harness — OpenCode

OpenCode provides the `question` tool. When running in an interactive OpenCode root session, use
`question` with 2-4 substantive options plus the standing `"Let's chat about this"` option per
question. The client-provided custom answer remains implicit. If `question` is unavailable in the
current OpenCode version, fall back to the markdown option format defined in Rule 6.

### OpenAI Codex

Codex exposes `request_user_input` to the interactive root thread when the repository enables
`[features].default_mode_request_user_input = true` in `.codex/config.toml`. Codex currently marks
this feature as under development and keeps it off by default, so the repository-level opt-in is
required.

The root orchestrator MUST own every grill and invoke `request_user_input` directly. After the user
resolves the questions, it constructs and passes the canonical Resolved User Decisions Envelope
verbatim to any delegated `plan-maker` or `plan-fixer`; it MUST NOT delegate the user interaction
itself.

One `request_user_input` call carries 1–3 tightly coupled question objects. Each object MUST use:

- `header`: a short label of at most 12 characters
- `id`: a stable `snake_case` identifier
- `question`: one self-contained decision prompt
- `options`: 2–3 option objects total; Rule 2's two-substantive-option minimum plus the standing
  **"Let's chat about this"** option means a grill uses exactly 3

Put the Recommended option first and suffix its label with `(Recommended)`. Every option object has
a 1–5 word `label`, including that suffix, and a one-sentence trade-off in `description`. Do not add
an `Other` option because the client supplies the free-form entry. Each question accepts one answer
only; never request or simulate multi-select.

For a 3–4-leaf envelope, the root follows [Staged Native Rendering](#staged-native-rendering): the
first stage has two branch groups plus Chat, and a multi-leaf follow-up has two original leaves plus
Chat. A selected singleton group is terminal and records its original leaf ID without a follow-up
prompt.

A non-root subagent returns `## User Decisions Required` to the root and stops; it MUST NOT render a
user prompt or select an answer. The root asks through `request_user_input`, then resumes or
reinvokes the delegated agent with the resolved answers. A non-interactive root, including
`codex exec`, emits the Rule 6 markdown fallback to its caller.

### All Other Harnesses

A genuinely non-interactive root or harness without a native interactive multiple-choice tool emits
the inline markdown format defined in Rule 6 to its caller. A subagent returns unresolved decisions
to the root and stops. A native tool with a 2–3-substantive-option limit follows
[Staged Native Rendering](#staged-native-rendering). The structured format requirements (Rules 2–5)
are identical regardless of rendering mechanism.

## Related Documentation

- **[grill-me Skill](../../../.claude/skills/grill-me/SKILL.md)** — The canonical
  implementation of this convention; its HARD RULES reflect the standards defined here
- **[plan-maker Agent](../../../.claude/agents/plan-maker.md)** — Invokes grill-me in Steps
  1 and 8
- **[plan-planning Workflow](../../workflows/plan/plan-planning.md)**
  — Invokes grill-me in Steps 1 and 3
- **[plan-execution Workflow](../../workflows/plan/plan-execution.md)** — Invokes grill-me
  before execution begins
- **[Plans Organization Convention](../../conventions/structure/plans.md)** — Plan structure
  this grilling process serves; grilling decisions are captured in plan documents
- **[Governance Vendor-Independence Convention](../../conventions/structure/governance-vendor-independence.md)**
  — Vendor neutrality rules; Platform Binding Examples allowlist mechanism
- **[Multi-Harness Binding Convention](../../conventions/structure/multi-harness-binding.md)**
  — Two-tier binding model used by the Platform Binding Examples section
- **[Agent Workflow Orchestration Convention](../agents/agent-workflow-orchestration.md)** —
  How agents plan and execute multi-step tasks; grilling is the pre-execution decision gate
- **[Implementation Workflow Convention](./implementation.md)** — "Make it work" first;
  grilling resolves the design decisions that define what "work" means
