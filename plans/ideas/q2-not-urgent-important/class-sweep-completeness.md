# Class sweeps that miss the class

One-line summary: when a change narrows a rule, sweeping "the sites the finding named" is not the
same as sweeping the class — producer surfaces, root instruction files, and the enclosing block
around a cited substring are the three places a sweep reliably misses.

> Surfaced 2026-07-21/22 during `bare-repo-governance-hardening` Phases 4 and 5 (three distinct
> shapes, each found by a _later_ PR-review cycle than the one that declared the sweep complete).

## Problem / context

One change narrowed the set of legal delivery-mode values in a bare repository. Three separate
review cycles each declared the sweep done; each was wrong in a different way.

- **Reading surfaces got it; writing surfaces did not.** Every document that _describes_ the
  delivery-mode vocabulary was updated — the plans convention, the parity workflow, the SDLC gate
  standard, `trunk-based-development.md` and its SKILL mirror. The agents and skills that _emit_ a
  value from that vocabulary were not: the plan-maker's mode table, the plan-creating SKILL's mode
  section, the git-push default standard, and — found only by sweeping, cited by nobody — the
  plan-planning grill question and the plan-fixer's mode-fix options. The validator checks only that
  the declared value is one of the four legal strings, **by explicit design**, so a wrong value
  passes every gate and fails at execution. When the checker is structurally unable to carry a
  restriction, the producers are the _only_ place it can live.
- **Root instruction files are the default blind spot.** A fixer commit titled "add bareness
  carve-outs to every mode-declaring surface" reached the agents, the skills, and the governance
  docs — and missed `AGENTS.md`, where a case-insensitive search for `bare` returned **no matches at
  all**. `AGENTS.md` is the file every harness auto-loads on every invocation: the highest-traffic
  mode-declaring surface in the repo, and the one most likely to be the actual source of a wrong
  declaration. It was missed because a sweep is naturally written as a walk over the directories
  that hold the artifact class, and root files sit outside all of them.
- **The unit of edit is the enclosing block, not the cited substring.** One fix changed a worked
  example's comment line to the corrected mode name and left the two commands beneath it — which
  demonstrate the _other_ mode — untouched, so the label and the body of one five-line block
  contradicted each other. Another rewrote a precondition sentence for one reason and silently
  dropped an unrelated conjunct from it, in the single copy explicitly designated **normative**,
  while six derivative copies kept the conjunct. Every check anyone would think to run passes on
  that loss: grep for the new wording passes, grep for the removed old wording passes, link check
  passes, lint passes. And the usual safety net inverted — a "do these copies agree?" spot-check on
  any two of the six derivatives would have looked fine while the authoritative copy was the wrong
  one.

### Second instance, 2026-08-18 (`repo-clean-up`)

A retirement sweep over four deleted project names reproduced the class and added three shapes the
first instance did not name. Notably, all three are cases where the _correct_ action was **not** to
edit the matched site — the opposite failure mode from the three above.

- **The exception list is the sweep.** The acceptance clause named three exempt roots. Execution
  found five more legitimate ones: inert `#[cfg(test)]` fixture strings behind a parity boundary,
  another in-progress plan's dated audit ledger, an `assert_no_match` guard, the plan's own prose,
  and a dated retarget note. Each would have read as a failure against the written clause, and the
  cheap fix for each is to edit the file rather than the clause. A sweep clause that enumerates
  matches without enumerating accepted non-matches pushes the executor toward the wrong repair.
- **Deleting a matched token can weaken a test.** One hit was
  `assert_no_match grep -Eq 'beavernest-app-web|…'` — an assertion that the workflow does _not_
  mention the removed app. It looks exactly like a stale reference. Removing it would have silently
  deleted a passing assertion: the CI-gaming shape, reached by mechanical tidying rather than by
  intent. Absence-assertions must name the absent thing, so they always match a sweep for it.
- **The neighbouring sentence is where the other errors live.** Correcting a `rust-commons` mention
  in an idea brief required reading around it, which exposed a claim that no `fsharp-crane-core`
  existed in the repo — it does, along with the exact file the brief says is absent, inverting one
  of its findings. A token-matching sweep never reads the sentence.

### A fourth missed-site shape: the definitional site (2026-08-21)

`repository-onboarding-readme-refresh` Phase 2 took three passes to retire one false claim, and the
third pass worked only because the method changed.

A reviewer found the plan's ledger asserting that two path trees are byte-identical with
`ose-private`. The real boundary is seven pathspecs, and of the 27 `identity-bound` Markdown paths
exactly 25 are in the 603-entry parity manifest. The reviewer named four sites; those four were
fixed; the next pass found the claim alive at two more — including the **vocabulary entry that
defines the label the fix was about**, sitting 1,150 lines above the correction. Two of the six
sites were ones neither reviewer nor executor had looked at, and one of those carried a second,
unrelated error.

What closed it: instead of patching cited line numbers, grep the whole delivery unit for every term
in the claim's _vocabulary_ — here `byte-identical`, `byte identity`, `identity-bound`,
`identity boundary`, `zero carve-outs` — classify all 47 hits as definition, assertion, or
incidental reference, and give each a verdict. The reviewer then enumerated independently and found
no seventh site.

This adds a fourth shape to the three this brief already names, and it is the one that most
reliably undoes a sweep: **the definitional site re-injects the error into every downstream use of
the term, including the uses you have just fixed.** Check definitions first.

## Why now

The pattern repeated three times inside one plan, each time surviving a review cycle that had
explicitly been asked to sweep, and then recurred in a second, unrelated plan five weeks later with
three further shapes. That is evidence the failure is structural rather than a lapse of care: the
sweep is being expressed in a way that cannot reach these surfaces. Every future rule narrowing — of
a delivery mode, a naming enum, a permitted command set — and every retirement sweep inherits them.

## Prior art / precedents

- **Maker-Checker-Fixer pattern** — where a fixer's obligations are defined; the "re-read the whole
  enclosing block" rule belongs here.
  [maker-checker-fixer](../../../repo-governance/development/pattern/maker-checker-fixer.md)
- **PR Review Quality Gate workflow** — the loop that caught all three, one cycle later than it
  should have each time.
  [pr-review-quality-gate](../../../repo-governance/workflows/pr/pr-review-quality-gate.md)
- **Multi-harness binding + platform-binding catalog** — the existing precedent for enumerating
  _every_ surface a class lives on rather than walking a directory; the same enumeration discipline
  is what a class sweep needs.
  [platform-bindings](../../../docs/reference/platform-bindings.md)
- **`propagation-checklist-under-coverage`** — the sibling brief; same family (a list that
  under-covers), different mechanism (cross-repo rather than cross-surface).
  [brief](./propagation-checklist-under-coverage.md)
- **Interface-vs-implementation change discipline** — the general engineering habit of asking "who
  produces this value?" and not only "who documents it?" when narrowing a type.

## Proposed direction (sketch)

- **Enumerate producers and validators, not just prose.** When a change restricts a declared enum or
  narrows a rule, the sweep names the surfaces that _emit_ a value (agents, skills, grill questions,
  templates, worked examples) and states explicitly whether the validator can carry the restriction.
  If it cannot — by design or otherwise — say so, because that makes the producer sweep
  load-bearing rather than belt-and-braces.
- **Name root instruction files in the sweep, always.** `AGENTS.md`, `CLAUDE.md`, `CONVENTIONS.md`
  are listed by name in any class sweep, never left to a directory walk.
- **Fixer re-reads the enclosing block.** After changing a cited substring, the fixer re-reads the
  whole unit that contains it — the example, list item, precondition, table row — and confirms every
  part still agrees. For a rewritten multi-clause sentence, diff for what was **removed**, not only
  for what was added.
- **Check the normative copy first.** Where one copy is designated authoritative and others are
  derivatives, a defect in the authoritative copy outranks agreement among the derivatives, so
  agreement between derivatives is not evidence of correctness.

## Rough scope & non-goals

In scope: the class-sweep requirements in the maker-checker-fixer pattern and the PR-review
quality-gate workflow — producer/validator enumeration, root-file naming, enclosing-block re-read,
normative-copy priority.

Out of scope (for now): making the delivery-mode validator topology-aware (a real question, but a
different one — this brief is about how sweeps are specified, not about that particular enum);
building a tool that discovers producer surfaces automatically; re-sweeping already-merged changes.

## Risks & open questions

- "Enumerate the producers" is easy to state and hard to bound: for a widely-used vocabulary the
  producer set may not be knowable without a full-text sweep anyway, in which case the rule
  degenerates into "grep everything". Where the enumeration comes from — a maintained registry, or
  discovery per change — is unresolved. (open)
- Re-reading the enclosing block is straightforwardly right and straightforwardly slower. Whether it
  applies to every fixer edit or only to edits inside worked examples and normative statements needs
  deciding. (open)
- Naming root instruction files in every sweep collides with the instruction-size budget: the
  correct fix for one repo's root file was blocked outright by its byte ceiling, so "sweep must
  include the root file" and "root file has no headroom" can both be true at once. See
  [agents-md-progressive-disclosure](../q1-urgent-important/agents-md-progressive-disclosure.md).

## What success looks like + promotion signal

Success: the next change that narrows a declared vocabulary lands with its producer surfaces and its
validator's capability stated up front, includes the root instruction files by name, and needs no
follow-up review cycle to find a missed surface — measured simply as "how many later cycles found a
site the sweep should have covered", which was three-for-three on this plan.

Ready to promote once the producer-enumeration question is settled — registry versus per-change
discovery is the choice that determines whether this is a documentation change or a tooling one.
