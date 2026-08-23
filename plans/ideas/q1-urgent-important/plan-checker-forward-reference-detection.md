# Teach plan-checker to catch cross-phase forward references

One-line summary: a delivery step can name an artifact that a **later** phase is the one to create,
and nothing catches it — `plan-checker` validates structure and completeness, not whether a step's
own command text is satisfiable given what earlier phases have actually built by that point.

> Surfaced 2026-08-09 during `optimize-cis` execution.

## Problem / context

Two independent instances in a single plan (`optimize-cis`), at two different layers — which is what
makes this a class rather than an authoring slip.

**Instance 1 — a Cargo profile that does not exist yet.** Phase 2's step specified
`cargo build --profile gate` and `target/gate/rhino-cli`, but `[profile.gate]` is not added to
`Cargo.toml` until **Phase 4** — which even carries its own dedicated step to repoint the script at
`--profile gate`, proving the sequencing was always meant to be later. Executed literally, the first
test exercising the build-fallback path would have hard-errored with
``error: profile `gate` is not defined``. It was caught only because the executing agent proactively
flagged the missing profile before writing the script. **Five `plan-checker` / `plan-fixer`
iterations had already run clean over this exact text.**

**Instance 2 — a Gherkin scenario nothing can bind.** Phase 5's step instructed adding the AC-9 and
AC-10 CI-topology scenarios to `gate-execution.feature` during Phase 5 — but AC-9 describes a
`build-rhino` job **Phase 6** creates and AC-10 a conditional node-setup input **Phase 7** creates.
`specs gherkin-cardinality validate` passed immediately, because it only checks keyword structure.
The real failure surfaced one layer deeper: `gate_specs.rs`'s cucumber suite requires a literal,
**passing** step binding for every scenario in the whole `gherkin/gate/` tree regardless of which
phase "owns" it, and there was no truthful way to bind either scenario — the behavior they assert
did not exist. Forcing a binding would have meant fabricating a fixture asserting against nothing.

Both were fixed by moving the authoring into the phase where the behavior actually lands. Neither was
caught by a checker.

### A sibling gap, same root (2026-08-21)

`repository-onboarding-readme-refresh` Phase 0 found the mirror image of a forward reference: not a
step naming something that does not exist yet, but a plan **transcribing** a live registry and
silently transcribing a subset. The plan listed eight `pre-commit` gates; the registry declares 29.

Most of the gap was benign — language formatters a documentation diff never triggers — but it hid
three gates that do fire on that plan's own declared file footprint: `repo-config validate`,
`convention emoji validate`, and `git lockfile sync`. A plan can be structurally perfect and still
be wrong about the repository it runs in, and nothing reads it that way.

The reconciliation has to run in **both** directions. "Does every transcribed command exist" is the
easy half and passes here. The half that caught this is "which live gates does the transcription
omit that this plan's declared footprint can trip." Both are mechanical, and both belong wherever
this brief's check lands.

## Why now

The two instances cost an execution-time catch and a mid-plan re-sequencing, both of which happened
to go well because the executing agent was paying attention. That is the failure mode worth acting
on: **the class is currently caught by vigilance, not by a gate.** The next instance lands in a phase
whose executor is less suspicious, and the plan hard-errors mid-execution.

It is also cheap to detect relative to what it costs to hit. Both instances are visible in the plan
text alone — no repo state needed, just the phase ordering and what each phase claims to create.

Against acting now: this needs a real design pass, because the naive version (grep each step for
identifiers created by later steps) will drown in false positives on ordinary prose.

## Prior art / precedents

- **`optimize-cis`** — both instances, recorded in its `learnings.md` with the second explicitly
  logged as "2nd instance of the cross-phase forward-reference class."
- **Related planning evidence** — a decision record can drift from its plan, and a clause can be
  unable to fail; a forward reference is the mirror image, where the clause cannot pass. Fold these
  failure modes together before promoting a planning rule.
- **[Trustworthy Measurement](../../../repo-governance/development/practice/trustworthy-measurement.md)** —
  its rule 4 ("a remedy written before anyone saw a timeline is a hypothesis") is the same underlying
  problem in the metrics domain: plan text authored ahead of the state it assumes.

## Proposed direction (sketch)

The detectable signal is narrow and mechanical, which is the reason to think this is tractable at
all: a step **creates** named artifacts and **consumes** named artifacts, and consumption must not
precede creation.

- **Step 0 — see how far a cheap version gets.** Extract, per phase, the artifacts each step claims
  to create (file paths written, config sections added, jobs/targets introduced) and the artifacts
  each step's command text references. Flag any reference whose only creator is a later phase. Run
  it over the plans already in `done/` and count false positives before building anything further.
- **Start with the two proven high-signal shapes** rather than general prose: a Cargo/Nx/CI artifact
  referenced in a command (`--profile X`, a target name, a job id), and a Gherkin scenario whose
  asserted behavior lands in a later phase. Both are the ones that actually hard-errored.
- **Bind the Gherkin case to the real constraint**: this repo's coverage tooling requires whole-tree,
  always-live bindings, so a scenario must be authored in the phase that creates its behavior or an
  **earlier** one — never a later one. That is a flat rule, not a heuristic, and is worth stating in
  the plan conventions regardless of whether the checker ever automates it.
- **If automated detection proves noisy**, fall back to a `plan-checker` prompt-level step: "for each
  step, name the phase that creates every artifact the step's command references" — slower and
  model-dependent, but the failure mode is a false flag rather than a missed one.

## Rough scope & non-goals

**In scope**: detect, at plan-quality-gate time, a delivery step referencing an artifact created only
by a later phase; cover the Cargo-profile shape and the Gherkin-scenario shape at minimum; state the
Gherkin same-or-earlier-phase rule in the plan conventions.

**Out of scope**:

- Whether a step is a _good_ step, correctly scoped, or well sequenced for any reason other than
  artifact availability. That is a different and much harder question.
- Runtime/execution-time validation. This is a pre-execution check on plan text.
- Rewriting `plan-fixer` to auto-repair a detected forward reference. Detection first; the repair is
  usually "move the step", which needs judgment about which phase should own it.

## Risks & open questions

- What is the false-positive rate of the cheap version on the existing `done/` corpus? If it is high,
  the whole automated branch is dead and the prompt-level fallback is the answer. **(open)**
- Can "what a step creates" be extracted reliably from prose at all, or does it need plans to declare
  it? A declaration requirement is a real authoring cost and would need its own justification.
  **(open)**
- Are there legitimate forward references — a step that intentionally names something a later phase
  builds, as documentation of intent rather than as an executable instruction? If so the check needs
  an opt-out, and an opt-out that is easy to reach is an opt-out that gets reached. **(open)**
- Does this belong in `plan-checker` at all, or in the `specs`/`gherkin-cardinality` validator for
  the Gherkin half? Splitting it across two tools risks each assuming the other covers it. **(open)**
- Rabbit hole: building a general dependency graph over plan steps. Both real instances were single
  named artifacts referenced one to three phases early — the general graph is a much larger project
  than the evidence supports.

## What success looks like + promotion signal

Success: a plan containing either of the two proven shapes fails its quality gate with the offending
step and the creating phase both named, and the `done/` corpus produces no false positives — or, if
automation proves untenable, the same class is caught by a stated `plan-checker` step and the Gherkin
same-or-earlier rule is written into the plan conventions.

**Promotion signal**: the Step 0 false-positive count over the `done/` corpus. That number decides
between "small `plan-checker` addition" and "prompt-level step plus a convention", and until it
exists there is no way to scope the work.
