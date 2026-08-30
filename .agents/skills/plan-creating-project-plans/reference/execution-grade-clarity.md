# Execution-Grade Clarity (HARD RULE)

Plans are executed by **execution-grade (sonnet-tier)** agents, not planning-grade (opus-tier) agents. Authoring-grade hand-waving is forbidden.

**Every outcome section and checkbox MUST be executable by a junior engineer fresh from bootcamp
with no professional work experience and no repository or stack context.**

- The outcome section names its canonical acceptance criterion plus **Input, Outcome, and Proof**.
- Every independently verifiable action is a separate checkbox with an executor tag.

- **Explicit file path(s)** when the action touches a known file. When the path cannot be determined at authoring time, give the maximum-possible-detail target: parent directory + naming pattern + sibling reference (e.g., "new file under `apps/organiclever-www/src/lib/` following the pattern of sibling `auth.ts`").
- **Explicit shell command(s)** verbatim when applicable (e.g., `npx nx run ose-web:test:quick`), not "run the lint".
- **Prerequisites, expected failure/pass state, failure handling, and evidence destination** for
  each action; never assume professional experience supplies a missing step.
- **Separate RED, GREEN, and REFACTOR checkboxes** for every code behavior slice.
- **Concrete proof** stating the observable change that proves done (e.g., "all assertions in
  `trpc.test.ts` pass", "`nx run ose-web:typecheck` exits 0"). No bare "implement X", "set up Y",
  "configure Z".

Canonical Gherkin remains in `prd.md`/`specs/**`; reference IDs/titles instead of copying full
scenarios. Checklist count never overrides natural delivery seams, Delivery Boundaries, or
atomicity. Do not split solely to force handwritten code below the strong 500-line recommendation.
When a natural, cohesive seam exceeds it, record measured size, rejected viable split alternatives,
and review/proof strategy; independent hard PR-size bounds still apply.

**`plan-checker` flags violations as HIGH severity. `plan-fixer` rewrites offending items with maximum detail.**

A finite cross-repository lifecycle checkbox may instead use the canonical same-document controlled
runbook-reference exception when it meets every condition in the
[Plans Organization Convention §Execution-Grade Clarity](../../../../repo-governance/conventions/structure/plans/execution-grade-clarity.md#controlled-runbook-reference-exception).
Do not duplicate that exception here.

## Bad / Good Examples

**Bad** (missing path, missing command, missing criterion):

```markdown
- [ ] Add caching
```

**Good** (explicit path, explicit command, explicit criterion):

```markdown
- [ ] Edit `apps/ose-www/src/server/trpc.ts`: wrap the public router with
      `unstable_cache(..., { revalidate: 300 })`. Verify by running
      `npx nx run ose-web:test:quick` — all tests pass.
```

**Bad**:

```markdown
- [ ] Implement the rate-limit middleware
```

**Good**:

```markdown
- [ ] Create `apps/organiclever-be/src/Middleware/RateLimit.fs` (siblings: `Auth.fs`, `Cors.fs`)
      implementing token-bucket rate limiting per `tech-docs.md §Rate Limiting`. Verify by running
      `npx nx run organiclever-be:test:unit` — new test `RateLimit_RejectsExceedingRequests` passes.
```

**Bad**:

```markdown
- [ ] Run the lint
```

**Good**:

```markdown
- [ ] Run `npx nx affected -t lint` — exits 0 with no errors reported.
```

See [Plans Organization Convention §Execution-Grade Clarity](../../../../repo-governance/conventions/structure/plans/execution-grade-clarity.md#execution-grade-clarity-hard-rule) for the authoritative rule.
