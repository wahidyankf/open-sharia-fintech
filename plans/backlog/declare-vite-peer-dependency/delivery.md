# Delivery Checklist — Declare the `vite` Every Vitest Config Already Imports

**Delivery Mode**: `worktree-to-pr`. Phase 0 opens no PR; the earliest PR is Phase 1.

**Repositories**: `ose-public` (9 packages) and `ose-private` (1 package). WS-V2 must land in both or
they diverge.

**Sequencing note**: WS-V2's RED is strongest while the ten packages are still undeclared. Phase 1
therefore writes the failing gate test **before** Phase 2 declares anything. If that ordering proves
impractical, Phase 1 may be deferred — but then its RED must use a fixture repository, and that
substitution must be recorded here.

---

## Phase 0 — Baseline

- [ ] [AI] Re-derive the class by command in both repositories rather than trusting this plan's table:
      every `package.json` beside a `vite*.config.*` that declares `vitest`, with its `vite` verdict.
      Acceptance: the printed list matches the README table, or the README is corrected first.
- [ ] [AI] Record the resolved `vite` version in each repository via
      `jq -r '.packages["node_modules/vite"].version' package-lock.json`.
      Acceptance: two versions recorded; if they now share a major, WS-V1's per-repo pinning rationale
      is re-checked before use.
- [ ] [AI] Confirm no `package.json` in either repository declares `vite` except `libs/ts-ui`.
      Acceptance: exactly one match in `ose-private`, zero in `ose-public`.
- [ ] [AI] Run the unit tests of all ten packages and record each test count.
      Acceptance: a baseline table exists; any already-failing suite is resolved before Phase 1.
- [ ] [AI] Confirm both worktrees are clean and level with `origin/main`.
      Acceptance: `git status --short` prints nothing in each.

### Phase 0 Gates

- [ ] [AI] Gate: the derived class list is recorded with a per-package verdict.
- [ ] [AI] Gate: baseline test counts recorded for all ten packages.

## Phase 1 — WS-V2: the gate (delivery boundary)

- [ ] [AI] Write the companion Gherkin at `specs/apps/rhino/` covering AC-3's four scenarios.
      Acceptance: the `rhino-cli` spec-coverage gate exits 0.
- [ ] [AI] RED: unit test asserting a package whose config imports an undeclared module is reported.
      Acceptance: the test **fails** before the implementation exists.
- [ ] [AI] RED: unit test asserting a declared import is **not** reported.
      Acceptance: fails before implementation — a test that passes here is testing nothing.
- [ ] [AI] RED: unit tests for the two non-findings — `node:path` and `./vitest.setup`.
      Acceptance: both fail before implementation.
- [ ] [AI] RED: unit tests for name extraction — `vite/client` → `vite`, `@vitejs/plugin-react/x` →
      `@vitejs/plugin-react`. Acceptance: both fail before implementation.
- [ ] [AI] GREEN: implement the config-import scanner per tech-docs' classification table.
      Acceptance: every RED test above now passes.
- [ ] [AI] Run the gate against the real `ose-public` tree.
      Acceptance: it reports exactly the nine undeclared packages from Phase 0 — no more, no fewer. A
      different count means the scanner's reach is wrong, not that the count changed.
- [ ] [AI] Run the gate against the real `ose-private` tree.
      Acceptance: exactly one finding (`ts-ui-tokens`).
- [ ] [AI] REFACTOR: extract any duplication between the scanner and existing manifest-reading code.
      Acceptance: `rhino-cli:lint` exits 0.
- [ ] [AI] Register the gate in `repo-config.yml` with identical arguments in both repositories.
      Acceptance: `repo-config validate` and `gate validate` exit 0 in each.
- [ ] [AI] Regenerate the parity manifest and stage it in the same commit as the source change.
      Acceptance: `parity manifest validate` reports `diverging=0` in both repositories.
- [ ] [AI] Apply the identical `apps/rhino-cli/` change to `ose-private`.
      Acceptance: the two `parity-manifest.sha256` files are byte-identical.

### Phase 1 Gates

- [ ] [AI] Gate: `nx run rhino-cli:test` and `rhino-cli:lint` both exit 0 in both repositories.
- [ ] [AI] Gate: the gate exits non-zero on both trees, naming exactly the Phase 0 packages.
- [ ] [AI] Gate: `parity manifest validate` reports `diverging=0` in both repositories.
- [ ] [AI] Gate: `pr-quality-gate.yml` green on both PRs.

## Phase 2 — WS-V1: declare the ten (delivery boundary)

- [ ] [AI] For each of the nine `ose-public` packages, add `"vite": "^<resolved>"` to
      `devDependencies`, keeping the map sorted. Acceptance: nine files changed, ranges satisfied by
      the already-resolved version.
- [ ] [AI] Add the same declaration to `ts-ui-tokens` in `ose-private`, pinned to **that** repository's
      resolved version. Acceptance: the range is not copied from `ose-public`.
- [ ] [AI] Run `npm install` in each repository.
      Acceptance: exits 0.
- [ ] [AI] Inspect each lockfile diff and require it to be declaration-only.
      Acceptance: every changed line adds a `vite` declaration to a workspace entry; **zero** changed
      `version`, `resolved`, or `integrity` fields. Any such change is reverted and the range
      re-derived, not accepted.
- [ ] [AI] Re-run all ten packages' unit tests.
      Acceptance: each passes with the **same** test count recorded in Phase 0.
- [ ] [AI] Run the WS-V2 gate on both trees.
      Acceptance: exits 0 in each — zero findings, which is the falsifiable proof WS-V1 is complete.

### Phase 2 Gates

- [ ] [AI] Gate: the config-import gate exits 0 in both repositories.
- [ ] [AI] Gate: both lockfile diffs are declaration-only.
- [ ] [AI] Gate: all ten packages' test counts are unchanged from Phase 0.
- [ ] [AI] Gate: `pr-quality-gate.yml` green on both PRs.

## Phase 3 — Knowledge Capture and Close-Out

- [ ] [AI] Record in `learnings.md` whether any of the ten needed a range other than the resolved
      version, and why. Acceptance: an entry exists, even if the answer is "none did".
- [ ] [AI] Record the general defect this plan closes: a dependency satisfied only by hoisting is
      invisible to every manifest reader and to every gate, so when it does fail there is no way to
      tell "missing" from "unreachable" — which is what made the `ts-ui` incident cost an extra CI
      cycle on a fix that could not have worked.
      Acceptance: the entry is triaged through the routing rubric.
- [ ] [AI] Decide whether the `vite` 7-vs-8 split between the repositories warrants its own plan.
      Acceptance: a recorded verdict — a `plans/backlog/` folder or a written reason it is acceptable.
- [ ] [AI] Merge both PRs, archive the plan to `plans/done/<YYYY-MM-DD>__declare-vite-peer-dependency/`,
      and update the three plan indexes.
- [ ] [AI] Remove both worktrees (non-force), prune, and delete the branches.
- [ ] [AI] Fast-forward both root checkouts' `main`.

### Phase 3 Gates

- [ ] [AI] Gate: both PRs show `MERGED`.
- [ ] [AI] Gate: `learnings.md` has no untriaged entry.
- [ ] [AI] Gate: the plan folder exists only under `plans/done/`.
- [ ] [AI] Gate: `git worktree list` shows no plan worktree in either repository.
