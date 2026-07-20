# Repo Rules Quality Gate — Bounded, Measurable Sweep Convergence

**Status**: Not Started
**Created**: 2026-07-20
**Delivery Mode**: `worktree-to-pr`

## Context

The [repo-rules-quality-gate workflow](../../../repo-governance/workflows/repo/repo-rules-quality-gate.md)
is the maker-checker-fixer loop that validates repository-wide governance consistency. Its stated
convergence expectation is **1-3 iterations, escalate after 5**
([Repo-grounded] — `repo-governance/development/pattern/maker-checker-fixer.md`
§Preventing Iteration Loops, verified present via `grep -c "converge in 1-3 iterations"` returning 1
and `grep -c "after 5 iterations"` returning 1). The workflow's own `max-iterations` frontmatter
defaults to **7** with an escalation warning at 5 [Repo-grounded].

On 2026-07-20 a real governance-change chain — inverting the plan merge default from `[HUMAN]` to
`[AI]` and hardening the merge preconditions — required **14 sequential checker rounds**, 13 of
which found genuine survivors. The first twelve distinct blind-spot classes below were all
discovered in the first thirteen rounds; the fourteenth found two further survivors
(`CONTRIBUTING.md` and a sibling plan's DN-11 note) but **no new class** — both were BS-12 misses,
in files no prior commit had ever touched.

A **second session**, running the PR-review maker→fixer cycle on the resulting PR, surfaced **three
further classes** (BS-13, BS-14, BS-15) plus the plan's central new finding: enumeration-based
guards fail open. Those classes were found by a mechanism no earlier round had used —
**completeness-diff against ground truth** — and none of them was reachable by text search at all.
The class list is therefore **fifteen**.

The corrective chain survives in git as twelve `fix(governance)` / `fix(docs)` commits,
`c23ae520b..c30ac344e`, touching **46 files** in union [Repo-grounded — verified via
`git log --format='%h|%s' 488148eca..c30ac344e` and `git diff --name-only … | wc -l`], plus a
thirteenth, `434430e0f` (`fix(plans): stop calling [HUMAN] merge the repo standard in DN-11`), which
the round-14 sweep produced after this plan's evidence range was first measured.

That chain is this plan's primary requirements input. It was not a low-quality chain — every round
found real, genuine stale text, and the resulting governance surface is correct because of it. The
problem is **terminability and measurability**, not rigor.

### Evidence provenance — the SHAs are branch-local and perishable

The twelve corrective commits live on the **unmerged branch**
`parallel-orchestration-shared-machine-governance` (tip `434430e0f`), **not** on `main`
[Repo-grounded — `git worktree list`; `git merge-base --is-ancestor c30ac344e origin/main` returns
non-zero; `main` and `origin/main` are both at `a207b66e7`].

This repo squash-merges PRs, so when that branch lands, **every SHA cited in this plan ceases to
resolve** in `main`'s history. The registry must therefore not depend on live SHA resolution — see
DECISION 8. Every registry entry embeds its evidence inline (commit subject plus the relevant file
list) so it stays auditable after the SHAs die, with the SHA retained only as a best-effort pointer.

## Diagnosis — the fifteen blind-spot classes, verified against git

Every round surfaced a **new blind-spot class** that the prior round's sweep had structurally
missed. Each row below maps to its corrective commit.

| #   | Blind-spot class                                            | Corrective commit | What the prior sweep missed                                                       |
| --- | ----------------------------------------------------------- | ----------------- | --------------------------------------------------------------------------------- |
| 1   | Fixed term order                                            | `c23ae520b`       | Table cells and reverse-order prose the fixed-order pattern never matched         |
| 2   | Scope limited to "the generative source"                    | `c23ae520b`       | Convention + checker + fixer siblings left stale after the source was fixed       |
| 3   | Bracketed-tag / plural assumption                           | `f071986db`       | Unbracketed phrasing — `human merge` without the `[HUMAN]` tag form               |
| 4   | Paraphrase                                                  | `39500d0a2`       | Text containing none of the search keywords ("Explicit user approval required")   |
| 5   | Teaching content vs normative passages                      | `f1b501b93`       | Explanatory prose still teaching the old default while the normative text was new |
| 6   | Untouched sections in already-partly-fixed files            | `817b015c6`       | Sections of files the sweep had already "handled"                                 |
| 7   | Worked examples contradicting the prose above them          | `3621f5932`       | Examples inconsistent with the paragraph directly preceding them                  |
| 8   | Agent-emitted templates hardcoding a value                  | `e4ba05266`       | Templates agents emit into plans, hardcoding the old default                      |
| 9   | Obligation-scoping keyed to the old condition               | `0c282a7d6`       | Obligations still conditioned on pushing to `main`                                |
| 10  | Definition blocks                                           | `d455f96dc`       | The TBD definition block itself, and the main-ci gate doc                         |
| 11  | Self-inflicted doc drift from the plan's OWN prior commits  | `362c23aab`       | Claims the chain's own earlier commits had just falsified                         |
| 12  | Directory-scoped sweep excluding `.github/`, `specs/`, root | `c30ac344e`       | A sweep that claimed "repo-wide" while never leaving `repo-governance/`           |

**BS-12 is provable from git and is the sharpest evidence of the first twelve.** Running
`git show --name-only` over each of the twelve commits shows `docs/` was first reached at commit 8
(`3812368a8`), and `.github/` and `specs/` were reached **only by the final commit** `c30ac344e`
[Repo-grounded]. Eleven rounds of sweeping, several described as repo-wide, never left a subtree.

### The three classes text search structurally cannot find (BS-13, BS-14, BS-15)

Discovered in the PR-review session that followed. Their common property is decisive: **none was
reachable by any text search, however well-phrased.** BS-13 has no swept phrasing to match; BS-14 has
no text and no inbound link at all; BS-15's ground truth is not a file on disk. All three were found
by enumerating ground truth and diffing it against the document claiming to describe it — the
**completeness-diff** mechanism (DECISION 11).

| #     | Blind-spot class                                              | Corrective commit | What every text-shaped sweep missed                                              |
| ----- | ------------------------------------------------------------- | ----------------- | -------------------------------------------------------------------------------- |
| BS-13 | Incomplete description that names no swept term               | `e46235226`       | A trigger stated as "Pull request" while the workflow also fires on `push: main` |
| BS-14 | Artifact exists on disk but appears in NO catalogue           | `b61e29754`       | A workflow file and an agent file present in the tree, absent from every index   |
| BS-15 | Safety rule scoped by an enumeration whose truth is a git ref | `3ee6323b7`       | Three live environment branches outside the enumeration the rule pointed at      |

**BS-13 — described without naming, phrased without the swept terms.** `.github/workflows/README.md`
stated `pr-quality-gate.yml`'s trigger as "Pull request", omitting `push: branches: [main]`
[Repo-grounded — the row is present in `.github/workflows/README.md` and the `push:` trigger is
present in `.github/workflows/pr-quality-gate.yml`, both re-verified during this amendment]. A
phrase sweep misses it because the row never says "push"; an inbound-link sweep misses it because
the row links nowhere. The only way to find it is to enumerate what a CI reference **should**
contain and diff that against `.github/workflows/`. The same class hit
`docs/reference/system-architecture/ci-cd.md` three times.

**BS-14 — the inverse, and harder: no text to match and no link to follow.**
`web-ui-build-deploy-prod.yml` was the only one of the 20 `.yml` workflow files absent from **both**
`.github/workflows/README.md` and `docs/reference/system-architecture/ci-cd.md` [Repo-grounded —
`command grep -c 'web-ui-build-deploy-prod' docs/reference/system-architecture/ci-cd.md .github/workflows/README.md`
returns 0 for both files, re-verified during this amendment]. Likewise
`.claude/agents/apps-web-ui-storybook-deployer.md` exists on disk while the `AGENTS.md` Operations
roster names only the six `*-www` / `*-app-web` deployers [Repo-grounded — re-verified during this
amendment]. There is nothing for a sweep to match on; only a filesystem enumeration diffed against
the catalogue finds it.

**BS-15 — the enumeration whose ground truth is a live git ref, not a file.** `AGENTS.md` scoped its
"never commit directly" safety rule to "`prod-*` per app, plus `stag-*`; the full list is in the Web
Sites table below". `git branch -r` shows **11** environment branches; the Web Sites table covers
**8** [Repo-grounded — re-verified during this amendment: `origin/prod-web-ui`,
`origin/stag-organiclever-be` and `origin/stag-ose-be` are absent from the table]. Three deploy
targets sat outside a rule whose entire purpose is protecting deploy targets, and one of them
(`prod-web-ui`) escaped the `prod-*`-per-app reasoning as well, because `web-ui` is a **lib**, not an
app — an agent force-pushes to it.

BS-15 is the first class whose ground truth is **not a file on disk**. BS-13 and BS-14 both diff
on-disk artifacts; nothing in this repo had ever been diffed against remote refs, and nothing
validates that enumeration.

### Classes compose — BS-15 is also an instance of BS-11

BS-15 was **self-inflicted**: an instruction-file byte-budget trim replaced an inline enumeration
with a pointer to a table that was not in fact complete. That makes it simultaneously an instance of
BS-11 (self-inflicted drift from the chain's own prior commits). The registry must therefore record
that **classes compose** — an entry is a lens, not a partition, and one defect can instantiate
several classes at once. A reader who treats the registry as mutually exclusive categories stops
looking after the first match.

### The central new finding — enumeration-based guards fail open

The PR-review cycle surfaced a **second convergence failure with the same shape as the sweep
problem**, and it is the most important thing this plan learned. Across the maker→fixer cycles on
PR #78, **four consecutive fixes each introduced the next defect**. Every guard was correct on the
axis it named and wide open on an axis nobody had named:

| Axis enumerated     | Guard said                        | Hole that opened next                                      |
| ------------------- | --------------------------------- | ---------------------------------------------------------- |
| 1. Tag value        | covers `[HUMAN]`                  | `[HUMAN → AI]` is a different literal                      |
| 2. Verb             | forbids **writing** `[AI]`        | says nothing about **deleting** the step                   |
| 3. Delivery mode    | scoped to `*-to-pr`               | other modes unguarded                                      |
| 4. Confidence       | scoped to the review path         | the HIGH-confidence auto-apply path unguarded              |
| 5. **Finding type** | umbrella claim: "no recipe, ever" | one recipe had no enforcement pointer, so it never arrives |

Axis 5 is the decisive one. `.claude/agents/plan-fixer.md`'s umbrella guard states that it binds "no
recipe in this file, present or future", and **on its own terms that is true**. But every
_enforcement pointer_ in that file is indexed by plan-checker **finding type**, and one recipe had
none: §Execution-Grade Clarity Fixes. That recipe fires on "checkbox lacks file path / verbatim
command / acceptance criterion", applies its rewrite **automatically at HIGH confidence**, and a step
reading `- [ ] [HUMAN] Merge PR once all preconditions hold` has none of the three. The recipe
derives a verbatim git command — `gh pr merge` — and once a step is a scripted git command, two other
rules push it toward `[AI]`. **A fixer entering the file on that finding type never reaches the
guard.** The `[HUMAN]` merge gate could be stripped by a rule about _missing file paths_, which never
mentions merging.

Two durable lessons follow, and both become first-class mechanisms here:

1. **A guard belongs at the point of rewrite, not in a section a fixer only reaches if it already
   suspected the hazard.** Enumerating axes failed four consecutive times; the fix is **placement**,
   not a longer enumeration. See DECISION 9.
2. **A guard is verified by enumerating how a fixer ENTERS the file** (by finding type, by step
   number) and checking that every entry path hits a guard before rewriting — **never** by reading
   what each section claims to cover. A section's self-description is exactly the artifact that was
   true and useless here.

This also generalizes the plan's existing ban on directory-scoped sweeps into something much larger:

> **The enumeration-fails-open rule.** Any safety property expressed as an enumeration fails open on
> the member nobody listed. Prefer properties expressed by what they **protect** (the human merge
> gate) over what they **enumerate** (tags, verbs, modes, confidence levels, finding types).

BS-12 (directory-scoped sweep), BS-15 (env-branch enumeration) and the five-axis guard sequence above
are three instances of that single rule.

### The convergence problem

A maker-checker-fixer loop over repo-wide governance **text** has no convergence guarantee and no
stopping rule. Unlike a compiler or a test suite, there is no finite oracle that says "no stale
phrasing remains." The loop terminates when the operator gets tired, not when the text is actually
consistent. The double-zero rule presumes the checker's search strategy is complete; the evidence
shows each round's strategy was incomplete in a **new** way.

This plan makes convergence **measurable and bounded** without weakening a single check.

## Techniques that worked — these become normative

Each was discovered mid-chain and each closed a class permanently once applied:

1. **Sweep by inbound link target, not by phrasing.** Link targets are stable where wording is not.
   Commit `39500d0a2` ("sweep by inbound link, catching the paraphrase survivors") is the proof:
   sweeping by who links to the governing doc caught survivors that no keyword search would.
2. **Diff the union of all corrective commits against the full file inventory** to find
   NEVER-TOUCHED candidate files. This is the mechanical detector for BS-12.
3. **Completeness-diff against ground truth.** Enumerate the ground truth — the filesystem,
   `git branch -r`, `.github/workflows/` — and diff it against the document claiming to describe it.
   This found BS-13, BS-14 **and** BS-15; text search found none of the three. It is promoted to a
   first-class mechanism alongside the inbound-link sweep, with the explicit warning that **ground
   truth is sometimes not a file on disk** (BS-15's was a set of remote refs). See DECISION 11.
4. **Verify doc claims about mechanical behavior against the actual workflow/hook/script files**,
   never against other docs. Commit `362c23aab` exists because a doc was trusted over the mechanism.
5. **Record the sweep command verbatim** so a reviewer can audit its scope. A claim of "repo-wide" is
   falsifiable only if the command is shown.
6. **Ban directory-scoped sweeps** unless the exclusions are enumerated and justified in the report.
7. **Adversarial framing**: a false "converged" verdict is the worst outcome — strictly worse than
   another round. The checker must argue against its own zero before accepting it.
8. **Adversarial framing must license a negative finding.** One reviewer was told "assume the
   previous fix introduced a defect", investigated, reported the **hypothesis wrong** — and found a
   real defect elsewhere in the same pass. A verification prompt that does not explicitly permit
   refuting the requester's hypothesis manufactures agreement instead of evidence. See DECISION 12.
9. **Prove the search tool works before trusting its zero.** A sweep whose conclusion is "nothing
   found" is evidence only if the command _could_ have produced a non-zero result. See DECISION 10.

## The false alarm — why validator-invocation parity is in scope

One round produced a **false alarm**. A bare `md mermaid validate` invocation flagged 4 violations
that were the validator's own deliberately-invalid negative fixtures. CI invokes the same validator
as:

```text
cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md mermaid validate --exclude apps/rhino-cli/tests/fixtures --exclude plans/done
```

[Repo-grounded — `.github/workflows/main-ci.yml:114`]. The bare form used in the round is the one
wired into `package.json` lint-staged [Repo-grounded — `package.json:88`], which carries neither
`--exclude`. Had the false alarm been trusted, it would have manufactured work **inside the
`apps/rhino-cli` byte-identity boundary** — a three-repo blast radius from a phantom defect.

So the gate must require that any validator invocation cited as evidence matches CI's exact flags,
or explicitly justifies the divergence.

## The tooling trap — a broken search command is indistinguishable from a clean result

In this environment `grep` resolves to **ugrep**, which **rejects ripgrep's `--glob`**. Combined
with `2>/dev/null`, a hard command failure looks exactly like a clean zero-result sweep. Measured
first-hand during this amendment, one pattern, one tree:

| Invocation                                                        | Result             |
| ----------------------------------------------------------------- | ------------------ |
| `grep -rn --glob '*.md' 'Trunk Based Development' . 2>/dev/null`  | **0 hits** (false) |
| `command grep -rn --include='*.md' 'Trunk Based Development' .`   | **543 hits**       |
| `/opt/homebrew/bin/rg -c --glob '*.md' 'Trunk Based Development'` | **147 files**      |

Zero and 543 are the same observation to a reader who only records the conclusion. Every "swept
repo-wide, found nothing" claim produced this way is worthless, and worse than worthless because it
is indistinguishable from a real zero.

A related trap of the same shape: `ls` output carries hyperlink escape sequences that eat leading
characters and silently corrupt a catalogue diff — precisely the diff BS-13/BS-14 detection depends
on. Use `find -print0`.

This becomes a normative rule (DECISION 10): **a sweep's zero is evidence only if the command could
have produced a non-zero result**, proven by a known-positive control probe.

## Approach

Nine mechanisms, ordered cheapest-first:

1. **Blind-Spot Class Registry (BSCR)** — a governance catalogue of the fifteen observed classes,
   each with its inline evidence, the sweep form that misses it, and the sweep form that catches it.
   Open for append, and explicit that **classes compose** rather than partition.
2. **Deterministic sweep-completeness validator** — `rhino-cli repo-governance sweep-completeness`,
   a zero-token mechanical pass computing the never-touched-candidate set and flagging
   directory-scoped sweeps with unenumerated exclusions.
3. **Inbound-link-target sweep as the primary method** — the checker and fixer sweep by who links to
   the changed governing document, with keyword search demoted to a secondary lens.
4. **Sweep transcript contract** — every sweep records its verbatim command and its exclusion set in
   the audit/fix report, making scope claims falsifiable.
5. **Evidence-grounding contract** — mechanical-behavior claims are verified against the mechanism
   file; validator invocations must match CI flags or justify divergence.
6. **Adversarial termination** — the checker must run one adversarial round arguing against its own
   zero, using the never-touched set, before `pass` is reported.
7. **Completeness-diff contract** — for any document that describes an enumerable ground truth,
   enumerate that ground truth and diff it against the document. Ground truth may be the filesystem,
   a set of git refs, or a directory listing; it is **not** necessarily a file on disk. Closes
   BS-13, BS-14 and BS-15, none of which any text search reaches. See DECISION 11.
8. **Guard placement contract** — a guard protecting an invariant is placed **at the point of
   rewrite**, and is verified by enumerating every entry path into the file rather than by reading
   what each section claims to cover. Closes the five-axis guard-hole sequence. See DECISION 9.
9. **Search-tool validity contract** — a sweep's zero counts as evidence only when the verbatim
   command is recorded, stderr is not suppressed, the tool is invoked in a form it accepts, and a
   known-positive control probe returns non-zero. See DECISION 10.

Mechanisms 2, 6 and 7 are the actual terminators. Mechanisms 1, 3, 4, 5, 8 and 9 reduce how much
work reaches them — and mechanism 9 is what keeps the others from reporting a fabricated zero.

## Scope

**In scope**:

- `repo-governance/workflows/repo/repo-rules-quality-gate.md` — step model, termination criteria
- New `repo-governance/development/quality/governance-sweep-blind-spots.md` — the BSCR
- `repo-governance/development/pattern/maker-checker-fixer.md` — the falsified 1-3 / escalate-at-5
  convergence claim, plus the sweep-methodology additions to §Preventing Iteration Loops
- `.claude/agents/repo-rules-checker.md`, `repo-rules-fixer.md`, `repo-rules-maker.md`
- `repo-governance/workflows/pr/pr-review-quality-gate.md` — the two termination gaps only
  (fix-committed-not-thread-resolved, and evidence-based rather than count-based cycles). See
  DECISION 13 for why these two are in scope and the third gap is not.
- `apps/rhino-cli` — the deterministic validator plus its Gherkin behavior tree
- Regeneration of `.opencode/` and `.amazonq/` via `npm run generate:bindings`
- Tri-repo propagation: `ose-public` (source of truth) → `ose-primer` → `ose-infra`

**Out of scope**:

- The governance change that supplied the evidence (the merge-default inversion) — it is evidence,
  not a target. This plan does not revisit it.
- The sibling `plan-quality-gate` loop — treated by
  [`plans/backlog/2026-07-20__plan-quality-gate-convergence/`](../2026-07-20__plan-quality-gate-convergence/README.md),
  which shares this plan's shape. Coordination is DECISION 6.
- The `repo-harness-compatibility-quality-gate` and `repo-workflow` gates — same shape, no evidence
  chain mined. DECISION 5.
- Any relaxation of an existing check, threshold, or criticality level. Explicitly forbidden.

## Navigation

- [brd.md](./brd.md) — why this matters
- [prd.md](./prd.md) — what gets built, with Gherkin acceptance criteria
- [tech-docs.md](./tech-docs.md) — architecture, design decisions, the BSCR seed, surface inventory
- [delivery.md](./delivery.md) — phased, gated checklist
- [learnings.md](./learnings.md) — Knowledge Capture running log

## Decisions taken without a grill (review before Phase 1)

This plan was authored without an interactive grill — the user was mid-session on another task. Each
decision below was made with stated reasoning and is genuinely open. Review each before Phase 1
begins; every one is reversible without restructuring the plan.

### DECISION 1 — Where does the deterministic sweep-completeness pass live?

- **A. `rhino-cli` validator, registered as a fifth `repo-governance audit` category** — **DECIDED**.
  Deterministic, zero-token, uniformly available to checker/fixer/maker, and it lands in the JSON
  envelope the checker already consumes at Step 0.5, so no new plumbing. Cost: `apps/rhino-cli` must
  stay byte-identical across all three repos per the
  [SDLC Gate Standard](../../../docs/reference/sdlc-gate-standard.md), adding a Gherkin behavior tree
  and tri-repo propagation weight.
- **B. A standalone script under `scripts/`** — far cheaper to land, no byte-identity constraint.
  Cost: not in the preflight envelope, so nothing guarantees it runs.
- **C. Prose-only obligation in the checker agent** — cheapest. Cost: the evidence chain shows
  precisely that self-imposed search discipline is what fails under budget pressure.

**Reasoning for A**: the never-touched-set computation is pure `git` arithmetic — exactly the kind of
mechanical predicate the
[Deterministic vs AI Validation Split Convention](../../../repo-governance/conventions/structure/deterministic-vs-ai-validation-split.md)
says should not consume AI tokens. Phase 2 is authored to be **separable**: dropping it degrades the
plan to mechanisms 1 and 3-6 with no other phase changing.

### DECISION 2 — Is the inbound-link sweep primary or merely recommended?

- **A. Primary, with keyword search demoted to a secondary lens** — **DECIDED**.
- **B. Co-equal with keyword search** — softer, but the evidence shows keyword-first sweeps produced
  classes 1, 3 and 4 directly.
- **C. Recommended only** — no behavioral change; rejected as insufficient.

**Reasoning for A**: commit `39500d0a2` is a controlled comparison — the inbound-link sweep caught
survivors that four prior keyword-shaped rounds had missed. Primacy is the finding, not a preference.

### DECISION 3 — How hard is the ban on directory-scoped sweeps?

- **A. Allowed only when exclusions are enumerated and justified in the report** — **DECIDED**.
- **B. Absolute ban** — every sweep must be repo-wide. Simple, but genuinely wasteful for a change
  whose blast radius really is one subtree, and it invites quiet non-compliance.
- **C. Advisory warning only** — rejected; class 12 cost a full round.

**Reasoning for A**: it preserves the cheap case while making the expensive failure mode visible. An
unenumerated exclusion becomes a mechanically detectable finding rather than a judgment call.

### DECISION 4 — What replaces the falsified "1-3 iterations, escalate after 5"?

- **A. Replace with a phased budget: a deterministic pass, a bounded semantic budget, and one
  adversarial round — plus the archived 13-round chain cited as the falsifying evidence** —
  **DECIDED**.
- **B. Raise the numbers to match observed reality (e.g. 10-15)** — honest, but treats the symptom;
  a bigger cap is not a stopping rule.
- **C. Delete the numeric claim entirely** — loses the reader's ability to tell whether a chain is
  going badly.

**Reasoning for A**: mirrors DD-7 of the sibling plan — correct the text and record why it changed,
so the next reader is not tempted to restore it.

### DECISION 5 — Do the sibling repo gates get the same treatment now?

- **A. Out of scope; file a follow-up backlog plan during Knowledge Capture** — **DECIDED**.
- **B. Fold `repo-harness-compatibility-quality-gate` and `repo-workflow-quality-gate` in now** — one
  propagation round instead of two, but triples the blast radius on zero evidence.
- **C. Do nothing until an equivalent evidence chain exists for each.**

**Reasoning for A**: the BSCR and the validator are gate-agnostic by construction, so adoption by the
sibling gates is later a link-and-reference edit, not a redesign.

### DECISION 6 — How does this plan coordinate with the sibling plan-quality-gate convergence plan?

- **A. Independent plans, independent PRs, shared registry vocabulary but separate registry files** —
  **DECIDED**. The sibling's registry catalogues _acceptance-clause_ traps (grep and CommonMark
  semantics); this one catalogues _sweep-completeness_ blind spots. Different failure domains, and
  merging them would produce one document serving two audiences badly.
- **B. One merged registry** — fewer files, but forces both plans into one PR and one merge order.
- **C. This plan waits for the sibling to land first** — serializes two independent efforts for no
  technical reason.

**Reasoning for A**: preserves the parallel-by-default posture (each plan gets its own worktree and
PR) and keeps each registry's audience coherent. The two registries cross-link.

### DECISION 8 — How does the registry survive the squash-merge that destroys its evidence SHAs?

Discovered while relocating this plan to the primary checkout: the evidence commits are branch-local
and this repo squash-merges, so the cited SHAs are perishable.

- **A. Embed the evidence inline in each registry entry — commit subject, the file list that proves
  the miss, and the sweep form — keeping the SHA only as a best-effort pointer** — **DECIDED**. The
  entry stays fully auditable when the SHA stops resolving, and a reader never has to reconstruct the
  chain from git.
- **B. Cite SHAs only** — smallest entries, but the registry becomes unverifiable the moment the
  branch merges, which is a self-inflicted instance of blind-spot class 11 (self-imposed drift).
- **C. Preserve the evidence by tagging the pre-merge commits** — keeps SHAs alive, but adds a
  permanent tag whose only purpose is propping up documentation, and tags are easy to prune later.
- **D. Land this plan's registry only after the evidence branch merges, citing post-merge SHAs** —
  serializes two independent efforts and still yields a single perishable squash SHA.

**Reasoning for A**: the registry's value is the _pattern_, not the commit. Inline evidence makes the
entry self-contained; the SHA is a convenience while it lasts. This also keeps the plan executable
regardless of whether the evidence branch has merged by then — which matters because the plan's own
worktree is provisioned from `origin/main`, where those SHAs are absent today. Delivery steps that
replay the chain must therefore resolve SHAs defensively and degrade to the inline evidence.

### DECISION 7 — Are the seed classes recorded verbatim, or generalized first?

- **A. Seeded verbatim with their git-commit proofs, then generalized in a "Sweep forms" summary
  table** — **DECIDED**. Concrete provenance is what makes a registry entry trustworthy; the summary
  table is what makes it usable.
- **B. Generalize into 4-5 abstract classes** — tidier, but discards the falsifiable evidence that
  makes each entry auditable.
- **C. Seed verbatim only** — usable as a checklist, poor as a teaching surface.

---

The five decisions below were added when the PR-review session's evidence was integrated. As with
the earlier eight, each was made without a grill, with stated reasoning, and each is reversible.

### DECISION 9 — How is a guard made to actually bind?

The five-axis guard-hole sequence (four consecutive fixes, each introducing the next defect) is the
evidence. The question is what generalizes from it.

- **A. Guard placement — the guard sits at the point of rewrite, and is verified by enumerating
  every entry path into the file** — **DECIDED**. Any recipe that rewrites a step hits the guard
  before rewriting, regardless of which finding type routed the fixer there. Verification enumerates
  entry paths (finding type, step number), never section self-descriptions.
- **B. Extend the axis enumeration** — add `[HUMAN → AI]`, deletion, all delivery modes, all
  confidence levels, all finding types. This is exactly what failed four consecutive times; each
  extension was correct and the next axis was still open.
- **C. Umbrella clause only** — "this guard binds every recipe, present or future". Already present
  in `plan-fixer.md`, already true on its own terms, and already useless: the fixer never reached
  the section that says it.
- **D. Both A and B** — belt and braces, but B's cost is unbounded (the axis set is not
  enumerable) and its presence invites the reader to believe the enumeration is the guard.

**Reasoning for A**: the failure was never that the enumeration was too short. It was that
enumeration is the wrong shape for the property. Placement is verifiable in finite work — the set of
entry paths into a file **is** enumerable, where the set of hazard axes is not. Stated as the
**enumeration-fails-open rule**: prefer a property expressed by what it protects over one expressed
by what it enumerates.

### DECISION 10 — What makes a sweep's zero admissible as evidence?

The measured ugrep/`--glob` trap turned a 543-hit query into a reported clean zero.

- **A. Record the verbatim command, forbid stderr suppression, require `--include` or
  `/opt/homebrew/bin/rg` by absolute path, and require a known-positive control probe** —
  **DECIDED**. The control probe is the load-bearing part: it proves the search tool works before
  its zero is trusted, and it is one extra command.
- **B. Mandate a specific tool** — e.g. always `/opt/homebrew/bin/rg`. Simpler, but brittle across
  machines and repos, and it does not detect the next tool-shaped failure.
- **C. Forbid `2>/dev/null` only** — the cheapest fix and it does address the specific observed
  trap, but a silent zero has other causes (wrong glob, wrong root, wrong case) that it misses.
- **D. Advisory note in the agent contracts** — no mechanical consequence; this is the class of
  self-imposed discipline the whole plan exists because it failed.

**Reasoning for A**: A subsumes C and generalizes past B. The control probe converts "the tool
returned nothing" into "the tool works **and** returned nothing", which is the actual claim being
made. It is also the only option under which a zero is falsifiable in both directions, which is the
acceptance-clause standard this plan's sibling installs.

### DECISION 11 — Is completeness-diff a first-class mechanism or a note under the sweep rules?

- **A. First-class mechanism, co-equal with the inbound-link sweep, with the explicit rider that
  ground truth is sometimes not a file on disk** — **DECIDED**.
- **B. A note under the existing never-touched computation** — cheaper, but the never-touched set is
  derived from links and commits, which is precisely the derivation BS-14 defeats (no link, no
  text). Filing it as a sub-note buries the one mechanism that found all three new classes.
- **C. Defer until a second chain confirms it** — the evidence is already three classes from one
  session, and each was invisible to every other mechanism in the plan.

**Reasoning for A**: the three new classes are one-third of the registry and were found by exactly
one mechanism, which no earlier round had used. The rider matters as much as the mechanism —
BS-15's ground truth was `git branch -r`, and a completeness-diff contract that silently assumes
on-disk artifacts reproduces BS-15 rather than catching it.

### DECISION 12 — Count-based or evidence-based cycle termination?

Three PR-review cycles ran; all three found blocking defects, and **two further verification passes
after cycle 3 each found another**.

- **A. Evidence-based: a cycle that finds nothing new terminates the loop; a cycle that finds
  something extends it** — **DECIDED**. This is the same critique the plan already makes of "1-3
  iterations, escalate at 5" (DECISION 4), applied to the review loop rather than the checker loop.
  Paired with the requirement that a verification prompt **licenses a negative finding**, so a
  no-new-findings cycle means "looked and found nothing" rather than "agreed with the requester".
- **B. Raise the default cycle count** — 3 to 5. Honest about the observed data, but a fixed count
  is the wrong shape of rule; five is as arbitrary as three and was already exceeded here.
- **C. Keep 3 and treat the overrun as an outlier** — the observed run had five consecutive
  productive passes. Calling that an outlier on one data point is the same over-confidence the plan
  is about.

**Reasoning for A**: consistency with DECISION 4 is not a stylistic preference here — both loops
failed the same way, so a plan that fixes one with an evidence-based rule and the other with a
bigger number is teaching two incompatible lessons from one body of evidence.

### DECISION 13 — Do the three PR-cycle process gaps belong in this plan?

Three gaps surfaced. They do not share a fix, so they do not share a disposition.

- **A. Take D1 and D3 in scope; file D2 as a follow-up** — **DECIDED**.
  - **D1 — "all threads resolved" ≠ "all findings fixed."** A fixer was told not to touch
    `AGENTS.md` (byte budget), correctly left the orchestrator's HIGH fix uncommitted in the working
    tree, replied to the thread and **resolved** it. GitHub showed 0 unresolved while the blocking
    defect was absent from the PR. **In scope**: this is a termination-criteria defect — a terminal
    verdict resting on a proxy signal instead of the property it stands for — which is this plan's
    subject exactly, and it is the same enumeration-fails-open shape (thread state enumerates
    conversations; the property to protect is "the fix is in the diff").
  - **D3 — the default 3 cycles was insufficient.** **In scope**: DECISION 12 above; it is the
    review-loop instance of DECISION 4's correction.
  - **D2 — `pr-review-maker` cannot post `REQUEST_CHANGES`.** `gh` authenticates as the PR author
    and GitHub rejects `REQUEST_CHANGES` on one's own PR, so reviews post as `COMMENT` with a
    blocking banner in the body. Anyone gating merge on GitHub's review **state** rather than the
    finding text reads the PR as unblocked. This is a real hole in the gate's enforcement, not
    cosmetic — but its fix is an authentication/tooling change (a separate token or bot identity, or
    a state-independent merge precondition), which shares no surface, no mechanism and no test with
    anything else in this plan. **Filed as a follow-up during Knowledge Capture.**
- **B. All three in scope** — one propagation round, but D2 drags token/identity configuration into
  a governance-text plan and its blast radius is the PR workflow for every plan in three repos.
- **C. All three filed as follow-ups** — keeps this plan tight, but D1 and D3 are literally this
  plan's thesis restated on a different loop; excluding them would leave the plan correcting
  termination in one place while a documented identical failure stands next to it.

**Reasoning for A**: the split is by fix-shape, not by convenience. D1 and D3 are termination-rule
text edits landing on surfaces this plan already opens (`maker-checker-fixer.md`, plus two narrow
edits to the PR-review workflow). D2 needs a credential decision this plan is not positioned to
make. Recording the reasoning matters more than the split itself — a future reader seeing D2 absent
should find why, not infer it was missed.
