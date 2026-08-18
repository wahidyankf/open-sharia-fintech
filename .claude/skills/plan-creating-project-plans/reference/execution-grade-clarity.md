# Execution-Grade Clarity (HARD RULE)

Plans are executed by **execution-grade (sonnet-tier)** agents, not planning-grade (opus-tier) agents. Authoring-grade hand-waving is forbidden.

**Every checkbox MUST contain all of the following that apply**:

- **Explicit file path(s)** when the action touches a known file. When the path cannot be determined at authoring time, give the maximum-possible-detail target: parent directory + naming pattern + sibling reference (e.g., "new file under `apps/organiclever-www/src/lib/` following the pattern of sibling `auth.ts`").
- **Explicit shell command(s)** verbatim when applicable (e.g., `npx nx run ose-web:test:quick`), not "run the lint".
- **Concrete acceptance criterion** stating the observable change that proves done (e.g., "all assertions in `trpc.test.ts` pass", "`nx run ose-web:typecheck` exits 0"). No bare "implement X", "set up Y", "configure Z".

**`plan-checker` flags violations as HIGH severity. `plan-fixer` rewrites offending items with maximum detail.**

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
