# Technical Documentation — oxlint Upgrade and Lint-Toolchain Reproducibility

## 1. Evidence Method

Every claim below was derived by command, not by reading. Re-derive at execution time; the version
numbers are a snapshot.

| Question                           | Command                                                     |
| ---------------------------------- | ----------------------------------------------------------- |
| When did each oxlint version ship? | `npm view oxlint time --json`                               |
| Did our diff touch the named tree? | `git diff --name-only <base>..<head> -- apps/ose-www/src`   |
| Did the same branch pass before?   | `gh pr checks 227` across successive heads                  |
| How many sites resolve unpinned?   | `grep -rn 'oxlint@latest' --include=project.json`           |
| Is the failure version-caused?     | Run both versions against the same tree, compare exit codes |

The last row is the one that matters: a claim that "an upgrade caused this" is only sound if the old
version passes and the new one fails **on identical source**. That was checked:

| oxlint | `apps/ose-www` result                                               |
| ------ | ------------------------------------------------------------------- |
| 1.78.0 | exit 0                                                              |
| 1.79.0 | `search-dialog.tsx:36:7: error react(set-state-in-effect)` — exit 1 |

## 2. WS-O1 — the `set-state-in-effect` violation

### The code

`apps/ose-www/src/features/search/shell/search-dialog.tsx`:

```tsx
useEffect(() => {
  if (!query || query.length < 2) {
    setResults([]); // line 36 — synchronous setState inside an effect
    return;
  }
  const timer = setTimeout(async () => {
    try {
      const data = await trpcClient.search.query.query({ query, limit: 10 });
      setResults(data); // asynchronous — not flagged, and correct
    } catch {
      setResults([]);
    }
  }, 200);
  return () => clearTimeout(timer);
}, [query]);
```

Only the guard branch is flagged. It runs during the effect, synchronously, and schedules a second
render immediately after the first — the cascading-render pattern the rule names.

### The design

oxlint's message states the remedy: _"Derive the value during render, initialize state directly, or
update it from the event that caused the change."_ The first applies cleanly here, because "results
are empty when the query is too short" is not state — it is a **function of** the query:

```tsx
const visibleResults = !query || query.length < 2 ? [] : results;
```

The effect then keeps only its debounce, with no early-return setState. `results` remains the raw
fetch buffer; `visibleResults` is what renders.

This is strictly better than disabling the rule: it removes a render cycle on every keystroke below
the threshold, and it makes the empty-state rule readable in one line instead of being implied by
effect ordering.

**Consider also**: the first effect's dependency array includes `open` and calls `setOpen(!open)`,
re-registering the keydown listener on every toggle. Not flagged, out of scope, but worth a look
while in the file.

### Testing

An observable behaviour change in an app, so
[Feature Change Completeness](../../../repo-governance/development/quality/feature-change-completeness.md)
applies: companion Gherkin under `specs/apps/ose-www/`, plus a unit test asserting that typing a
one-character query renders no results and that clearing a query drops previously-fetched results.
The regression test must fail before the fix and pass after.

## 3. WS-O2 — take the upgrade

Move both repositories from 1.78.0 to current in the same delivery unit. They must not diverge.

Procedure:

1. Run the current oxlint against every one of the 22 call sites **before** changing the pin, and
   record the full finding list. This is the specification for the rest of the workstream.
2. Triage each finding: fix, or disable in `oxlint.json` with a stated reason. A finding may not be
   left unaddressed and unexplained.
3. Change the pin, run every affected lint target, confirm exit 0.

Sequencing: WS-O1 lands first. If the upgrade and the `search-dialog` fix land together, a failure
cannot be attributed to either.

## 4. WS-O3 — prevent the class

Begin with enumeration, not remediation. The question is not "should we pin oxlint" — that is done —
but **what else gates CI while resolving at run time**.

Sweep `project.json`, `package.json`, `.github/workflows/`, and `.husky/` for run-time resolution:
`npx <pkg>@latest`, bare `npx <pkg>` where the package is undeclared, `curl | sh` installers, and
unpinned action refs (`uses: foo/bar@main`). Produce a per-item verdict table: pinned / deliberately
floating with reason / must pin.

Then decide the durable mechanism. Candidates, to be chosen during execution rather than presumed:

- A governance convention stating that no CI-gating tool may resolve at run time, plus a `rhino-cli`
  validator enforcing it — consistent with how this repository enforces its other invariants.
- Automated dependency updates, so pinning does not mean stagnating.

The `rhino-cli` option carries the four-repo parity-manifest obligation and its own TDD cycle. Cost
it before committing to it.

## 5. Dependency Bump Policy Classification (WS-O2)

Per the
[Dependency Bump Stability & Safety Policy](../../../repo-governance/development/workflow/dependency-bump-policy.md),
every `devDependency` bump — oxlint included — must classify under the Three-Path Decision Tree
before the pin changes, and record a Security Clearance Status before the manifest edit lands.

**Path**: oxlint carries no LTS designation (unlike Node.js or .NET) — **Path B (60-day stable +
CVE-clean)** applies, not "take the latest published release."

**Cutoff (snapshot, re-derive at execution — see §1 Evidence Method)**: authored 2026-08-21; cutoff
= bump date − 60 days = 2026-06-22. Per `npm view oxlint time --json`, the latest release published
on or before that cutoff is `1.71.0` (2026-06-22). §3's "move ... to current" means "current within
the applicable path," not the literal newest tag — Phase 2 MUST re-run this cutoff calculation
against the actual execution date and MUST NOT pin to a release younger than 60 days without a
documented Path C waiver.

**Security Clearance Status**

This is the execution-time decision register required by the policy. It deliberately does not claim
CVE-clean status before Phase 2 selects and clears the final version. A pending row is a stop
condition, not clearance.

| Item   | Planned change surface                       | Required exact pin                                               | Selection route                                                                        | Clearance status at plan authoring                                                                                                                                                                                                                                                                                                                                                 |
| ------ | -------------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| oxlint | `package.json` `devDependencies`, both repos | TBD — Phase 2 re-derives the Path B cutoff at the execution date | **Path B** — 60-day soak, no LTS line; candidate at authoring is `1.71.0` (2026-06-22) | **PENDING** — Phase 2 must clear the selected version against NVD, GitHub Advisories, Snyk, oxlint's own security page, and CISA KEV per the [CVE Clearance Process](../../../repo-governance/development/workflow/dependency-bump-policy/cve-clearance-process.md), and record the final `CLEAR`/`CLEAR (patch-of)`/`WAIVER`/`FUNCTIONAL-HOLD` status here before the pin changes |

## 6. Related

- [`repo-rules-sweep`](../../done/2026-08-18__repo-rules-sweep/README.md) — where this surfaced; its
  inline pin is the blocker carve-out of the Code-Routing Downstream Rule, not a scope breach.
- [Reproducible Environments](../../../AGENTS.md) — the standard an unpinned linter violates.
