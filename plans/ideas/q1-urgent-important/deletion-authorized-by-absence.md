# Deletion authorized by absence from a hand-maintained list

One-line summary: `harness bindings generate` decides what to **delete** by asking whether a file is
absent from a hand-maintained `vendored[]` allowlist, so every way that list can fail to match
reality — an empty value, a padded value, a typo, a trailing separator — resolves to _destroy the
file_; the safe inversion is to delete only what the emitter itself previously generated.

> Surfaced 2026-08-19/20 across PR-review cycles 4-7 of `update-harness-support`
> (ose-public #232 / ose-private #56). Four consecutive CRITICALs, one root cause.

## Problem / context

The skills-mirror emitter computes `to_remove` as "present under the target directory, not wanted,
and not matched by `is_vendored`". `is_vendored` consults `vendored[]`, a hand-authored list in
`repo-config.yml`. The list is the _only_ thing standing between a tracked vendored file and
`fs::remove_file`. Consequently **any** mismatch between the list and the filesystem is resolved in
the destructive direction. Four distinct shapes reached that outcome, each found by a separate
review cycle, each reproduced live:

- **Empty value** (cycle 4/5). `path_is_under(p, "")` is `true` for every `p`, so an empty entry
  originally made `is_vendored` return true for everything — fail-safe by accident. Cycle 4 added an
  empty-dir guard for an unrelated reason, which inverted it: now false for everything, so every
  mirrored file routed to `to_remove`. A guard added for correctness turned a benign accident into
  data loss.
- **Whitespace-padded value** (cycle 6). `validate_repo_relative_path` tested `value.is_empty()` on
  the raw string and never trimmed, so `" "`, a leading space, a trailing space, and a tab all
  passed validation and then matched nothing. Four more shapes, same outcome.
- **Typo'd value with no `ownership[]` record** (cycle 7). The agreement check added in cycle 6 runs
  only forward ("every vendored-class ownership entry has a `vendored[]` entry"). Its doc comment
  justified excluding the reverse direction as _"an orphaned `vendored[]` declaration simply protects
  nothing additional; it never itself causes a deletion."_ That reasoning is wrong: it is not the
  orphan that deletes, it is the **real** directory left unprotected because the typo'd entry does
  not name it.
- **Trailing-separator mismatch** (cycle 7). The same commit shipped a unit test asserting
  `.agents/skills/foo/` must be accepted, and an agreement check comparing that value to
  `ownership[].path` by exact string equality — so a semantically identical pair was reported as
  drift and aborted the mirror job on a gate that runs on every commit.

Each fix hardened the _validation of the input_ to a decision rule that is unsafe by construction.
That is why there was always another shape: the shapes are unbounded, and the rule converts every
one of them into deletion.

A gate-scoping asymmetry makes it reachable rather than theoretical. Measured in `repo-config.yml`:

| Gate                                                | pre-commit surface                                                        | fires                             |
| --------------------------------------------------- | ------------------------------------------------------------------------- | --------------------------------- |
| `repo-config-schema` (catches a bad registry)       | `scope: affected-file-type`, `glob: repo-config.yml`, no pre-push surface | only when that one file is staged |
| `harness-bindings-generate` (performs the deletion) | `scope: other`, `restages: true`                                          | every commit, unconditionally     |

The validator that protects the invariant is conditionally scoped; the mutator that violates it is
not. Once a non-conforming registry lands by any route that skipped the conditional gate, every
later unrelated commit silently deletes and re-stages the payload.

## Why now

The immediate shapes are closed — cycles 5-7 plus a terminal pass added a trim rejection, a
bidirectional agreement check, and component-wise comparison. But the **decision rule is unchanged**:
deletion is still authorized by absence from a hand-maintained list. The current state is a
well-guarded unsafe design, not a safe one. The next contributor to add a `vendored[]` entry is one
unanticipated shape away from the same outcome, and the class has already demonstrated it produces
one new shape per review cycle.

`DD-7` and the feature file's own title already state the correct invariant — _"the emitter owns
only what it generates"_. The implementation does not enforce it; it enforces the contrapositive of
a list.

## Prior art / precedents

- **Default-deny / capability-style authorization.** Deletion should require a positive capability
  ("I generated this file"), never the absence of a protective declaration. Standard security
  reasoning, applied to a filesystem mutation.
- **`vendored-skill-preservation.feature`** — already titled for the correct invariant; the natural
  home for a scenario stating it as a property rather than per-shape.
  [feature](../../../specs/apps/rhino/behavior/rhino-cli/gherkin/harness/vendored-skill-preservation.feature)
- **Ownership classes (SOURCE / GENERATED / VENDORED)** — the repo already models exactly the
  distinction the safe rule needs; the emitter simply does not consult it as the deletion authority.
  [ownership-classes](../../../repo-governance/conventions/structure/multi-harness-binding/ownership-classes.md)
- **Falsifiable acceptance evidence** — the per-shape tests here all passed in both directions and
  still left the class open, which is the same "verified the wrong thing" family.

## Proposed direction (sketch)

- **Invert the authority.** Compute `to_remove` from a manifest of what the emitter previously
  generated, not from "everything not declared protected". A file the emitter never wrote is not
  the emitter's to delete, whatever the registry says.
- **Make the invariant a property test, not a shape test.** Assert _no registry content causes the
  deletion of a file the emitter did not generate_, and drive it with generated/fuzzed `vendored[]`
  values. Every one of the four shapes above would have fallen out of one such test.
- **Gate symmetry rule.** A destructive mutation gate must be scoped at least as broadly as the
  validator that protects its precondition. Worth stating repo-wide, not just here — the table above
  is a general trap, not a `vendored[]` quirk.

## Rough scope & non-goals

In scope: the deletion-authority inversion in the skills-mirror emitter; the property test; the
gate-symmetry rule as a governance statement.

Out of scope (for now): re-litigating the shapes already closed; redesigning the ownership-class
model itself; changing `repo-config.yml`'s hand-authored nature, which is deliberate.

## Risks & open questions

- A generated-output manifest is new persistent state, and this repo has an explicit prohibition on
  timestamp-based detection — the manifest must be content-addressed, and where it lives (tracked
  file, or derived each run from the source tree) is unresolved. (open)
- Inverting the authority may change behaviour for a genuinely stale mirror file that the emitter
  _did_ generate under an older configuration — the migration path for existing trees needs a stated
  answer before promotion. (open)
- Whether the gate-symmetry rule is mechanically checkable from `repo-config.yml` (compare each
  mutation gate's surface against its named validator's) or only a review convention. Mechanical
  looks feasible and would be the higher-leverage half.

## What success looks like + promotion signal

Success: a fuzzed `vendored[]` value cannot cause the deletion of any file the emitter did not
generate, demonstrated by a property test that fails when the authority is reverted to the current
allowlist rule. Secondary: no destructive gate in `repo-config.yml` is more broadly scoped than the
validator guarding it.

Ready to promote once the manifest-location question is answered — the inversion's shape depends on
whether generated-output provenance is stored or re-derived.
