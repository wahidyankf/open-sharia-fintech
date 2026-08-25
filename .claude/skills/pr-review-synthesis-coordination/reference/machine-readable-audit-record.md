# Machine-Readable Audit Record (Every Cycle, In the PR Itself)

The PR is the only durable record of its own review. No side log survives, so every fact a future
analysis could want must be posted into the PR at the moment it is true.

The prose header is for humans. This record is for machines, carried in an **HTML comment** that
never renders, so neither audience pays for the other.

## Stable Post Title

Every consolidated review opens with exactly this line, no variants:

```markdown
## PR Review — Cycle N of M
```

Format drift is not cosmetic. A retrospective over PRs #225/#226/#227/#232 found four different
titles and six different finding-header shapes, so cycles could not be ordered without a bespoke
tolerant parser.

## Stable Finding IDs

Every finding is `C<cycle>-F<n>`, `n` restarting at 1 each cycle — `C3-F2` is cycle 3's second
finding, permanently. A finding that recurs cites the earlier ID rather than reusing it.

## The Record Block

Emit this immediately after the prose header, populated for every cycle including a
`trivial`-tier coordinator-only pass:

```html
<!-- ose-pr-review:v1
{"cycle":3,"cycles_max":5,"tier":"full","head_sha":"<40-char SHA>",
 "diff":{"lines_changed":367,"files_changed":44,"files_hand_authored":30},
 "specialists":["architecture","logic","governance","security","integrity"],
 "raw_findings":{"architecture":2,"logic":2,"governance":3},
 "posted":3,
 "probe":{"class":"clause-durability","previously_used":false},
 "dropped":{"below_confidence_floor":2,"reasonableness_filter":1,"deduplicated":1},
 "findings":[{"id":"C3-F1","severity":"HIGH","discipline":"logic","confidence":92,
   "file":"libs/x/src/a.ts","line":42,"raised_by":["logic"],"refutable_by":"rg -F 'X' libs/x/src/a.ts"}]}
-->
```

`probe.class` names the question this cycle asked and `previously_used` says whether an earlier
cycle on this PR asked the same class. The
[exit condition](../../../../repo-governance/workflows/pr/pr-review-quality-gate/probe-variation-and-exit.md)
reads these two fields, so a rule that would otherwise be asserted becomes checkable from the PR
alone.

On a [checkpoint cycle](../../../../repo-governance/workflows/pr/pr-review-quality-gate/convergence-measurement.md)
the block also carries `"checkpoint":{"verdict":"continue|change-fix-strategy|block","original_series":[...],"induced_rate":[...]}`.
All three verdicts are recorded, not only the one that extends a ceiling: a checkpoint whose
`continue` leaves no artifact is indistinguishable from a checkpoint that never ran, and a rule
whose compliance and non-compliance look identical cannot be audited by anyone.

**The counts must balance**: the `raw_findings` values sum to `posted` plus the `dropped` values,
for this cycle alone. Every raw finding is either posted or dropped for exactly one recorded
reason, so a block that does not balance is malformed.

`diff` is recorded here because the GitHub compare API truncates at 300 files and silently returns
a floor — a later analysis reading it back gets the wrong number with no error. `dropped` is
recorded because a filtered finding otherwise leaves no trace at all, making the confidence floor
and the reasonableness filter permanently unmeasurable: their false-negative rate is the one thing
this pipeline cannot currently learn about itself.

Never place a secret, token, or copied vulnerable value in the block — it inherits the same
sanitization rule as every other posted artifact.

## Enforcement

None automated. The block is emitted by this agent and verified by reading the PR. A cycle posting
a review without it has produced an unanalyzable cycle, which is a defect in this agent's output.
