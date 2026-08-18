# Idea Briefs (Two-Pagers)

This folder holds **two-pagers**: shortened, promotable idea briefs that are richer than a one-line
todo but deliberately **not** full five-document plans. Each idea is one `<slug>.md` file. `ideas/`
is the first stage of the plan lifecycle:

```text
ideas/ (two-pagers) → backlog/ (full 5-doc plans) → in-progress/ → done/
```

## Two-Pagers

Grouped into Eisenhower quadrants by [`plan-ideas-grooming`](../../repo-governance/workflows/plan/plan-ideas-grooming.md).

### Q1 — Urgent & Important

Blocks an active plan or documents a live defect, and carries a cross-repo, security, data-integrity, CI-gate, or checker-enforced stake. Do these first.

- [acceptance-clause-vacuity](./q1-urgent-important/acceptance-clause-vacuity.md) — acceptance clauses that cannot fail certify nothing; require falsifiability in both directions.
- [agents-md-progressive-disclosure](./q1-urgent-important/agents-md-progressive-disclosure.md) — `AGENTS.md` sits under 20 B beneath its 30,000 B ceiling; restore headroom via progressive disclosure.
- [markdownlint-ci-gate-lints-zero-files](./q1-urgent-important/markdownlint-ci-gate-lints-zero-files.md) — the `markdownlint` gate declares `all-file-type` with no glob, so CI runs it with empty argv, lints `0 file(s)`, and has always passed vacuously.
- [mermaid-validator-does-not-check-syntax](./q1-urgent-important/mermaid-validator-does-not-check-syntax.md) — `md mermaid validate` is cited as the Mermaid-correctness gate but never parses syntax; broken diagrams pass clean.
- [plan-checker-forward-reference-detection](./q1-urgent-important/plan-checker-forward-reference-detection.md) — a step can name an artifact only a later phase creates; two instances hard-errored in one plan after five clean checker passes.
- [plan-decision-integrity-hardening](./q1-urgent-important/plan-decision-integrity-hardening.md) — four authoring-time rules plus a mechanical `plan-checker` step stop a plan shipping pre-loaded with its own successor.
- [rhino-cli-parity-propagation-optimize-cis](./q1-urgent-important/rhino-cli-parity-propagation-optimize-cis.md) — `apps/rhino-cli` byte-identity parity is broken against `ose-private`, whose sibling PR already merged, with nothing left to propagate it automatically.

### Q2 — Important, Not Urgent

No active plan waits on these and no live defect is running, but each carries a real stake. This is the plan-from-here quadrant.

- [actions-cache-eviction-policy](./q2-not-urgent-important/actions-cache-eviction-policy.md) — the Actions cache sits at 99.29 % of its 10 GiB ceiling because nothing ever deletes an entry; only GitHub's LRU relieves pressure.
- [audit-e2e-reuse-existing-server-config](./q2-not-urgent-important/audit-e2e-reuse-existing-server-config.md) — a stale dev server on the target port silently absorbs e2e runs via unconditional `reuseExistingServer: true`.
- [ayokoding-content-checker-coverage](./q2-not-urgent-important/ayokoding-content-checker-coverage.md) — enforce the canonical topic-tree shape in the content checkers; add a by-concept checker.
- [ayokoding-course-root-overview-parity](./q2-not-urgent-important/ayokoding-course-root-overview-parity.md) — 23 of 181 AyoKoding courses lack a root `overview.md`; two layouts coexist and cross-course links already guessed wrong once.
- [ayokoding-database-internals-ruff-config](./q2-not-urgent-important/ayokoding-database-internals-ruff-config.md) — 22 sibling courses carry a scoped `ruff.toml` and this one does not, though `ruff format --check` currently passes clean.
- [ayokoding-mermaid-diagram-remediation](./q2-not-urgent-important/ayokoding-mermaid-diagram-remediation.md) — 636 mermaid violations exposed by the `detect_kind` fix; remediate and drop the temporary CI exclude.
- [ayokoding-www-app-shell-tap-targets](./q2-not-urgent-important/ayokoding-www-app-shell-tap-targets.md) — shared header/footer tap targets render 17-20 CSS px tall against WCAG 2.5.8's 24x24 floor, site-wide and unguarded by CI.
- [bare-repo-landing-method-step-count-drift](./q2-not-urgent-important/bare-repo-landing-method-step-count-drift.md) — the landing method numbers eight steps but is summarized as "seven-step" in nine sites across three repos.
- [beavernest-first-deploy](./q2-not-urgent-important/beavernest-first-deploy.md) — provision the first real `prod`/`stag` deploy targets for `beavernest-app`/`beavernest-be`; the deployer agents and CI callers ship wired but dormant.
- [beavernest-local-full-stack-development](./q2-not-urgent-important/beavernest-local-full-stack-development.md) — make one development command own BeaverNest's local data lifecycle, same-origin Flutter/F# runtime, and supported edit loop.
- [behavior-coverage-json-report-wiring](./q2-not-urgent-important/behavior-coverage-json-report-wiring.md) — wire rhino-cli's JSON-run-report cross-check into project targets + CI.
- [ci-setup-rust-toolchain-retry](./q2-not-urgent-important/ci-setup-rust-toolchain-retry.md) — `setup-rust` flaked 7× in one phase on the toolchain download; add a retry in both parity repos.
- [class-sweep-completeness](./q2-not-urgent-important/class-sweep-completeness.md) — class sweeps miss producer surfaces, root instruction files, and the block around a cited substring.
- [coverage-artifact-relative-paths](./q2-not-urgent-important/coverage-artifact-relative-paths.md) — generated coverage files bake in the last runner's absolute path; most instances are gitignored, but a 2026-08-18 re-check found one finding overstated.
- [cross-repo-governance-link-parity](./q2-not-urgent-important/cross-repo-governance-link-parity.md) — governance docs copied to a sibling repo carry anchors that break there; check link parity before the copy, not at the destination's push gate.
- [cross-repo-port-registry](./q2-not-urgent-important/cross-repo-port-registry.md) — port allocation across the four sibling repos lives in four separate prose tables, so a collision is caught only when two apps fail to bind at once.
- [deploy-targets-registry](./q2-not-urgent-important/deploy-targets-registry.md) — declare `prod-*`/`stag-*` deploy branches in `repo-config.yml` instead of deriving their existence from `git branch -r`.
- [doc-command-existence-validation](./q2-not-urgent-important/doc-command-existence-validation.md) — a rhino-cli validator catching doc-cited commands that don't exist.
- [doctor-fix-polyglot-restore](./q2-not-urgent-important/doctor-fix-polyglot-restore.md) — `doctor --fix` verifies toolchain presence but not per-project restore state (NuGet, npm-workspace hoisting), leaving idle checkouts pre-push-red until manually diagnosed.
- [gate-exclusions-need-a-named-owner](./q2-not-urgent-important/gate-exclusions-need-a-named-owner.md) — a gate's `exclude:` list records that a tree is skipped but never who checks it instead, so an exclusion outlives the tool that justified it.
- [governance-command-name-reconciliation](./q2-not-urgent-important/governance-command-name-reconciliation.md) — governance tables cite Nx targets and npm scripts that do not exist, and three `sync:*` scripts invoke a removed `rhino-cli` subcommand.
- [governance-path-ownership-registry](./q2-not-urgent-important/governance-path-ownership-registry.md) — declare glob→agent→dimension ownership in `repo-config.yml` with a validator, and close the five zero-owner governance paths.
- [harness-binding-catalog-drift](./q2-not-urgent-important/harness-binding-catalog-drift.md) — triage the 2026-07-20 harness-compatibility external-drift findings.
- [harness-converter-preserve-agent-mode](./q2-not-urgent-important/harness-converter-preserve-agent-mode.md) — the agent converter emits a fixed field set, so OpenCode-only frontmatter like `mode: subagent` is dropped once an agent gains a `.claude/` source.
- [iam-service-module](./q2-not-urgent-important/iam-service-module.md) — a shared IAM (authn/authz) capability; early placeholder, mostly open questions.
- [merge-queue-adoption](./q2-not-urgent-important/merge-queue-adoption.md) — merge-precondition (c) cannot hold under concurrent merges, but GitHub's native queue is gated on organization ownership both parity repos lack.
- [mermaid-state-label-render-clipping-warn](./q2-not-urgent-important/mermaid-state-label-render-clipping-warn.md) — a WARN rule for `stateDiagram-v2` edge labels that clip in GitHub's renderer.
- [nx-affected-cross-worktree-contamination](./q2-not-urgent-important/nx-affected-cross-worktree-contamination.md) — `nx affected` includes uncommitted working-directory changes, so a concurrent plan's stray WIP blocked an unrelated docs-only push.
- [ose-private-opencode-ci-monitor-orphan](./q2-not-urgent-important/ose-private-opencode-ci-monitor-orphan.md) — an unsourced `.opencode/agents/ci-monitor-subagent.md` mirror survives only via a hardcoded filename skip both parity repos inherit.
- [plan-archival-in-pr-multi-repo-gap](./q2-not-urgent-important/plan-archival-in-pr-multi-repo-gap.md) — `plan-execution.md` §8's Archival-in-PR rule has no provision for a plan whose delivery spans multiple repositories.
- [plan-quality-gate-convergence](./q2-not-urgent-important/plan-quality-gate-convergence.md) — make the plan-quality-gate loop converge in a bounded number of iterations without relaxing checks.
- [post-cutoff-dependency-migrations](./q2-not-urgent-important/post-cutoff-dependency-migrations.md) — track and promote the deferred dependency bumps as their soak windows clear.
- [pr-review-bot-identity](./q2-not-urgent-important/pr-review-bot-identity.md) — a dedicated bot identity so blocking reviews post as `REQUEST_CHANGES`.
- [propagation-checklist-under-coverage](./q2-not-urgent-important/propagation-checklist-under-coverage.md) — propagation checklists enumerated by change ID under-cover the merged changeset; derive the file list from the PR diff.
- [refresh-agent-illustrative-example-paths](./q2-not-urgent-important/refresh-agent-illustrative-example-paths.md) — 4 generic agent definitions still illustrate usage with example paths naming apps this repo deleted.
- [repo-rules-quality-gate-convergence](./q2-not-urgent-important/repo-rules-quality-gate-convergence.md) — turn the repo-rules sweep into a bounded, count-diff convergence loop.
- [rhino-cli-env-backup-scripts](./q2-not-urgent-important/rhino-cli-env-backup-scripts.md) — scripted backup/restore of the gitignored rhino-cli `.env*` files.
- [rhino-cli-exclude-dir-shared-steps-gap](./q2-not-urgent-important/rhino-cli-exclude-dir-shared-steps-gap.md) — thread `--exclude-dir` through rhino-cli's whole-app step scan so both sides of a `--shared-steps` comparison exclude the same dirs.
- [rhino-cli-git-env-scrub-widening](./q2-not-urgent-important/rhino-cli-git-env-scrub-widening.md) — `find_root_from` scrubs only `GIT_DIR`/`GIT_WORK_TREE` before invoking `git rev-parse`, leaving `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, and `GIT_COMMON_DIR` unscrubbed.
- [rhino-cli-md-links-json-output-scenario-gap](./q2-not-urgent-important/rhino-cli-md-links-json-output-scenario-gap.md) — the retired CLI link checkers' `Scenario: JSON output produces structured results` has no equivalent in `rhino-cli`'s successor feature, though the behaviour is live and unit-tested.
- [rhino-cli-sync-validator-wrong-model-drift](./q2-not-urgent-important/rhino-cli-sync-validator-wrong-model-drift.md) — a one-line test-fixture placeholder in `sync_validator.rs` diverges from ose-public, violating the zero-carve-out `apps/rhino-cli` byte-identity rule.
- [rhino-cli-tools-superset-carveout](./q2-not-urgent-important/rhino-cli-tools-superset-carveout.md) — `doctor/tools.rs`'s "zero carve-outs" byte-identity target collides with `ose-private`'s real, needed IaC tool-provisioning extensions.
- [rust-crate-structural-checklist-promotion](./q2-not-urgent-important/rust-crate-structural-checklist-promotion.md) — promote the Rust crate structural checklist to governance once a 2nd crate exists.
- [sdlc-gate-standard-property-bound-lag](./q2-not-urgent-important/sdlc-gate-standard-property-bound-lag.md) — `ose-public`'s SDLC gate standard trails both siblings on two name-bound bareness claims; adopt their wording.
- [shared-cargo-target-lock-contention](./q2-not-urgent-important/shared-cargo-target-lock-contention.md) — one shared cargo target directory reclaims disk but serializes concurrent worktree builds; a 65 s pure-lock-wait stall was measured.
- [sibling-main-ci-never-runs-on-merge](./q2-not-urgent-important/sibling-main-ci-never-runs-on-merge.md) — `main-ci` is schedule-triggered in `ose-private`, so a merge to its `main` gets no post-merge CI signal.
- [source-code-credential-scanning](./q2-not-urgent-important/source-code-credential-scanning.md) — evaluate Betterleaks (gitleaks successor) for pre-commit + CI credential detection in source.
- [specs-checker-phantom-nx-targets](./q2-not-urgent-important/specs-checker-phantom-nx-targets.md) — `specs-checker.md`'s Drift Detection section names Nx targets that don't exist.
- [stale-checkout-ref-advance-drift](./q2-not-urgent-important/stale-checkout-ref-advance-drift.md) — a ref-advancing `fetch` moved a checked-out branch 9 commits without its index, and git reported the drift as 265 staged files two agent sessions deferred to.
- [standardize-cis](./q2-not-urgent-important/standardize-cis.md) — audit for any CI-standardization residual left by the toolchain-parity work.
- [syllabus-conformance-validator](./q2-not-urgent-important/syllabus-conformance-validator.md) — a deterministic `rhino-cli md syllabus validate` for course-file section conformance, deferred until the format settles.
- [vendor-audit-kiro-term](./q2-not-urgent-important/vendor-audit-kiro-term.md) — add `Kiro` to the vendor-audit denylist before it leaks into governance prose.
- [vitest-glob-coverage-guard](./q2-not-urgent-important/vitest-glob-coverage-guard.md) — a regression test that matched no Vitest project's include glob ran zero times and passed green; guard the class.
- [web-ui-alert-destructive-dark-contrast](./q2-not-urgent-important/web-ui-alert-destructive-dark-contrast.md) — shared `Alert variant="destructive"` renders at 1.99:1 in dark mode; the obvious token fix is unsafe.

### Q3 — Urgent, Not Important

Something active references these, but they carry none of the importance signals. Delegate or timebox.

- [beavernest-database-config-test-flake](./q3-urgent-not-important/beavernest-database-config-test-flake.md) — seven cases share one bare `Assert.True`, so three `.NET quality gate` flakes have produced no evidence about which case is nondeterministic.
- [ayokoding-www-e2e-coverage-gaps](./q3-urgent-not-important/ayokoding-www-e2e-coverage-gaps.md) — implement the ~104 + 83 missing Playwright step defs so e2e can revert to `fail-on-gen`.

### Q4 — Neither Urgent nor Important

Parked deliberately. Kept because the need may become real, not because it is real now.

- [ayokoding-i18n-nav-hardening](./q4-not-urgent-not-important/ayokoding-i18n-nav-hardening.md) — pre-existing id-locale, language-switcher-404, and sidebar-clip defects surfaced by the url-restructure Phase-5 retest.
- [ayokoding-www-cost-reduction](./q4-not-urgent-not-important/ayokoding-www-cost-reduction.md) — retire the 3 MB search index, ~700 KB client mermaid, 97 MB image copy, and the not-XSS-safe HTML parser in one coordinated pass.
- [ayokoding-www-e2e-parallel-load-flake](./q4-not-urgent-not-important/ayokoding-www-e2e-parallel-load-flake.md) — the e2e suite flakes under full-suite parallel-worker load (isolated re-runs pass); stabilize or quarantine.
- [beavernest-be-nullbyte-path-error-envelope](./q4-not-urgent-not-important/beavernest-be-nullbyte-path-error-envelope.md) — a null-byte-path request gets a bare Kestrel 400 instead of `beavernest-be`'s usual `{"error": "..."}` envelope.
- [beavernest-first-llm-integration](./q4-not-urgent-not-important/beavernest-first-llm-integration.md) — give `beavernest-be` its first real AI-assistant capability; no capture, notes, LLM calls, or prompt plumbing exist yet.
- [beavernest-persistence-layer](./q4-not-urgent-not-important/beavernest-persistence-layer.md) — introduce the first concrete BeaverNest feature that durably stores and retrieves product data on the SQLite foundation.
- [dependency-library-updates](./q4-not-urgent-not-important/dependency-library-updates.md) — a standing, policy-compliant sweep to advance pinned library dependencies as their soak windows clear.
- [fsl-standards](./q4-not-urgent-not-important/fsl-standards.md) — clarify the intent behind "FSL standards" and, if warranted, codify a licensing standard around the Functional Source License.
- [harden-ayokoding-www-fe-e2e-bulk-link-concurrency](./q4-not-urgent-not-important/harden-ayokoding-www-fe-e2e-bulk-link-concurrency.md) — two step files check every page link via unbounded `Promise.all`, flaking a required gate 4 runs in 7; bound the concurrency.
- [vercel-cost-steady-state-verification](./q4-not-urgent-not-important/vercel-cost-steady-state-verification.md) — grade the shipped cost fix against the $30 invoice ceiling once the first clean billing cycle closes on 2026-09-26.

## What a Two-Pager Is

A two-pager sits between a throwaway one-liner and a full backlog plan: short enough to write in one
sitting and triage at a glance, yet structured enough to decide whether to promote it. Target ≤ ~2
printed pages, ~8 short sections:

1. **Title + one-line summary** (plus a provenance note when it came from a plan)
2. **Problem / context** — a specific example of why the status quo doesn't work, with concrete data points (counts/sizes/measurements; never fabricated)
3. **Why now** — the urgency, dependency, or opportunity window
4. **Prior art / precedents** — 2-5 named precedents (tool/pattern/standard/prior plan) with links; lightweight at capture, deep `web-researcher` study deferred to promotion
5. **Proposed direction (sketch)** — core elements only; **not** wireframes, file paths, or Gherkin
6. **Rough scope & non-goals** — in-scope bullets + an explicit out-of-scope list
7. **Risks & open questions** — rabbit holes + the unknowns that block promotion
8. **What success looks like + promotion signal**

Keep it a brief, not a plan: one paragraph per section, no fabricated metrics, no secrets, and no
BRD/PRD/tech-docs/delivery split (that is the backlog plan's job).

## Before You Add — Integrate, Don't Duplicate

Before creating a new two-pager, scan the index above for an existing brief on the same problem or
area and **fold the new thought into it** rather than adding a near-duplicate. Two two-pagers about
the same underlying problem should be one. This applies equally to learnings routed here by the
Knowledge Capture phase — check for an existing home first.

## Promoting a Two-Pager to a Plan

Promotion is a **completeness gate, not a perfection gate**: an idea is ripe when every section holds
a real answer — including honest open questions — and the remaining questions genuinely need a full
plan's deeper work to answer. When a two-pager is ripe, create `backlog/<slug>/` as a full plan, carry
the problem/scope/questions forward, then **delete** the two-pager and drop its line above. "Not
promoted yet" is a legitimate state, distinct from "rejected".

## See Also

- [Plans Organization Convention → Ideas Folder (Two-Pagers)](../../repo-governance/conventions/structure/plans/03-ideas-folder-overview-rationale-and-file-layout.md#ideas-folder-two-pagers)
  — the authoritative convention, template, and discipline.
- [Knowledge Capture Convention](../../repo-governance/development/quality/knowledge-capture.md) —
  routes future-work learnings from plan execution here as two-pagers.

## Grooming Log

### 2026-08-06 — plan-ideas-grooming (all four OSE repos in one run)

Swept 120 two-pagers across `ose-public`, `ose-primer`, `ose-private`, and `beaver-nest`; 79 survive. Every surviving idea carries a residency verdict (R1 secrets-bearing, R2 single-repo-only, R3 generalizable) and an Eisenhower quadrant.

- **Classified**: 60 idea(s) resident here, filed into quadrant folders.
- **Relocated in** (9):
  - `coverage-artifact-relative-paths.md` from `beaver-nest` — rule R3: generalizable cross-cutting concern; no secret required, present in 2+ repos
  - `cross-repo-port-registry.md` from `beaver-nest` — rule R3: generalizable cross-cutting concern; no secret required, present in 2+ repos
  - `ose-public-nx-affected-rhino-cli-gap.md` from `ose-private` — rule R3: generalizable cross-cutting concern; no secret required, present in 2+ repos
  - `refresh-agent-illustrative-example-paths.md` from `beaver-nest` — rule R3: generalizable cross-cutting concern; no secret required, present in 2+ repos
  - `rhino-cli-exclude-dir-shared-steps-gap.md` from `ose-primer` — rule R3: generalizable cross-cutting concern; no secret required, present in 2+ repos
  - `rhino-cli-sync-validator-wrong-model-drift.md` from `ose-private` — rule R3: generalizable cross-cutting concern; no secret required, present in 2+ repos
  - `specs-checker-phantom-nx-targets.md` from `beaver-nest` — rule R3: generalizable cross-cutting concern; no secret required, present in 2+ repos
  - `dependency-library-updates.md` from `ose-private` — rule R3: generalizable cross-cutting concern; no secret required, present in 2+ repos
  - `fsl-standards.md` from `ose-private` — rule R3: generalizable cross-cutting concern; no secret required, present in 2+ repos
- **Deduplicated out** (1) — the surviving copy is named for each:
  - `demo-apps-standards-recheck.md` → `ose-primer/plans/ideas/q2-not-urgent-important/demo-apps-standards-recheck.md`
- **Unresolved follow-ups**: none. No relocation was interrupted and no filename collision was
  deferred. One inbound link sat in `plans/backlog/beaver-nest-repo-consolidation/`, an untracked
  plan folder that was another actor's in-flight work at grooming time; its single reference to
  `post-cutoff-dependency-migrations.md` was repointed at the new quadrant path in the working tree
  and left for that folder's own author to commit, since this run does not stage their files.

> Last groomed: 2026-08-06
