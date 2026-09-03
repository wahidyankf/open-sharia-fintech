# PR Boundary Detection and Consistency Validation (Scope 5)

For `*-to-pr` modes, run these **detection commands** from the plan folder and compare the two
number sets. For direct modes, inspect the declared direct-checkpoint steps instead of requiring PR
commands.

```bash
# (1) phases the plan DECLARES as delivery boundaries
grep -oE 'yes[^|]*Phase [0-9]+' delivery.md | grep -oE '[0-9]+$' | sort -un | tr '\n' ' '

# (2) phases that ACTUALLY carry an integration step
awk '
  /^## Phase [0-9]+/ { n=$3; sub(/[^0-9].*$/,"",n) }
  /^ *- \[ \]/       { if (buf) print buf; buf = n "\t" $0; next }
  /^ *- \[x\]/ || /^ *$/ || /^#/ { if (buf) print buf; buf = ""; next }
  buf                { buf = buf " " $0 }
  END                { if (buf) print buf }
' delivery.md \
  | grep -viE 'gh pr list|no PR (here|at this gate)' \
  | grep -Ei 'gh pr create|gh pr ready|open (a )?(draft )?pr|draft pr opened|PR-Review|review cycle|\[AI\]`?-merged|auto-merge' \
  | cut -f1 | sort -un | tr '\n' ' '
```

Command (2) restricts to **unticked** `- [ ]` lines deliberately: _checklist_ excludes prose (a
sentence mentioning "merged PR" isn't a step); _unticked_ excludes history (a `- [x]` step is a merge
that already happened — unactionable, and would fire forever on a part-executed plan). The rule binds
PRs a plan has **yet** to open, not executed history.

The awk accumulates each checklist **item** (its `- [ ]` line plus wrapped continuation lines) before
matching — load-bearing, not tidiness: a boundary step typically reads `- [ ] [AI] **Delivery
boundary …PR opens.**` on one line with `[AI]-merged` on a following indented line. Line-by-line
matching puts the keyword out of reach and silently reports zero integration steps on a plan with
three — the worst failure mode for a checker. The `grep -v` pre-filter drops steps that _query_
integration (e.g. `gh pr list --state open`) rather than cause it.

Sanity-check on a trusted plan before believing a zero. Acceptance: every number in (2) also appears
in (1). Falsifiable both ways: `gh pr create` added to an intermediate phase appears in (2) not (1)
(fails); promoting it to a boundary row makes it appear in both (passes). A number in (1) absent from
(2) is the separate defect of a declared boundary with no integration step — report it too.

Also flag: a change-producing phase in **no** table row (**HIGH** — no declared route to `main`); a
non-boundary final change-producing phase (**HIGH** — that work never merges); a missing
`### Delivery Boundaries` table on a non-trivial plan (**MEDIUM**,
`grep -c '^### Delivery Boundaries' delivery.md` returns `0`); a single end-of-plan boundary against
a `## Parallelization Model` declaring independent parallel nodes (**MEDIUM** — re-serialises the
DAG).

Remediation: move integration steps to the delivery unit's boundary phase, or promote a genuinely
boundary-qualifying intermediate phase and add its table row. A qualifying boundary follows one
natural cohesive seam, keeps all required build/verification/operation/rollback/consistency
artifacts together, and leaves `main` immediately safe to deploy to production. Incomplete behavior
requires a temporary production-disabled flag, both path tests, and rollout/rollback/removal. Never
derive a boundary from LOC or file counts, and never delete the work's route to `main`.

## 5. Consistency Validation

Requirements align with delivery steps; technical docs support the implementation approach;
acceptance criteria match user stories; no contradictions between sections.
