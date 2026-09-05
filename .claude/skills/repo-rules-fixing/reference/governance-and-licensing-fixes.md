# Rules Governance and Licensing Fixes

## Rules Governance Fixes

Five categories, each re-validated against current file state before fixing (never trust the
audit report's snapshot):

Quality-gate filtering follows [Lifecycle Delegation](./lifecycle-delegation.md).

**Contradictions** — two governance documents state incompatible rules for the same situation.
Confidence HIGH only when both passages are quoted verbatim in the finding and genuinely
irreconcilable (not merely differently scoped). Fix: align the newer/more-specific doc's wording
into the older/general one, never delete either document.

**Inaccuracies** — a governance document describes tooling/behaviour that no longer matches the
codebase (a renamed command, a removed flag, a changed default). Confidence HIGH only when the
current codebase state is independently confirmed via Grep/Read, not just asserted by the finding.

**Inconsistencies** — the same convention is phrased differently across documents without being
contradictory (a formatting nuance, an example using outdated syntax). Fix: standardize on the
canonical doc's phrasing, update the others to match or link to it instead of restating.

**Traceability Violations** — a rule references a convention/ADR that doesn't exist, or a
convention exists with no rule enforcing it. Fix: add the missing cross-reference, or flag for
human judgment if the missing piece requires new authoring (not just linking).

**Layer Coherence** — content lives at the wrong governance layer (e.g., a workflow-specific
detail stated in a repo-wide convention). Fix: move the content to its correct layer, leave a
pointer at the original location.

**Validated Consolidation** — for any `Propagation Consolidation` finding, reconstruct the full
subject-scoped inventory of rule and discoverability surfaces. For each surface, record its
canonical home and exactly one verdict: keep, amend, merge, delete, relocate, or supersede. Then act
on every verdict while preserving each distinct obligation and necessary discoverability path;
record the rationale for keep. This never permits deleting a document to resolve a contradiction.

## Important Guidelines for Rules Fixes

- Never delete a governance document to resolve a contradiction — reconcile the wording instead.
- Quote the exact conflicting/inaccurate passage in the fix report, not a paraphrase.
- When a fix touches a convention that other agents' `## Required Reading` sections point at,
  re-verify those agents still make sense post-fix (their pointer, not their content).
- Layer-coherence moves are HIGH confidence only when the destination layer already exists and is
  unambiguous — otherwise flag for human placement decision.
- Governance-prose vendor-neutrality is out of scope for this skill — see
  `repo-harness-compatibility-protocol` Invariant 1/2 instead.

## Licensing Convention Fixes

**Missing LICENSE (CRITICAL)**: every app/lib directory requires its own `LICENSE` file. Fix:
`cp libs/web-ui/LICENSE apps/[dir]/LICENSE` (or the nearest correctly-licensed sibling), then
verify the copied file's content matches exactly via `diff`.

**Wrong License Type (HIGH)**: the `LICENSE` file's declared type doesn't match the project's
canonical license. Fix: replace with the correct license text, never hand-edit license boilerplate.

**Cross-Document Inconsistency (MEDIUM)**: a README or doc states a different license than the
actual `LICENSE` file. `LICENSING-NOTICE.md` is the source of truth — reconcile every inconsistent
reference to match it, never the other way around.
