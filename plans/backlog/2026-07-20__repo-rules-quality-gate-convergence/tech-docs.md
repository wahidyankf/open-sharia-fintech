# Technical Documentation — Repo Rules Quality Gate Convergence

## Architecture

### Current loop (as built)

```mermaid
%% Current repo-rules-quality-gate loop — one search shape, one termination rule
flowchart LR
  A[rhino-cli preflight<br/>4 deterministic categories] --> B[repo-rules-checker<br/>AI semantic sweep]
  B --> C{threshold<br/>findings > 0?}
  C -- yes --> D[repo-rules-fixer<br/>instance-level fix]
  D --> A
  C -- no --> E{consecutive<br/>zeros >= 2?}
  E -- no --> B
  E -- yes --> F[pass]

  style A fill:#56B4E9,stroke:#04395E,color:#000000
  style B fill:#0072B2,stroke:#04395E,color:#FFFFFF
  style D fill:#D55E00,stroke:#7A3600,color:#FFFFFF
  style F fill:#009E73,stroke:#006147,color:#FFFFFF
```

The preflight already covers four mechanical categories, but **none of them measures sweep
completeness**. The AI checker picks its own search shape each round, and nothing records or
constrains that shape — so a zero means "this round's search found nothing", not "the text is
consistent".

### Target loop (this plan)

```mermaid
%% Target loop — sweep-completeness gate, transcript, and an adversarial round before pass
flowchart LR
  P[rhino-cli preflight<br/>+ sweep-completeness] --> Q{never-touched<br/>candidates > 0?}
  Q -- yes --> R[repo-rules-fixer<br/>class-wide sweep<br/>+ self-drift recheck]
  R --> P
  Q -- no --> S[repo-rules-checker<br/>inbound-link sweep<br/>+ transcript]
  S --> T{in-scope<br/>findings > 0?}
  T -- yes --> R
  T -- no --> U[adversarial round<br/>agenda = never-touched set]
  U --> V{adversarial<br/>zero?}
  V -- no --> R
  V -- yes --> W[pass]

  style P fill:#56B4E9,stroke:#04395E,color:#000000
  style S fill:#0072B2,stroke:#04395E,color:#FFFFFF
  style R fill:#D55E00,stroke:#7A3600,color:#FFFFFF
  style U fill:#CC79A7,stroke:#6B2F55,color:#000000
  style W fill:#009E73,stroke:#006147,color:#FFFFFF
```

### Sweep-set derivation

```mermaid
%% How the sweep set is built — stable keys first, phrasing second
flowchart TD
  G[changed governing document] --> H[inbound links:<br/>documents linking TO it]
  G --> I[outbound links:<br/>documents it links to]
  G --> J[declared blast radius:<br/>agents + workflows + skills<br/>naming the rule]
  H --> K[candidate set]
  I --> K
  J --> K
  K --> L[secondary lens:<br/>keyword phrasing search<br/>WITHIN the candidate set]
  K --> M[never-touched set =<br/>candidates minus<br/>corrective-commit union]

  style K fill:#0072B2,stroke:#04395E,color:#FFFFFF
  style M fill:#CC79A7,stroke:#6B2F55,color:#000000
```

The critical inversion: today keyword search **selects** the files, so any file whose wording differs
is invisible. In the target design, links and declared blast radius select the files, and keyword
search only ranks within that set.

### Lens sequencing across a round

```mermaid
%% Order of operations within one gate execution
sequenceDiagram
  participant O as Orchestrator
  participant D as rhino-cli (deterministic)
  participant C as repo-rules-checker
  participant F as repo-rules-fixer
  participant R as Blind-Spot Registry

  O->>D: repo-governance audit (incl. sweep-completeness)
  D->>D: compute candidate set and never-touched set
  D-->>O: mechanical findings (zero-token)
  alt never-touched candidates exist
    O->>F: class-wide sweep over the untouched candidates
    F->>F: re-check own change surface for self-inflicted drift
    F-->>O: fix report + sweep transcript
  else clean
    O->>C: semantic sweep over the candidate set
    C->>R: consult blind-spot classes
    C-->>O: findings + verbatim sweep transcript
  end
```

### Finding-evidence decision branch

```mermaid
%% How a claim becomes accepted evidence — the false-alarm path is explicit
flowchart TD
  E[claim under validation] --> G{claim about<br/>mechanical behavior?}
  G -- no --> N[normal semantic review]
  G -- yes --> H{verified against the<br/>implementing file?}
  H -- no --> X[reject as unverified<br/>doc-restating-doc]
  H -- yes --> I{evidence from a<br/>validator invocation?}
  I -- no --> OK[accept]
  I -- yes --> J{invocation matches<br/>CI flags?}
  J -- no --> K{divergence<br/>justified in report?}
  K -- no --> X
  K -- yes --> OK
  J -- yes --> OK

  style X fill:#D55E00,stroke:#7A3600,color:#FFFFFF
  style OK fill:#009E73,stroke:#006147,color:#FFFFFF
```

### Blind-spot lifecycle

```mermaid
%% A single stale passage's states from introduction to closure
stateDiagram-v2
  [*] --> Stale: rule changed
  Stale --> InCandidateSet: link sweep
  Stale --> Invisible: keyword miss
  Invisible --> InCandidateSet: stable key
  InCandidateSet --> ClassSwept: class swept
  ClassSwept --> ClosureVerified: no residue
  ClosureVerified --> [*]: closed
  ClosureVerified --> Stale: self-inflicted
```

Edge labels are kept short deliberately — `stateDiagram-v2` transition labels clip in GitHub's
renderer, and a clipped label is a silently wrong diagram. The full transitions read:

- **`[*] --> Stale`** — the governing rule changed somewhere else, stranding this passage.
- **`Stale --> InCandidateSet`** — selected by inbound-link sweep or blast-radius analysis.
- **`Stale --> Invisible`** — missed entirely by keyword-shaped search (BS-4, BS-13, BS-14).
- **`Invisible --> InCandidateSet`** — reached once a stable-key or completeness-diff sweep is adopted.
- **`InCandidateSet --> ClassSwept`** — the fixer sweeps the whole class, not the single instance.
- **`ClassSwept --> ClosureVerified`** — an adversarial round finds no residue.
- **`ClosureVerified --> Stale`** — the fixer's own commit falsified another claim.

The `ClosureVerified --> Stale` edge is blind-spot class 11 — the self-inflicted drift loop that
commit `362c23aab` had to close.

### Tri-repo propagation dependency

```mermaid
%% Propagation order — ose-public is the source of truth
flowchart LR
  A[ose-public<br/>Phases 1-6] --> B[ose-primer<br/>Phase 7]
  A --> C[ose-infra<br/>Phase 8]
  B -.byte-identity check.-> A
  C -.byte-identity check.-> A

  style A fill:#0072B2,stroke:#04395E,color:#FFFFFF
  style B fill:#56B4E9,stroke:#04395E,color:#000000
  style C fill:#56B4E9,stroke:#04395E,color:#000000
```

### Delivery phase flow

```mermaid
%% Phase progression with gates
flowchart LR
  P0[Phase 0<br/>baseline] --> P1[Phase 1<br/>registry]
  P1 --> P2[Phase 2<br/>validator]
  P1 --> P3[Phase 3<br/>sweep contracts]
  P2 --> P4[Phase 4<br/>evidence grounding]
  P3 --> P4
  P4 --> P5[Phase 5<br/>adversarial termination]
  P5 --> P5B[Phase 5B<br/>guard placement +<br/>search validity +<br/>cycle termination]
  P5B --> P6[Phase 6<br/>replay + bindings + PR]
  P6 --> P7[Phase 7<br/>ose-primer]
  P6 --> P8[Phase 8<br/>ose-infra]
  P7 --> P9[Phase 9<br/>knowledge capture]
  P8 --> P9

  style P0 fill:#009E73,stroke:#006147,color:#FFFFFF
  style P5B fill:#E69F00,stroke:#7A5200,color:#000000
  style P6 fill:#0072B2,stroke:#04395E,color:#FFFFFF
  style P9 fill:#CC79A7,stroke:#6B2F55,color:#000000
```

Phases 2 and 3 are independent of each other and may run in parallel (subject to the repo's
concurrency cap); Phases 7 and 8 likewise. Phase 5B carries the three mechanisms added from the
PR-review session (DECISIONs 9, 10, 12 and 13) and depends on Phase 5's termination rewrite.

## Blind-Spot Class Registry — seed content

The registry lands at `repo-governance/development/quality/governance-sweep-blind-spots.md`
[Repo-grounded — verified absent via `test -f` on `main` during authoring].

**Evidence durability (DECISION 8)**: each entry embeds its evidence inline — the commit subject and
the file list proving the miss — because the cited SHAs live on the unmerged branch
`parallel-orchestration-shared-machine-governance` and will not survive a squash-merge. The SHA is a
best-effort pointer, never the sole evidence.

**Classes compose, they do not partition.** BS-15 is simultaneously an instance of BS-11: it was
introduced by an instruction-file byte-budget trim that replaced an inline enumeration with a
pointer to an incomplete table. The registry states this explicitly, because a reader who treats
entries as mutually exclusive categories stops matching after the first hit.

### The fifteen seed classes

| ID    | Blind spot                            | Missing sweep form                                    | Catching sweep form                                             | Evidence (commit subject)                                        |
| ----- | ------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------- |
| BS-1  | Fixed term order                      | Ordered multi-term pattern                            | Order-independent alternation; inspect table cells separately   | `sweep stale direct-push-default boilerplate to all four copies` |
| BS-2  | Generative-source-only scope          | Edit the doc that generated the rule                  | Include convention + checker + fixer + maker siblings           | `sweep stale direct-push-default boilerplate to all four copies` |
| BS-3  | Bracketed-tag / plural assumption     | Search the tagged form `[HUMAN]` only                 | Search the untagged prose form too (`human merge`)              | `close the unbracketed "human merge" sweep gap`                  |
| BS-4  | Paraphrase                            | Any keyword-selected search                           | Inbound-link sweep — select by link, not by wording             | `sweep by inbound link, catching the paraphrase survivors`       |
| BS-5  | Teaching vs normative content         | Sweep only normative sections                         | Include explanatory/teaching prose in the candidate set         | `rewrite the teaching content that still taught main-by-default` |
| BS-6  | Untouched sections in touched files   | Treat a file as done once edited                      | Re-scan the whole file, not the edited region                   | `rewrite the untouched teaching sections in partly-fixed files`  |
| BS-7  | Worked examples contradicting prose   | Sweep prose only                                      | Diff each example against the paragraph governing it            | `align worked examples with the prose above them`                |
| BS-8  | Agent-emitted templates               | Sweep documentation only                              | Include templates agents emit into other artifacts              | `make post-push CI templates delivery-mode-aware`                |
| BS-9  | Obligation scoped to old condition    | Search the changed value                              | Search the **condition** the obligation is keyed on             | `scope CI post-push verification to the delivery target`         |
| BS-10 | Definition blocks                     | Sweep usage sites                                     | Include the definition/glossary blocks defining the term        | `correct the TBD definition block and the main-ci gate doc`      |
| BS-11 | Self-inflicted drift                  | Sweep only pre-existing content                       | Re-check the chain's own change surface for claims it falsified | `correct nx-targets CI-trigger claims for main-ci schedule`      |
| BS-12 | Directory-scoped sweep                | `grep -r … repo-governance/` while claiming repo-wide | Repo-wide, or enumerate + justify every exclusion               | `correct main-ci trigger docs outside repo-governance`           |
| BS-13 | Incomplete description, no swept term | Any phrase sweep; any inbound-link sweep              | Completeness-diff: enumerate what the reference should contain  | `correct the pr-quality-gate trigger description`                |
| BS-14 | Artifact on disk, in no catalogue     | Any text or link sweep — there is no text and no link | Completeness-diff: enumerate the filesystem, diff the catalogue | `catalogue the missing workflow and storybook deployer`          |
| BS-15 | Enumeration whose truth is a git ref  | Any sweep of on-disk artifacts                        | Completeness-diff against `git branch -r`                       | `cover the three uncovered environment branches`                 |

### BS-13, BS-14, BS-15 — the classes no text search reaches

These three share the property that makes them the registry's most important entries: **there is
nothing to search for.** BS-13's text omits the swept term rather than containing a stale one;
BS-14's artifact has neither text nor inbound link; BS-15's ground truth is not in the tree at all.
Every mechanism in this plan other than completeness-diff (DD-10) finds zero of the three.

**BS-13 — incomplete description that names no swept term.** `.github/workflows/README.md` stated
`pr-quality-gate.yml`'s trigger as "Pull request" while the workflow also carries
`push: branches: [main]`. **Inline evidence**: the corrective commit
`correct the pr-quality-gate trigger description`; the proving pair is the "PR and repo-wide gates"
table row in `.github/workflows/README.md` against the `on:` block of
`.github/workflows/pr-quality-gate.yml` [Repo-grounded — both re-verified during the amendment that
added this entry]. The same class hit `docs/reference/system-architecture/ci-cd.md` three times.
**Missing form**: phrase sweep (the row never says "push"); inbound-link sweep (the row links
nowhere). **Catching form**: enumerate what a CI reference should contain — every trigger of every
workflow — and diff against `.github/workflows/`. **Detection**: statically detectable, given a
parser for workflow `on:` blocks.

**BS-14 — the artifact that appears in no catalogue.** **Inline evidence**: the corrective commit
`catalogue the missing workflow and storybook deployer`. `web-ui-build-deploy-prod.yml` was the only
one of the 20 `.yml` files under `.github/workflows/` absent from **both**
`.github/workflows/README.md` and `docs/reference/system-architecture/ci-cd.md`;
`.claude/agents/apps-web-ui-storybook-deployer.md` exists while the `AGENTS.md` Operations roster
names only the six `*-www` / `*-app-web` deployers [Repo-grounded — both re-verified during this
amendment]. **Missing form**: every text- or link-shaped sweep; the artifact is absent from the
documentation by definition, so there is no occurrence to match and no link to follow.
**Catching form**: enumerate the filesystem with `find -print0` and diff against the catalogue.
**Detection**: statically detectable, and the cheapest of the three.

**BS-15 — the enumeration whose ground truth is a live git ref.** **Inline evidence**: the
corrective commit `cover the three uncovered environment branches`. `AGENTS.md` scoped its "never
commit directly" rule to "`prod-*` per app, plus `stag-*`; the full list is in the Web Sites table
below". `git branch -r` shows 11 environment branches against the table's 8; `origin/prod-web-ui`,
`origin/stag-organiclever-be` and `origin/stag-ose-be` were uncovered [Repo-grounded — re-verified
during this amendment]. `prod-web-ui` escaped the `prod-*`-per-app reasoning as well, because
`web-ui` is a **lib**, not an app — and an agent force-pushes to it. **Missing form**: any sweep of
on-disk artifacts; the ground truth is a set of remote refs. **Catching form**: completeness-diff
against `git branch -r`. **Detection**: statically detectable, but only by a check that knows to
consult refs rather than files — which is the entire point of DD-10's rider.

**Composition note**: BS-15 is also a BS-11 instance. It was self-inflicted by a byte-budget trim
replacing an inline enumeration with a pointer to an incomplete table — the chain's own change
falsifying the chain's own safety scope.

### BS-12 — worked entry (the highest-cost class of the first twelve)

**Symptom**: a sweep restricted to one subtree, reported as repo-wide. Eleven consecutive rounds
asserted repo-wide scope without demonstrating it.

**Inline evidence** (survives SHA loss): the final corrective commit
`correct main-ci trigger docs outside repo-governance` was the **first** in a twelve-commit chain to
touch any of:

```text
.github/workflows/README.md
specs/apps/ayokoding/containers/container.md
specs/apps/organiclever/containers/container.md
```

`docs/` was first reached only at the eighth commit (`scope CI post-push verification to the delivery
target` / `correct the TBD definition block…`). The union of all twelve commits touches 46 files
[Repo-grounded — `git diff --name-only 488148eca..c30ac344e | wc -l` returns 46].

**Missing form**: a recursive search rooted at `repo-governance/`.

**Catching form**: repo-wide search, or a search whose exclusions are enumerated as literal globs and
justified in the report.

**Detection**: statically detectable — a recorded sweep command whose root is a subdirectory, or
whose exclusion set is non-empty and unjustified.

### BS-4 — worked entry (the controlled comparison)

**Symptom**: stale text containing none of the search keywords. The observed instance read
"Explicit user approval required" — no occurrence of the changed tag, the changed default, or any
term a reasonable keyword sweep would have chosen.

**Inline evidence**: commit `sweep by inbound link, catching the paraphrase survivors` — the first
round to select files by inbound link rather than by phrasing, and it found survivors that four
prior keyword-shaped rounds had missed. This is the single controlled comparison in the chain and is
the basis of DECISION 2.

**Missing form**: any search that selects candidate files by matching their text.

**Catching form**: enumerate documents linking to the changed governing document; sweep all of them
regardless of wording.

**Detection**: partially static — the validator can verify the inbound-link set was enumerated;
whether a given passage is stale stays an AI judgement.

## Design Decisions

### DD-1 — the registry is a governance quality document, not agent-inlined prose

Inlining fifteen class descriptions with evidence into `repo-rules-checker.md`, `repo-rules-fixer.md`
and `repo-rules-maker.md` would triple their content and push against the instruction-file size
budget [Repo-grounded — `nx run rhino-cli:instruction-size:validation` exists and is wired into the
preflight as the `instruction-size` category]. One governance file that all three link to keeps a
single source of truth and one place to append class thirteen.

### DD-2 — the deterministic pass is a fifth `repo-governance audit` category

The orchestrator today runs exactly four categories — `layer-coherence`, `traceability-audit`,
`vendor-audit`, `instruction-size` [Repo-grounded — `repo-rules-quality-gate.md` Step 0.5]. Adding
`sweep-completeness` as a fifth means the checker consumes it through the Step 0.5 JSON envelope it
already parses, with no new plumbing and no new invocation for an agent to skip.

Cost: `apps/rhino-cli` must stay byte-identical across all three repos per the
[SDLC Gate Standard](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary),
so this adds a Gherkin behavior tree under `specs/apps/rhino/behavior/rhino-cli/gherkin/` and
tri-repo propagation weight. This is the plan's largest reversible commitment (DECISION 1); Phase 2
is authored to be separable — dropping it degrades the plan to mechanisms 1 and 3-6 without
restructuring any other phase.

### DD-3 — the candidate set is bounded by links and declared blast radius

A naive never-touched set would be "every file in the repo", which is useless. The candidate set is:

1. every document with an **inbound link** to the changed governing document;
2. every document the changed document **links out** to;
3. the **declared blast radius** — agents, workflows and skills naming the changed rule.

The never-touched set is the candidate set minus the union of the chain's corrective commits. This
keeps the adversarial round's agenda finite and relevant, which is what stops it degenerating into
free-form doubt (a named product risk).

### DD-4 — sweep transcript over sweep assertion

The workflow cannot verify a sweep it cannot see. Recording the verbatim command plus the exclusion
set converts an unfalsifiable claim into a checkable one, and costs one line in a report. This is the
cheapest mechanism in the plan and closes BS-12 even without the validator.

### DD-5 — evidence grounding has two rules, not one

Rule A: a claim about mechanical behavior is verified against the **implementing** file (workflow,
hook, script), never against another document restating it. Closes BS-11.

Rule B: a validator invocation cited as evidence must match **CI's exact flags**, or record a written
justification for diverging. Closes the observed false alarm, where a bare `md mermaid validate`
flagged the validator's own negative fixtures. CI invokes it with
`--exclude apps/rhino-cli/tests/fixtures --exclude plans/done`, while the `package.json` lint-staged
entry uses the bare form [Repo-grounded — both verified on `main` during authoring]. The two rules
ship together because both failures are "trusted the wrong artifact as evidence".

### DD-6 — termination is adversarial, not merely repeated

Two consecutive zeros from the same search shape is one observation repeated, not two observations.
The adversarial round changes the shape: its agenda is the mechanically derived never-touched set,
so it interrogates exactly the region the semantic rounds structurally could not see. An empty
agenda is reported explicitly (AC-13) so that "nothing to challenge" is distinguishable from "the
computation never ran".

### DD-7 — the falsified convergence claim is corrected, not deleted

`maker-checker-fixer.md` §Preventing Iteration Loops claims convergence in 1-3 iterations with
escalation after 5 [Repo-grounded — both phrases verified present on `main`]. The archived chain ran 13. The text is rewritten to describe the phased budget and cite the falsifying chain, rather than
silently dropped, so the next reader understands why the number changed and does not restore it.

### DD-8 — evidence is embedded inline because the SHAs are perishable

See README DECISION 8. The evidence commits are branch-local and this repo squash-merges, so SHA
citations die on merge. Each registry entry carries its commit subject and proving file list inline.
Delivery steps that replay the chain resolve SHAs **defensively** — if `git cat-file -t <sha>` fails,
the step falls back to the inline evidence rather than failing the phase.

The BS-13/BS-14/BS-15 SHAs (`e46235226`, `b61e29754`, `3ee6323b7`, `f5f819642`, `72af8ab83`) are on
the same unmerged branch and are equally perishable. Their entries above carry inline evidence that
is re-derivable from the current tree at any time — a `find` over `.github/workflows/`, a `grep`
over the two catalogues, and `git branch -r` — which makes them the most durable entries in the
registry, not the least.

### DD-9 — a guard is placed at the point of rewrite, not enumerated by hazard axis

The evidence is the five-axis sequence in README DECISION 9: four consecutive fixes, each correct on
the axis it named, each opening the next. The decisive instance is structural rather than a matter
of wording. `.claude/agents/plan-fixer.md` carries an umbrella guard claiming to bind "no recipe in
this file, present or future" — a claim that is **true on its own terms**. But every _enforcement
pointer_ in that file is indexed by plan-checker **finding type**, and §Execution-Grade Clarity
Fixes has none. That recipe fires on "checkbox lacks file path / verbatim command / acceptance
criterion", auto-applies at HIGH confidence, and a step reading
`- [ ] [HUMAN] Merge PR once all preconditions hold` has none of the three. It derives a verbatim
command — `gh pr merge` — after which two other rules push the step toward `[AI]`. A fixer entering
on that finding type never reaches the guard.

Two rules follow:

- **Placement**: a guard protecting an invariant is co-located with every rewrite that could violate
  it. The umbrella clause may remain, but it is documentation, never the mechanism.
- **Verification by entry path**: coverage is established by enumerating how an agent **enters** the
  file — finding type, step number, invocation mode — and tracing each path to the guard. A
  section's self-description is not evidence; in the observed case it was accurate and irrelevant.

Why not simply extend the axis enumeration: the entry-path set is finite and enumerable; the hazard-
axis set is neither. This is the **enumeration-fails-open rule** — prefer a property expressed by
what it protects over one expressed by what it enumerates — of which BS-12 and BS-15 are two further
instances.

### DD-10 — completeness-diff is a first-class mechanism, and ground truth is not always a file

The never-touched computation (DD-3) derives its candidate set from links and commits. BS-14 defeats
that derivation by construction: an artifact absent from every catalogue has no inbound link and no
matchable text, so it is never a candidate. Completeness-diff inverts the direction — enumerate the
**ground truth**, then diff the document that claims to describe it.

Three ground-truth sources are in evidence:

| Ground truth             | Enumerated by                                | Class caught |
| ------------------------ | -------------------------------------------- | ------------ |
| Workflow triggers        | parsing `on:` blocks in `.github/workflows/` | BS-13        |
| Workflow and agent files | `find .github/workflows -type f -print0`     | BS-14        |
| Environment branches     | `git branch -r`                              | BS-15        |

The third is the rider that matters most: **ground truth is sometimes not a file on disk**. A
completeness-diff contract that silently assumes on-disk artifacts reproduces BS-15 rather than
catching it. Every instance of the contract therefore names its authoritative source explicitly, and
an unnamed source is itself a finding (AC-20).

Tooling note carried from DD-11: catalogue diffs use `find -print0`, never parsed `ls` output —
`ls` emits hyperlink escape sequences that eat leading characters and silently corrupt exactly the
diff this mechanism depends on.

### DD-11 — a sweep's zero is admissible only with a working-tool proof

In this environment `grep` resolves to **ugrep**, which rejects ripgrep's `--glob`. With
`2>/dev/null` appended, a hard failure and a clean sweep are the same observation. Measured
first-hand on one pattern in one tree during this amendment:

| Invocation                                                        | Result             |
| ----------------------------------------------------------------- | ------------------ |
| `grep -rn --glob '*.md' 'Trunk Based Development' . 2>/dev/null`  | 0 hits — **false** |
| `command grep -rn --include='*.md' 'Trunk Based Development' .`   | 543 hits           |
| `/opt/homebrew/bin/rg -c --glob '*.md' 'Trunk Based Development'` | 147 files          |

The contract has four parts, all cheap:

1. the **verbatim command** is recorded in the report;
2. **stderr is not suppressed** — no `2>/dev/null` on an evidence-producing sweep;
3. the invocation uses a form the tool accepts — POSIX `--include`, or
   `/opt/homebrew/bin/rg` **by absolute path**;
4. a **known-positive control probe** runs the same pattern against a file known to contain it and
   returns non-zero, before the zero is trusted.

Part 4 is load-bearing. Parts 1-3 address the observed failure; part 4 addresses the next one,
whatever shape it takes, by converting "the tool returned nothing" into "the tool works **and**
returned nothing". It is also what makes a zero falsifiable in both directions, which is the
acceptance-clause standard the sibling plan installs.

### DD-12 — review-cycle termination is evidence-based, mirroring DD-6

The PR-review cycle defaults to three sequential maker→fixer cycles. In the observed run **all three
found blocking defects, and two further verification passes after cycle 3 each found another** — the
loop was still productive when arithmetic declared it done. This is DD-7's falsified "1-3
iterations, escalate at 5" claim reappearing on a different loop, so it takes the same correction
rather than a larger constant:

- a cycle producing any **new** blocking finding extends the loop;
- termination requires a cycle producing **no new** finding (repeat findings do not extend it);
- the verification prompt for each cycle must **license a negative finding** — explicitly permitting
  the reviewer to refute the requester's hypothesis. In the observed run, one reviewer told to
  "assume the previous fix introduced a defect" investigated, reported the hypothesis **wrong**, and
  found a real defect elsewhere in the same pass. A prompt without that license manufactures
  agreement, and a loop terminating on manufactured agreement is worse than one terminating on a
  count.

### DD-13 — the three PR-cycle process gaps split by fix-shape

Full reasoning in README DECISION 13. Summary of the split and its rationale:

| Gap                                                  | Disposition        | Why                                                                                       |
| ---------------------------------------------------- | ------------------ | ----------------------------------------------------------------------------------------- |
| D1 — resolved threads ≠ committed fixes              | **In scope**       | A terminal verdict resting on a proxy signal; same shape as enumeration-fails-open (DD-9) |
| D3 — fixed cycle count insufficient                  | **In scope**       | The review-loop instance of DD-7 / DD-6; DD-12 above                                      |
| D2 — `pr-review-maker` cannot post `REQUEST_CHANGES` | **Follow-up plan** | Fix is a token/identity change; shares no surface, mechanism or test with this plan       |

D1's mechanism is worth stating precisely, because the failure was a **correct** action producing a
wrong aggregate signal. A fixer was instructed not to touch `AGENTS.md` (instruction-size budget),
so it correctly left the orchestrator's HIGH fix uncommitted in the working tree, replied to the
thread explaining why, and resolved it. GitHub then reported 0 unresolved threads while the blocking
defect was absent from the PR. The remedy is to gate merge on the property rather than the proxy:
**every finding's fix is committed and pushed**, verified against the diff, never inferred from
thread state.

D2 is left unfixed here deliberately, and until its follow-up lands the mitigation is that merge
preconditions gate on **finding text**, never on GitHub's review state — which is already what
AC-26 requires.

## UI-Design-Funnel Exemption

This plan is **not UI-bearing**. It changes governance markdown, agent definitions, and a CLI
validator that emits text to stdout. It adds and changes no user-facing screen or component under
`apps/` or `libs/` that renders to an end user. Per the
[UI Mockups in Plan Docs convention](../../../repo-governance/conventions/formatting/diagrams.md#ui-mockups-in-plan-docs),
the design funnel does not apply, and this paragraph is the explicit exemption record.

## Testing Strategy

| Mechanism                  | Test level                | How the Gherkin binds                                                                 |
| -------------------------- | ------------------------- | ------------------------------------------------------------------------------------- |
| Registry entries           | Inline-evidence review    | AC-1, AC-2 — each entry's proving file list is checked against the inline evidence    |
| Never-touched computation  | Rust unit + Gherkin specs | AC-3 — RED tests against fixture repo states with known candidate and touched sets    |
| Directory-scope detection  | Rust unit + Gherkin specs | AC-4 — RED tests against sweep-report fixtures with and without enumerated exclusions |
| Agent contract text        | Grep-based gate checks    | AC-5 through AC-11 — presence and shape verified mechanically, semantics by review    |
| Adversarial termination    | Workflow text + review    | AC-12, AC-13 — termination criteria read and verified                                 |
| Convergence-claim removal  | Grep both directions      | AC-14 — phrase present pre-edit (returns 1), absent post-edit (returns 0)             |
| No-check-removed invariant | Inventory diff            | AC-15 — Phase 0 records the baseline inventory; Phase 6 compares                      |
| Bindings + byte identity   | Existing repo validators  | AC-16, AC-17 — `npm run generate:bindings`, harness sync validation, byte-identity    |
| Registry BS-13/14/15       | Inline-evidence replay    | AC-18, AC-19 — each entry's evidence re-derived from the tree, never from a live SHA  |
| Completeness-diff contract | Rust unit + Gherkin specs | AC-20, AC-21 — RED tests over catalogue fixtures and a git-ref fixture                |
| Guard placement            | Entry-path enumeration    | AC-22, AC-23 — every entry path traced to the guard; one bypass falsifies coverage    |
| Search-tool validity       | Control-probe fixtures    | AC-24 — broken and working invocations both exercised; a zero without a probe fails   |
| Review-cycle termination   | Workflow text + review    | AC-25, AC-26 — termination criteria and merge preconditions read and verified         |

Per [Test-Driven Development](../../../repo-governance/development/workflow/test-driven-development.md),
the validator's tests are written before its implementation; each RED step in
[delivery.md](./delivery.md) carries exactly one bound scenario.

## Surface Inventory

| #   | Surface                                                                  | Change                                                          | Grounding                    |
| --- | ------------------------------------------------------------------------ | --------------------------------------------------------------- | ---------------------------- |
| 1   | `repo-governance/development/quality/governance-sweep-blind-spots.md`    | **Create** — the BSCR                                           | [Repo-grounded] absent today |
| 2   | `repo-governance/workflows/repo/repo-rules-quality-gate.md`              | Step model, termination criteria, adversarial round             | [Repo-grounded] exists       |
| 3   | `repo-governance/development/pattern/maker-checker-fixer.md`             | Corrected convergence guidance; sweep methodology               | [Repo-grounded] exists       |
| 4   | `.claude/agents/repo-rules-checker.md`                                   | Inbound-link sweep, transcript, evidence grounding, adversarial | [Repo-grounded] exists       |
| 5   | `.claude/agents/repo-rules-fixer.md`                                     | Class-wide sweep, self-drift recheck, transcript                | [Repo-grounded] exists       |
| 6   | `.claude/agents/repo-rules-maker.md`                                     | BSCR link; start propagation from the inbound-link set          | [Repo-grounded] exists       |
| 7   | `apps/rhino-cli/src/commands/governance_sweep_completeness.rs`           | **Create** — the validator                                      | [Repo-grounded] dir exists   |
| 8   | `apps/rhino-cli/src/cli.rs`, `commands.rs`, `governance_audit.rs`        | Register the fifth audit category                               | [Repo-grounded] all exist    |
| 9   | `specs/apps/rhino/behavior/rhino-cli/gherkin/repo-governance/`           | **Create** — `repo-governance-sweep-completeness.feature`       | [Repo-grounded] dir exists   |
| 10  | `repo-governance/development/quality/README.md`, `development/README.md` | Register the new convention in the index tables                 | [Repo-grounded] exist        |
| 11  | `.opencode/`, `.amazonq/`                                                | **Regenerated only** — never hand-edited                        | Generated artifacts          |
| 12  | `repo-governance/workflows/pr/pr-review-quality-gate.md`                 | Evidence-based cycle termination; committed-fix precondition    | [Repo-grounded] exists       |
| 13  | `ose-primer`, `ose-infra`                                                | Propagation of surfaces 1-10 and 12                             | Sibling repos                |

## Dependencies

- `npm run generate:bindings` — regenerates `.opencode/` and `.amazonq/` from `.claude/`
- `npx nx affected -t typecheck lint test:quick specs:coverage` — the standing quality gate
- `cargo` via the existing rhino-cli Nx targets — validator build and test
- `git` plumbing (`git log`, `git diff --name-only`, `git cat-file`) — never-touched computation
- `gh` CLI — PR creation and the review cycle

## Rollback

Every surface is additive or text-level. Rollback is `git revert` of the phase PR. The validator is
introduced advisory-first — it reports findings into the existing preflight envelope, which the
workflow's Step 2 already treats as visibility-only and never counts toward the mode threshold
[Repo-grounded — `repo-rules-quality-gate.md` Step 2]. A defective validator therefore degrades to
noise rather than to a blocked gate. The registry is inert data. No migration, no persisted state, no
schema change.
