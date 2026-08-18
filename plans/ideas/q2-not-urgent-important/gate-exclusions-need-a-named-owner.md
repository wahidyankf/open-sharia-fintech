# Gate Exclusions Need a Named Owner

One-line summary: a gate's `exclude:` list records that a tree is skipped but never why or who
covers it instead, so an exclusion outlives the tool that justified it and the tree ends up checked
by nothing while the board stays green.

> Surfaced 2026-08-18 during `repo-clean-up`, which retired two link-checking CLIs and found the
> `md-links` gate had been excluding exactly the trees those CLIs were believed to cover.

## Problem / context

`repo-config.yml`'s `md-links` gate carried three exclusions. One, `plans/done`, is a deliberate
historical-record carve-out. The other two, `apps/ayokoding-www/content` and `apps/ose-www/content`,
existed because `ayokoding-cli` and `ose-cli` were understood to check those trees themselves.

Neither CLI had been executed in months. `ayokoding-cli` had no Nx target invoking it at all;
`ose-cli`'s `ose-www:links:check` target existed but appeared in no gate, no hook, no CI workflow,
and no `test:quick`. So the arrangement was: gate skips the tree, delegated owner never runs, tree
checked by nobody, every board green. The gap had no symptom because a gate that skips a tree and a
gate that finds nothing wrong in it produce identical output.

The measured cost of arming it was one broken link across both trees — trivial, which is the point:
nobody would have accepted the gap if the price of closing it had ever been visible.

Note the failure is not "someone forgot". The exclusion was correct when written. What the config
cannot express is the fact it depended on, so nothing connected the retirement of the CLIs to the
exclusions they justified.

## Why now

Cheap while the instance is fresh, and the class is live: `repo-config.yml` currently carries
exclusions across several gates, and no one has enumerated which are deliberate carve-outs and which
are delegations to a named owner. Every future tool retirement inherits the same blind spot.

## Prior art / precedents

- [`markdownlint-ci-gate-lints-zero-files`](../q1-urgent-important/markdownlint-ci-gate-lints-zero-files.md)
  — the sibling shape: a gate that runs and checks nothing. Its item 4 (fail any `check` whose
  candidate count is zero) is the closest existing remedy, and it would not catch this one, because
  an excluded tree still leaves a non-zero candidate count elsewhere.
- [`doc-command-existence-validation`](./doc-command-existence-validation.md) — the neighbouring
  "a gate should be provably non-vacuous" idea.
- `repo-config.yml:968-975` — house precedent for a comment explaining a non-obvious gate choice.
  The mechanism already exists as convention; it is simply not required.

## Proposed direction (sketch)

Require every `exclude:` entry to carry a reason, distinguishing at minimum a **carve-out** (this
tree is deliberately unchecked, and here is why that is acceptable) from a **delegation** (this tree
is checked by X instead). A delegation names X. Then a retirement has something to grep for, and a
delegation whose owner no longer exists is a mechanical, detectable defect rather than an
archaeological one. Whether that reason lives in a structured field or an enforced comment is open.

## Rough scope & non-goals

In scope: the shape of `exclude:` entries in `repo-config.yml`, an audit of the existing ones across
both parity repos, and whatever check makes a dangling delegation detectable.

Out of scope: changing which trees are excluded — this is about making the reason legible, not
re-adjudicating any particular exclusion. Also out of scope: the general vacuous-gate question,
which its own two-pager owns.

## Risks & open questions

- How many exclusions exist today, and how many are delegations rather than carve-outs? Nobody has
  counted. If nearly all are carve-outs, this is documentation, not enforcement. (open)
- Structured field versus enforced comment: a field is checkable but changes the schema in both
  repos; a comment is free but only a reviewer enforces it. (open)
- Rabbit hole: this could expand into "every gate must justify its scope", which is a much larger
  design question than the concrete defect that produced this brief.

## What success looks like + promotion signal

Success: a delegation whose named owner has been deleted is caught by a command rather than by
someone happening to retire the owner and think to look. Ready to promote once the exclusion census
is done and the field-versus-comment question is settled.
