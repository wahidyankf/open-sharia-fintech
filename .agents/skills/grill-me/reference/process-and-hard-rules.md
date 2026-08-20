# Grill Me — Process and Hard Rules

## Process

Interview the user about every aspect of the plan until shared understanding is reached. Walk
down each branch of the decision tree, resolving dependencies one-by-one.

This skill is the canonical implementation of the
[Grilling-With-Options Convention](../../../../repo-governance/development/workflow/grilling-with-options.md) —
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
