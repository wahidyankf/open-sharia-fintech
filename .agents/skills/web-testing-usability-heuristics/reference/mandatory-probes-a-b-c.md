# Mandatory Systematic Probes (Forcing Functions), Part 1: Probes A, B, C

The dimensions checklist gives breadth; these four named probes force the specific
first-time-comprehension failures a heuristic sweep tends to **read past** — because the evaluator,
having already explored the page, stops perceiving them as a newcomer would. Run all four every
`standard`/`thorough` pass, **enumerate** the elements each targets (do not judge a sample), and
record them in the coverage map.

## A. Conditional / hidden-control discoverability

For every control that only **appears** (or only **enables**) after a prerequisite — a toggle that
shows once a quantity is non-zero, a field gated behind a selection, a button disabled until a step
completes — judge whether a first-time user could know it exists before meeting the prerequisite. A
control simply absent with no hint, or disabled with no explanation of what unlocks it, is a finding
citing **Heuristic 6 (Recognition rather than Recall)** and NN/g **Progressive Disclosure** (the path
to a gated feature must be visibly signalled, else users assume it does not exist). Expected: a
ghost/disabled affordance, helper text, or tooltip naming the prerequisite.

> Class this catches: _the school-type toggle that was simply hidden until a school-age child was
> added._

## B. Per-label jargon / real-world-match scan

Enumerate every visible control label, column header, button, and section title. For each, ask
whether a first-time user with no domain knowledge would understand it. Internal/domain jargon with
no plain-language gloss is a finding citing **Heuristic 2 (Match between system and the real
world)**. Expected: plain language, or an adjacent tooltip/help text decoding the term.

> Class this catches: _a baseline-source option labelled "Reference role" with no hint of what it
> means._

## C. Cross-view information-redundancy probe

When the same datum or panel is rendered in more than one view/tab, ask whether the duplication earns
its place or merely competes for attention. Information shown in one view that is already fully
visible in another (and adds nothing there) is a finding citing **Heuristic 8 (Aesthetic &
Minimalist Design)** and **Hick's Law** (redundant data/choices inflate decision cost). Expected: each
datum has one authoritative home unless repetition demonstrably aids the task.

> Class this catches: _the per-city expense breakdown duplicated on the Cost and Savings tabs where
> the table already showed it._
