# Learnings: ayokoding-learning-path-01-url-restructure

Transient running log. The executor appends one entry per generalizable learning **as it surfaces**,
sanitized before it is written. Phase 7 (Knowledge Capture) triages every entry to a durable home or
discards it with a reason; nothing is left in a non-terminal state at archival.

**Before writing any entry**, apply the two safety gates:

- **Secret / sensitivity gate** — replace any secret, credential, token, or private hostname with a
  `<placeholder>` token; discard the entry outright if it cannot be sanitized.
- **Repo-relevance gate** — infra-private content (Terraform, k3s, Proxmox, real hostnames or
  inventories) stays in `ose-infra` only and is never cross-routed into this repo.

**Code-routing rule** — a learning whose home is `apps/`, `libs/`, or tests is **ALWAYS** filed as a
separate `plans/backlog/<slug>/` plan and **NEVER** landed inline in this plan's commits or PR. The
only carve-out is a blocker genuinely required to finish this plan's own scope (Root Cause
Orientation).

Entry shape:

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized)
- **Why it might generalize**: the litmus reasoning
- **Routing**: _(filled at Phase 7 — durable home, backlog plan slug, or discard reason)_
```

## Entries

## Learning: `ls` is shell-aliased to `eza` — `ls … | xargs` corrupts output

- **Context**: Phase 0, freezing the 37 re-home slugs via
  `ls -d …/*/ | xargs -n1 basename > evidence/phase-0-rehome-slugs.txt`.
- **Observation**: `ls` resolves to `eza --icons --hyperlink` in this environment. Piping its
  hyperlinked (OSC-8-escaped) output through `xargs` collapsed 37 directory names into 2 garbled
  lines with embedded escape codes. Invoking `/bin/ls` explicitly produced the correct 37 lines.
- **Why it might generalize**: distinct from the plan's already-documented `find`/RTK hazard — this is
  an `ls`-alias hazard. Any later step (or any plan) that pipes `ls` into `xargs`/`while read`/`wc`
  must use `/bin/ls` (or `command ls`). Phases 1–3 of this plan use `ls`-based enumeration.
- **Routing**: **Routed** to a durable operator-memory reference (`reference_ls_is_eza_xargs_hazard`),
  filed alongside the existing `grep`-is-ripgrep and RTK-`find` hazards — a cross-session environment
  hazard, not repo code. Terminal.

## Learning: tech-docs ground-truth counts drift; re-measure at Phase 0, don't trust the authored table

- **Context**: Phase 0 baseline inventory vs. tech-docs' "Ground-truth inventory" table.
- **Observation**: `fundamentally-strong` measured 562 `.md` on disk (git-tracked) vs. 563 stated in
  tech-docs — a stale authored count, confirmed via `git ls-files` + `git log --diff-filter=DR` (no
  deletions), i.e. authoring-time miscount, not a session regression. Reconciled in tech-docs (table +
  tree) and the delivery baseline string this session.
- **Why it might generalize**: any plan that hard-codes a repo-measured count in its docs should have
  a Phase-0 step that re-measures and reconciles before a later phase asserts on it — the count the
  author wrote can be stale by the time the plan runs.
- **Routing**: **Discarded** — plan-specific. The generalizable form ("re-measure repo-grounded counts
  at Phase 0, don't trust the authored table") is already embodied in this plan's Phase-0 re-measure
  steps and in the repo's existing anti-hallucination "repo-ground every count" guidance; no new durable
  surface would catch it that does not already exist. Terminal.

## Learning: `generate-indexes` owns section bodies — persistent index prose must live in frontmatter

- **Context**: Phase 1, authoring the five structural `paths/**/_index.md` indexes required by DD-49
  to render "acceptably empty, never blank."
- **Observation**: `index-generator.ts` (`rebuildIndexFile`) rewrites every `isSection` `_index.md`
  **body** from its live children on `generate-indexes`, and `validate-indexes` gates equality — so a
  childless section's hand-written body sentence is erased and cannot be reinstated without failing
  the gate. The plan's "write a body sentence" step and its "validate-indexes must pass" step were
  mutually exclusive for childless buckets. Fix: put the sentence in a `description:` **frontmatter**
  field (preserved verbatim by the generator); the page still renders title + breadcrumb + prev/next
  (not a 404). Visible empty-state deferred to the render-layer plan.
- **Why it might generalize**: any plan that seeds a section index expecting persistent hand prose
  must use frontmatter (or a generator-preserved region), never the body, in a repo whose index
  generator regenerates section bodies. A plan step that mandates both "author body prose" and "run +
  validate the index generator" is internally contradictory for childless sections.
- **Routing**: **Folded** into [`plans/ideas/acceptance-clause-vacuity.md`](../../ideas/acceptance-clause-vacuity.md)
  as instance (a) of its new "self-contradictory acceptance steps" sub-class — a phase that mandates a
  hand-written index body AND `validate-indexes` passing is internally inconsistent because the generator
  regenerates section bodies. Terminal.

- **Phase 2 — pre-existing e2e flake in an unrelated tool surfaced under the full-suite parallel load.**
  `ayokoding-www-fe-e2e:test:e2e`'s `tools/cost-of-living-calculator.feature` ("Minimum-role tab is dual
  currency") fails intermittently under full-suite parallel-worker load (different browser combination each
  run; 0 failures when the spec is run isolated). Verified pre-existing on `origin/main` and untouched by
  the Phase 2 diff. It is NOT a Phase 2 regression, so it was not fixed here.
  - **Why it might generalize**: a content/IA restructure that makes `ayokoding-www-fe-e2e` affected will
    drag the whole e2e suite — including unrelated load-flaky tool specs — into its CI gate, so a green
    Phase-2 deliverable can still show a red suite. Distinguish "my scenarios green + unrelated flake" from
    a real regression before gating on the aggregate exit code.
  - **Routing**: **Filed** as a new idea brief
    [`plans/ideas/ayokoding-www-e2e-parallel-load-flake.md`](../../ideas/ayokoding-www-e2e-parallel-load-flake.md)
    (code-homed test-infra ⇒ separate plan, never inline per the code-routing rule). Terminal.
- **Phase 2 — two delivery.md wording gaps for future plan-maker runs.** (1) The pure-rename proof step
  wrote `git diff --cached --summary -M -- <destination path>`, but git cannot pair a rename when the
  source side is excluded by a destination-only pathspec — the commit-level unscoped `git show --summary -M
<sha>` is the form that actually proves renames. (2) The §2.5 "legacy section-index browse still resolves"
  Gherkin assumed a standing legacy `_index.md` tree, but wholesale `git mv` of every child bundle + the
  Q-E root deletions leave no such tree; the acceptance text and the implementation reality diverged and had
  to be reconciled at execution time.
  - **Why it might generalize**: acceptance commands that scope a rename/diff to only one side of a move, or
    Gherkin that assumes a structure a later same-plan override removes, are internally inconsistent — the
    same class as the DD-49 body/validate contradiction above. plan-maker/plan-checker should flag pathspec-
    scoped rename proofs and cross-check later-resolved overrides against earlier acceptance prose.
  - **Routing**: **Folded** into [`plans/ideas/acceptance-clause-vacuity.md`](../../ideas/acceptance-clause-vacuity.md)
    as instances (b) rename-proof pathspec scoping and (c) later-override-vs-earlier-acceptance divergence
    of the "self-contradictory acceptance steps" sub-class. Terminal.

- **Phase 4 — the parallel-load e2e flake set widened to 3 scenarios under heavier concurrent load.**
  During Phase 4's full-suite `ayokoding-www-fe-e2e:test:e2e` run (while build/typecheck/lint/test:unit
  had also just run on the same shared machine), **3** scenarios failed:
  `course-rehome-redirects.feature` "resolves every re-homed course" (chromium),
  `ia-navigation-revamp.feature` "RSS feed item links use bare content URLs" (firefox), and the
  already-known `cost-of-living-calculator.feature` "minimum qualifying role" (firefox) — 575 passed /
  139 skipped otherwise. Re-running exactly those three isolated (`playwright test -g …`) passed **9/9**
  (3 scenarios × chromium/firefox/webkit). The committed tree is byte-identical to the `origin/main`
  that passed CI green at the Phase-3 merge (`git diff origin/main HEAD` empty), so none is a Phase-4
  regression — Phase 4 changed only `delivery.md`.
  - **Why it might generalize**: the pre-existing cost-of-living flake is not the only load-flaky spec —
    plan-relevant redirect/feed specs also flake under full-suite parallel-worker contention when the
    machine is loaded. The aggregate e2e exit code is unreliable on this shared machine; distinguish
    "isolated re-run passes" (flake) from a real regression before gating on it. Reinforces the Phase-2
    entry: the whole `ayokoding-www-fe-e2e` suite, not just the calculator, is load-sensitive here.
  - **Routing**: **Filed** into the same idea brief as the Phase-2 flake entry —
    [`plans/ideas/ayokoding-www-e2e-parallel-load-flake.md`](../../ideas/ayokoding-www-e2e-parallel-load-flake.md),
    whose scope covers the whole suite (all three identified load-flaky scenarios), not just the
    calculator spec. Terminal.

If execution completes and nothing generalizable surfaced, replace the entries above with the explicit
escape: `No generalizable learnings — <one-line reason>`. This file is never left silently empty.
