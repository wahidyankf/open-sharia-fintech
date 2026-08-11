---
name: grill-me
description: >
  Interview the user relentlessly about a plan or design, presenting choices one at a time
  until shared understanding is reached. Resolves every branch of the decision tree. Use
  when the user wants to stress-test a plan, get grilled on their design, or mentions
  "grill me".
---

# Grill Me

Stress-test plans and designs through relentless, structured questioning before implementation
begins.

## When to activate

Activate when:

- User says "grill me", "challenge my plan", "stress-test this", "interrogate my design",
  or any close variant
- A new plan is being created and design decisions remain open
- A design review is requested before committing to implementation

## Process

Interview the user about every aspect of the plan until shared understanding is reached. Walk
down each branch of the decision tree, resolving dependencies one-by-one.

This skill is the canonical implementation of the
[Grilling-With-Options Convention](../../../repo-governance/development/workflow/grilling-with-options.md) —
that convention is the normative source for the format, mechanism, and scope below. Keep them in
sync.

**Rules (HARD — no exceptions):**

1. **Explore the codebase first** — if a question can be answered by reading existing files,
   read them instead of asking. Never ask what a file read can answer.
2. Present **2-4 concrete, mutually-exclusive options** per question, each with a one-sentence
   trade-off specific to this decision (no generic "this is simpler" filler) — open-ended
   questions without options are FORBIDDEN. If you cannot enumerate options, read the codebase
   first (Rule 1) and synthesize them before asking.
3. **Mark exactly one option Recommended** with a one-line rationale grounded in the repo state
   and the user's stated constraints. More than one Recommended is forbidden.
4. **One decision per question.** Tightly-coupled decisions (where one answer constrains the
   other) MAY be batched in a single multi-question prompt; unrelated decisions MUST NOT be
   bundled.
5. The user can always supply an **unlisted write-in answer** — options are a starting point, not
   a cage. Treat a write-in with the same weight as a listed option; if it opens a new branch,
   grill on that branch.
6. **Two standing options on EVERY question** — beyond the 2-4 substantive options, ALWAYS
   surface (a) a free-form **type-your-own (blank state)** path whose answer is whatever the user
   types — explicit, never merely implicit (this is the most common omission) — and (b) a
   **"chat about this"** option that lets the user discuss the branch in prose before deciding.
   With `AskUserQuestion`, the auto-provided free-text "Other" entry is the blank-state type; add
   "Let's chat about this" as an explicit option (keep substantive options ≤3 so it fits the
   4-option cap). When the user picks "chat about this", drop the structured options, talk the
   branch through, then return to a structured question once they are ready to decide.
7. Continue until all branches are resolved — do not stop early.

**Violation of Rule 2 (asking without options) is the most common failure mode.** If you catch
yourself writing a question without listing concrete options, rewrite it with options before
sending. **Dropping the blank-state type option (Rule 6) is the second most common failure** —
every question MUST let the user type their own answer.

## Mechanism — use the native interactive tool

Grilling in an interactive root thread MUST use the harness's native interactive
multiple-choice tool when available, not free-text prose questions. It renders options as
selectable choices and returns a structured answer, eliminating parse ambiguity. The root
orchestrator owns every grill and passes resolved answers to a delegated `plan-maker` or
`plan-fixer`; it MUST NOT delegate the user interaction itself.

Use the harness-specific invocation contract in
[Platform Binding Examples](#platform-binding-examples). In all bindings, put the Recommended
option first and append `(Recommended)` to its label, place the rationale in its description,
keep **"Let's chat about this"** as the final explicit option, and rely on the client-provided
free-text **"Other"** entry for the blank-state type.

**Delegated-agent handoff**: a subagent MUST NOT render markdown as if it were asking the user.
It returns `## User Decisions Required` using the
[canonical envelope schema](../../../repo-governance/development/workflow/grilling-with-options.md#user-decisions-required-envelope)
and stops before work that depends on those answers. Every `options` array exhaustively lists all
substantive leaves; the root adds the standing chat option and relies on the client's implicit
custom answer. The root invokes this skill through its native UI when available, then resumes or
reinvokes the specialist with the resolved answers. Direct custom-agent callers receive the same
envelope.

**Fallback only for a genuinely non-interactive root or harness without a native tool**: emit
inline markdown options to the caller, still satisfying Rules 2–5:

> **[Question]**
>
> - **Option A**: [description] — [trade-off] **(Recommended — [rationale])**
> - **Option B**: [description] — [trade-off]
> - **Other — type your own answer**: free-form write-in; the answer is whatever you type (blank
>   state). Always present.
> - **Chat about this**: talk the decision through before deciding. Always present.

No bare "What do you think about X?" questions. No yes/no questions without an options list.
Present the choices; let the user pick or override. Never silently select the Recommended option
or infer an answer because interactive input is unavailable.

## After the grilling

When all decision tree branches are resolved:

1. Summarize every decision made and its rationale
2. Confirm shared understanding explicitly
3. Signal readiness to proceed to plan writing or implementation

## Platform Binding Examples

The content under this heading is intentionally vendor-specific. Per the
[Governance Vendor-Independence Convention](../../../repo-governance/conventions/structure/governance-vendor-independence.md),
the vendor-audit scanner skips every line under this heading until the next same-level heading or
end of file.

### Claude Code

Use `AskUserQuestion` with 1–4 tightly coupled questions per call. Each question object has a
`header` of at most 12 characters, a self-contained `question`, 2–3 substantive
`{ label, description }` option objects plus **"Let's chat about this"** (3–4 total), and
`multiSelect: false`. The client-provided free-text **"Other"** entry remains implicit and satisfies
the blank-state type requirement.

### OpenCode

Use OpenCode's `question` tool with 2–4 substantive options plus the standing **"Let's chat about
this"** option per question, preserving its rich multiple-choice UI path. The client-provided custom
answer remains implicit. If the current version does not expose `question` to the interactive root
thread, use the markdown fallback.

### Codex

Use `request_user_input` in the root thread. One call carries 1–3 tightly coupled question objects;
each object MUST have:

- `header`: a short label of at most 12 characters
- `id`: a stable `snake_case` identifier
- `question`: one self-contained decision prompt
- `options`: 2–3 option objects total; Rule 2's two-substantive-option minimum plus the standing
  **"Let's chat about this"** option means a grill uses exactly 3

Put the Recommended option first and suffix its label with `(Recommended)`. Give every option a
1–5 word `label`, including that suffix, and a one-sentence trade-off in `description`. Do not add an
`Other` option: the client supplies the free-form entry. Each question accepts one answer only; do
not request or simulate multi-select.

When any decision has 3–4 substantive leaves, render a complete staged decision tree.
Every `request_user_input` question still has exactly 2 substantive branch options plus chat. A
branch may group remaining leaves only when its label and description enumerate them; selecting it
opens a subsequent question until every leaf is reachable exactly once. Never truncate the envelope
to fit one prompt.

Codex currently classifies `default_mode_request_user_input` as under development and keeps it off
by default. This repository opts in through `.codex/config.toml` so interactive root threads expose
the native tool outside plan mode. A non-root subagent returns `## User Decisions Required` to the
root and stops. A non-interactive root, including `codex exec`, emits the markdown fallback to its
caller. No context chooses silently.
