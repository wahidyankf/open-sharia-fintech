# Mandatory Pre-Write and Post-Write Grilling

Before writing any plan content, the calling root resolves all open design decisions through a
structured multiple-choice pre-write grill. After writing the plan, the root runs the same
post-write validation grill. Neither gate is optional.

**HARD RULE — 2-4 options required**: Every grilling question MUST present **2-4 concrete,
mutually exclusive options**. Each option MUST state its trade-off in one sentence. Exactly one
option MUST be marked `(Recommended)` with a one-sentence rationale. Open-ended questions without
options are FORBIDDEN. Resolve one decision per question; tightly coupled decisions may be batched
in a single multi-question prompt.

**Interaction ownership**: the root owns native UI interaction and, when it is noninteractive or
lacks a native tool, emits markdown choices to its caller. A plan specialist never questions the
user directly. It returns `## User Decisions Required` using the
[canonical envelope schema](../../../../repo-governance/development/workflow/grilling-with-options.md#user-decisions-required-envelope),
with stable decision ID, question, recommended option and rationale, and exhaustive option objects
with trade-offs, then stops. The root resolves the envelope and resumes or reinvokes the specialist
with the canonical [Resolved User Decisions Envelope](../../../../repo-governance/development/workflow/grilling-with-options.md#resolved-user-decisions-envelope),
constructed from the original IDs after rendering and passed verbatim. The specialist validates it
before dependent work. A direct custom-agent or noninteractive specialist caller receives the same
envelope.

**Explore before composing**: read the relevant repo artifacts before creating an envelope or root
question. Never surface a decision a file read can answer — the repo is the ground truth; the user
is the tiebreaker for genuinely ambiguous decisions.

**Pre-write grill covers** (each as a structured multiple-choice question):

- What problem is this solving? What specific pain point?
- What are the acceptance criteria? How will we know it is done?
- What is the scope? What is explicitly out of scope?
- What are the constraints (performance, harness-neutrality, backwards compatibility)?
- Are there design decision forks where the user has a preference?
- **For UI-bearing plans only**: the UI-design-funnel questions — which low-fi alternatives, what
  prior art, which selection + why (see
  [ui-design-funnel-grilling-and-learning-plans.md](ui-design-funnel-grilling-and-learning-plans.md#design-funnel-grilling-questions-ui-bearing-plans)).

**Post-write grill covers** (each as a structured multiple-choice question):

- Does the plan structure match the user's intent? Are all acceptance criteria captured?
- Is Gherkin completeness sufficient (every acceptance criterion has a scenario)?
- Is checklist granularity correct (each item is one concrete action; TDD substeps separate)?
- Is the `## Worktree` section present?
- Is Phase 0 (Environment Setup and Baseline) the first phase in `delivery.md`?
- Does `delivery.md` open with the `[AI]`/`[HUMAN]` executor legend, and is every step that only a human can do tagged `[HUMAN]`?
- Does every phase end with a `### Phase N Gate` (must-pass verification) followed by a Pause Safety note?

**Do NOT proceed to writing until all pre-write branches are resolved.** A specialist with any open
branch returns `## User Decisions Required` and stops; it never infers an answer. Unresolved design
decisions force expensive rewrites.

See [Grilling-With-Options Convention](../../../../repo-governance/development/workflow/grilling-with-options.md)
for the authoritative rule, validation checklist, and examples. Invoke via the `grill-me` skill.
