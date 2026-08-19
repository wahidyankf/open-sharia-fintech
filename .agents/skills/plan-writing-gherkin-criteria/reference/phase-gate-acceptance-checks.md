# Gherkin Acceptance Criteria — Phase Gate Acceptance Checks

Phase gate checklist items (inside `### Phase N Gate` blocks in `delivery.md`) are a special
class of acceptance check that must meet the same testability standard as Gherkin scenarios: each
item must be independently verifiable, with a concrete observable outcome, and not reliant on
subjective judgment.

When writing phase gate items, apply the same Given-When-Then reasoning used for Gherkin
scenarios — ask "what is the precondition, what command runs, and what does success look like?" —
then express it as a single runnable check rather than a full scenario block.

See [Plans Organization Convention §Phases as Natural Pauses With Clear Gates](../../../../repo-governance/conventions/structure/plans/phases-as-natural-pauses.md#phases-as-natural-pauses-with-clear-gates-hard-rule)
for the gate structure rule and worked example.
