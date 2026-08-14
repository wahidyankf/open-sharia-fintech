# Knowledge Capture Routing and Delivery Mode/PR-Review Cycle Verification

## 1. Knowledge Capture Routing Verification (Step 5h — MANDATORY BLOCKING GATE)

Enforces the
[Knowledge Capture Convention](../../../../repo-governance/development/quality/knowledge-capture.md).
This is a **blocking gate** — run it BEFORE the plan is allowed to archive to `plans/done/`. A plan
MUST NOT be archived until every `learnings.md` entry is verified terminal and both safety gates are
confirmed satisfied.

### What to Validate

1. **Every entry reached a terminal state** — read `learnings.md` (or confirm the explicit
   `No generalizable learnings — <reason>` escape if the file is absent or empty). Each surviving
   entry MUST record exactly one of:
   - **Routed inline** (non-code homes only — `docs/`, `repo-governance/`, `.claude/agents/`,
     `.claude/skills/`, post-mortems, or any other non-code durable home) — confirm the referenced
     commit or file edit actually landed in this plan's own history.
   - **Filed as a `plans/backlog/<slug>/` plan** — **mandatory** whenever the home is `apps/`,
     `libs/`, or a test (code); also an acceptable route for any non-code home. Confirm the backlog
     folder actually exists: `Bash test -d plans/backlog/<slug>/`.
   - **Discarded with a one-line reason** — confirm a concrete reason is present, not merely the word
     "discarded". An entry with no terminal state recorded, or left silently open: **CRITICAL**
     finding — archival is BLOCKED until resolved.
2. **No code-homed learning landed inline** — cross-check `learnings.md` against this plan's own
   commit history/diff for any learning whose home is `apps/`, `libs/`, or a test file that was
   implemented directly in this plan's commits/PR instead of filed to `plans/backlog/`. Any code born
   from a learning that landed inline in the current plan — outside the narrow current-plan-blocker
   carve-out (Root Cause Orientation: fixing a genuine blocker to finish this plan's own scope) — is a
   **CRITICAL** finding — archival is BLOCKED.
3. **Secret/sensitivity gate satisfied** — `Grep` `learnings.md` for credential-shaped strings
   (connection strings, API keys, tokens, raw IPs/hostnames outside a `<placeholder>` token). Any
   unsanitized secret found: **CRITICAL** finding — archival is BLOCKED. This inherits the
   [No Secrets in Git Convention](../../../../repo-governance/conventions/security/no-secrets-in-committed-files.md)
   hard iron rule in full.
4. **Repo-relevance gate satisfied** — confirm no infra-private content (Terraform, k3s, Proxmox,
   `coralpolyp`, real hostnames/inventories) was routed into this repo's public surfaces (`docs/`,
   `repo-governance/`, `.claude/`) when this repo is `ose-public` or `ose-primer`. Any cross-routed
   infra-private content: **CRITICAL** finding — archival is BLOCKED.
5. **Mandatory phase presence carried through to archival** — if `plan-checker`'s silent-absence
   MEDIUM finding for the Knowledge Capture phase was never resolved before this archival check runs,
   treat as unresolved: **HIGH** finding, escalated to a blocking condition until either a phase or an
   explicit "none" record exists.
6. **No duplicate two-pager created in `plans/ideas/`** — for any entry routed to `plans/ideas/`,
   confirm the routing note evidences the overlap scan required by
   [Integrate Before You Add](../../../../repo-governance/conventions/structure/plans/03-ideas-folder-overview-rationale-and-file-layout.md#integrate-before-you-add-no-duplicate-two-pagers):
   either it names the pre-existing brief the learning was folded into, or it states the scan of
   `plans/ideas/README.md` found no overlapping brief before a new file was created. A new
   `plans/ideas/<slug>.md` created in this plan's diff without that evidence, or one that duplicates
   an existing brief's topic: **HIGH** finding.

### How to Audit

1. Read `learnings.md` in full (or confirm its absence plus the explicit "none" record elsewhere).
2. For each entry, resolve its recorded routing destination and verify it against the repo:
   `Bash test -d` for backlog folders, `git log`/`git diff` for inline commits.
3. Run `Grep` for secret-shaped patterns across `learnings.md`.
4. Run `Grep` for infra-private terms (Terraform, k3s, Proxmox, `coralpolyp`, real hostnames) across
   any non-`ose-private` routed destination named in the entries.
5. For any entry routed to `plans/ideas/`, `Bash git diff` this plan's commits for new files under
   `plans/ideas/`, then read `plans/ideas/README.md` as it stood before this plan's changes to check
   whether an existing brief already covered the same topic.
6. File findings per the severity table below; a single unresolved entry is sufficient to BLOCK
   archival regardless of how many other entries passed.

### Finding Severity

- Any `learnings.md` entry not in a terminal state at archival time: **CRITICAL** (BLOCKS archival)
- Code-homed learning landed inline instead of filed to `plans/backlog/`: **CRITICAL** (BLOCKS
  archival)
- Unsanitized secret in `learnings.md`: **CRITICAL** (BLOCKS archival)
- Infra-private content cross-routed into a public repo: **CRITICAL** (BLOCKS archival)
- Knowledge Capture phase entirely absent with no explicit "none" record carried through to archival
  time: **HIGH** (escalated from `plan-checker`'s authoring-time MEDIUM if left unresolved)
- New `plans/ideas/` two-pager created without evidence of the overlap scan, or one that duplicates an
  existing brief's topic: **HIGH**

## 2. Delivery Mode and PR-Review Cycle Verification (Step 5i — MANDATORY)

After the Knowledge Capture blocking gate (Step 5h), verify that execution actually matched the
plan's resolved
[Delivery Mode](../../../../repo-governance/conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode).
For `*-to-pr` modes this replaces the plain-`main` assumption baked into Step 5d (Archival) and Step
5e (Worktree) above: archival lands **inside the delivering PR**, and completion does not require the
PR to be merged.

### What to Validate

1. **Resolved mode matches actual execution** — confirm the mode declared in `delivery.md` (or the
   tier-3 default `worktree-to-pr` if undeclared) matches what actually happened: worktree vs.
   primary-checkout work location, and PR vs. direct-push integration target. A mismatch: **HIGH**
   finding.
2. **For `worktree-to-pr` / `main-to-pr`**:
   - **PR exists** and targets `main` from the plan's branch. Missing: **CRITICAL**.
   - **PR's CI gates are green** on the current head SHA. Not green: **CRITICAL** — plan is not done,
     regardless of other criteria.
   - **Review loop ran** — evidence of the PR-Review Maker→Fixer Cycle (default N=3 sequential
     maker→fixer cycles — a **hard ceiling, not a floor**, never extended and never exited early)
     actually executing. Fewer cycles than the plan specified: **HIGH** — there is no legitimate
     early-exit reason under the hard-ceiling rule. No review-loop evidence at all: **CRITICAL**.
   - **Every thread answered/resolved** — zero unresolved threads, OR each remaining open thread
     carries an explicit escalation-to-`[HUMAN]` note in the PR description. An unresolved thread with
     no reply and no escalation note: **HIGH**.
   - **Archival-in-PR present** — the archival commit (`git mv` to `plans/done/` + README updates) is
     part of the delivering PR's own commit history, not deferred to a separate post-merge commit.
     N/A for repos where the plan folder is not tracked. Missing or post-merge-deferred archival on an
     applicable repo: **HIGH**.
   - **Completion does not require merge** — do NOT file a finding solely because the PR is still
     open/unmerged; a green, fully-reviewed, archival-committed PR awaiting its merge is the correct
     terminal state for this mode.
3. **For `worktree-to-origin-main` / `main-to-origin-main`**: confirm no PR-review-cycle evidence is
   expected (its absence is correct, not a finding) and that the final push landed directly on
   `origin main` with CI green — this reuses Step 5d/5e's existing plain-`main` checks unchanged.
4. **No PR was opened for Phase 0** — under **every** mode, Phase 0 is Environment Setup and Baseline
   and must not have produced a pull request. Enumerate the plan's PRs and confirm none corresponds to
   Phase 0 — no `…/phase-0` branch, no PR whose title or body scopes it to Phase 0, and no PR whose
   diff contains only baseline evidence artifacts. A PR actually opened for Phase 0: **HIGH**. Also
   confirm the plan's Phase 0 checklist has no ticked PR/push/merge checkbox — a ticked one is the
   same finding with on-disk evidence. See
   [Plans Organization Convention §Phase 0 Opens No PR](../../../../repo-governance/conventions/structure/plans/23-phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).
5. **PRs match the declared delivery boundaries** — a PR opens at a **delivery boundary**, not at
   every phase. Read the plan's `### Delivery Boundaries` table, then enumerate the PRs actually
   opened. Confirm: (a) each PR corresponds to a declared delivery unit — a PR scoped to an
   intermediate phase is **HIGH**; (b) every declared delivery unit has a PR that **merged** — an
   unmerged unit is **HIGH**; and (c) the count of PRs does not exceed the count of declared
   boundaries. If the plan predates this rule and carries no table, record that as a grandfathering
   note rather than a finding, and check only that no work was left unmerged. See
   [Plans Organization Convention §PRs Open at Delivery Boundaries](../../../../repo-governance/conventions/structure/plans/25-prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).

### Finding Severity

- A PR was opened, reviewed, or merged for the plan's Phase 0 (any mode): **HIGH**
- A PR was opened for a phase the plan does not declare a delivery boundary: **HIGH**
- A declared delivery unit whose PR never merged: **HIGH**
- `*-to-pr` mode: PR missing: **CRITICAL**
- `*-to-pr` mode: PR's CI gates not green: **CRITICAL**
- `*-to-pr` mode: no review-loop evidence at all: **CRITICAL**
- `*-to-pr` mode: fewer review cycles than specified: **HIGH** (no legitimate early exit exists under
  the hard-ceiling rule)
- `*-to-pr` mode: unresolved thread with no reply and no `[HUMAN]` escalation note: **HIGH**
- `*-to-pr` mode: archival-in-PR missing or deferred post-merge (where applicable): **HIGH**
- Filing a finding solely because a `*-to-pr` PR remains unmerged: **not a finding** (false positive
  to avoid — flag the CHECK itself as wrong if this occurs)
