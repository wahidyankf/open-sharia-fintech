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
which found genuine survivors. The twelve distinct blind-spot classes below were all discovered in
the first thirteen rounds; the fourteenth found two further survivors (`CONTRIBUTING.md` and a
sibling plan's DN-11 note) but **no new class** — both were class-12 misses, in files no prior
commit had ever touched. The class list is therefore twelve, not fourteen.

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

## Diagnosis — the twelve blind-spot classes, verified against git

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

**Class 12 is provable from git and is the sharpest evidence.** Running `git show --name-only` over
each of the twelve commits shows `docs/` was first reached at commit 8 (`3812368a8`), and
`.github/` and `specs/` were reached **only by the final commit** `c30ac344e` [Repo-grounded]. Eleven
rounds of sweeping, several described as repo-wide, never left a subtree.

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
   NEVER-TOUCHED candidate files. This is the mechanical detector for class 12.
3. **Verify doc claims about mechanical behavior against the actual workflow/hook/script files**,
   never against other docs. Commit `362c23aab` exists because a doc was trusted over the mechanism.
4. **Record the sweep command verbatim** so a reviewer can audit its scope. A claim of "repo-wide" is
   falsifiable only if the command is shown.
5. **Ban directory-scoped sweeps** unless the exclusions are enumerated and justified in the report.
6. **Adversarial framing**: a false "converged" verdict is the worst outcome — strictly worse than
   another round. The checker must argue against its own zero before accepting it.

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

## Approach

Six mechanisms, ordered cheapest-first:

1. **Blind-Spot Class Registry (BSCR)** — a governance catalogue of the twelve observed classes,
   each with its git-commit proof, the sweep form that misses it, and the sweep form that catches it.
   Open for append.
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

Mechanisms 2 and 6 are the actual terminators. Mechanisms 1, 3, 4 and 5 reduce how much work reaches
them.

## Scope

**In scope**:

- `repo-governance/workflows/repo/repo-rules-quality-gate.md` — step model, termination criteria
- New `repo-governance/development/quality/governance-sweep-blind-spots.md` — the BSCR
- `repo-governance/development/pattern/maker-checker-fixer.md` — the falsified 1-3 / escalate-at-5
  convergence claim, plus the sweep-methodology additions to §Preventing Iteration Loops
- `.claude/agents/repo-rules-checker.md`, `repo-rules-fixer.md`, `repo-rules-maker.md`
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

### DECISION 7 — Are the twelve classes seeded verbatim, or generalized first?

- **A. Seeded verbatim with their git-commit proofs, then generalized in a "Sweep forms" summary
  table** — **DECIDED**. Concrete provenance is what makes a registry entry trustworthy; the summary
  table is what makes it usable.
- **B. Generalize into 4-5 abstract classes** — tidier, but discards the falsifiable evidence that
  makes each entry auditable.
- **C. Seed verbatim only** — usable as a checklist, poor as a teaching surface.
