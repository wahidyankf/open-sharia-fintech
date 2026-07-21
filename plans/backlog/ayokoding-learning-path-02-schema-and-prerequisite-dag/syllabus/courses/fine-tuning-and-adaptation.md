# Fine-Tuning & Adaptation (By Example, Python)

**Course ID**: `fine-tuning-and-adaptation` · **Format**: By Example · **Language**: Python. **NEW** —
`fine-tun` appears exactly once library-wide today, as a foil for RAG in
[`creating-ai-powered-apps`](./creating-ai-powered-apps.md); nothing teaches the technique itself.

**Scope note**: adapting a model's weights to a task — **supervised fine-tuning** on
instruction/response pairs, **parameter-efficient fine-tuning** with low-rank adapters (the LoRA family),
**dataset curation** as the activity that actually determines the outcome, **evaluation of an adapted
model** against the base it must beat, **distillation** of a large model's behaviour into a smaller one,
and **deployment of adapters** alongside the serving stack. The course is framed around a question it
takes seriously in both directions: **when to fine-tune and, far more often, when to avoid it.**

> **Deliberate de-emphasis — read this before the syllabus.** Chip Huyen's production-AI framing treats
> fine-tuning as deliberately de-emphasized for application engineers — the discipline is knowing **when
> to do it and when to avoid it**, not treating weight adaptation as the default response to a quality
> problem. This course adopts that framing as its structure rather than reporting it as an aside. The
> first band is **not** how to fine-tune; it is how to establish that prompting, retrieval, and scoping
> have genuinely failed first, and how to recognise the specific and relatively narrow situations where
> adaptation is the right instrument. A learner who finishes this course and correctly decides **not** to
> fine-tune has used it as intended.

## Why this exists · the big idea

- **The problem before the solution**: fine-tuning is the intuitive response to "the model does not do
  what I want", and it is usually the wrong one. It is reached for to inject knowledge — which retrieval
  does better, cheaper, and freshly — far more often than to shape behaviour, which is the thing it
  actually does well. The result is a recurring, expensive failure pattern: weeks of data work and
  training produce a model that is stale on facts, worse on everything outside the training
  distribution, harder to operate, and no better on the original complaint. The engineer needs both a
  reliable decision procedure for avoiding that, and real competence in the technique for the cases that
  survive it.
- **Keep-this-if-you-forget-everything**: fine-tuning teaches behaviour, not facts — exhaust prompting,
  retrieval, and scoping first, and when you do adapt, the dataset is the whole job.
- **Big ideas touched**: `correctness-vs-pragmatism` (adaptation is a costly bet on a measured gap, not a
  default), `abstraction-and-its-cost` (an adapter is a compact approximation of a full fine-tune, with
  the trade-offs approximations carry), `taming-state` (adapted weights are a versioned artefact with a
  lifecycle, not a configuration change).

## Prerequisites

- **Prior topics**: [`creating-ai-powered-apps`](./creating-ai-powered-apps.md) (prompting, structured
  output, and RAG — the alternatives this course requires you to exhaust first),
  [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md) (**hard prerequisite**: a
  fine-tune with no eval is unfalsifiable, and every decision in this course is an eval comparison),
  [`statistics-for-evaluation`](./statistics-for-evaluation.md) (the base-versus-adapted comparison is a
  paired significance test, not two printed numbers),
  [`inference-serving-and-model-deployment`](./inference-serving-and-model-deployment.md) (where an
  adapter is actually served), [`data-engineering`](./data-engineering.md) (the dataset pipeline),
  [`just-enough-python`](./just-enough-python.md).
- **Tools & environment**: a macOS/Linux terminal; Python 3.x under `uv`; a small open-weights base model
  and a parameter-efficient fine-tuning library, both pinned CVE-clean at authoring; a training runtime.
  **GPU access is optional**: every example is sized to run on CPU or a small consumer GPU against a
  tiny base model, so the mechanics, dataset work, and evaluation discipline are fully exercisable
  without a training cluster; runs requiring larger hardware are marked **[GPU]** and ship with committed
  reference artefacts.
- **Assumed knowledge**: the model-application material and its eval discipline; what tokens and a
  context window are; loading and transforming a dataset in Python; the idea of gradient-based training
  at a conceptual level. **No deep-learning course is assumed** — this course explains what it needs and
  does not teach model architecture or backpropagation theory.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-20 — **durable spine**: the distinction between teaching behaviour and injecting knowledge; the
  decision procedure ordering prompting, retrieval, and scoping ahead of adaptation; dataset quality
  dominating dataset size; low-rank adaptation as a _principle_ (training a small number of additional
  parameters instead of all of them); catastrophic forgetting and the base-model regression it causes;
  the mandate to evaluate an adapted model against the base it must beat; and distillation as
  behaviour transfer from a larger teacher. None of these depend on a library, a framework, or a model
  generation.
- 2026-07-20 — `[Needs Verification]` **volatile, accuracy-note only**: every fine-tuning library and
  trainer name, its API surface, its configuration keys, and its defaults. Pin exact versions at
  authoring, keep library-specific configuration in an accuracy-note sidebar, and never state a spine
  concept in terms of a library's parameter name.
- 2026-07-20 — `[Needs Verification]` **at authoring**: the LoRA method's originating paper — its authors,
  year, and canonical formulation — and the published results attributed to it. The **principle** of
  low-rank adaptation is spine; the citation must be verified against the primary source before it is
  written, and the specific rank/alpha guidance quoted anywhere must be traced to the source read. Do
  not reproduce a citation from memory.
- 2026-07-20 — `[Needs Verification]` **at authoring**: Chip Huyen's fine-tuning framing referenced in the
  scope note above — verify the exact wording and locate it in the specific work before quoting it
  directly. The framing is used structurally here; the direct quotation must be sourced.
- 2026-07-20 — `[Needs Verification]` **volatile**: base-model IDs, their licences and permitted uses,
  hosted fine-tuning-service pricing, GPU-hour costs, and any published benchmark improvement figure for
  a fine-tuned model. All are dated snapshots. Licence terms in particular must be re-verified at
  authoring, because a base model's permitted commercial use can change between releases.
- 2026-07-20 — `[Needs Verification]` **volatile**: quantized-training and adapter-merging technique names
  and their published memory/quality figures. Teach the underlying trade as durable and treat every named
  technique and number as dated.

## Concepts

<!-- co-NN · concept enumeration. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · behaviour-not-knowledge** — fine-tuning reliably shapes form, style, format, and task
  behaviour; it is an unreliable and expensive way to install facts.
- **co-02 · the-knowledge-injection-mistake** — the most common and most costly misuse is fine-tuning to
  add facts, which produces a model stale from the moment training ends.
- **co-03 · exhaust-prompting-first** — a substantial share of gaps blamed on the model close with better
  instructions, examples, and output structure, at no training cost.
- **co-04 · exhaust-retrieval-first** — if the gap is missing information, retrieval solves it better,
  cheaper, and with facts that stay current.
- **co-05 · exhaust-scoping-first** — narrowing the task until the base model succeeds is frequently
  cheaper than adapting a model to a task that is too broad.
- **co-06 · the-decision-procedure** — a written, ordered gate — measured gap, alternatives exhausted,
  behaviour-shaped not knowledge-shaped, data obtainable, evaluation possible — passed before any
  training begins.
- **co-07 · legitimate-fine-tuning-cases** — consistent output format, a domain register or style,
  proprietary task behaviour with no textual description, latency or cost reduction via a smaller model,
  and tool-use patterns the base model handles poorly.
- **co-08 · the-cost-nobody-budgets** — data labour, training compute, evaluation, and the standing
  maintenance obligation of a model that must be re-adapted whenever the base changes.
- **co-09 · supervised-fine-tuning** — training on input/output pairs so the model learns to produce the
  target given the input.
- **co-10 · dataset-is-the-work** — outcome quality is determined by the dataset far more than by any
  training hyperparameter, and this is the single most under-weighted fact in the discipline.
- **co-11 · dataset-quality-over-quantity** — a few hundred consistent, correct, on-distribution examples
  routinely beat tens of thousands of noisy ones.
- **co-12 · dataset-consistency** — examples disagreeing with each other about the target behaviour teach
  the model to be inconsistent, and this failure is invisible until evaluation.
- **co-13 · dataset-sourcing** — production traffic, expert authoring, and synthetic generation each carry
  distinct bias, cost, and legal profiles.
- **co-14 · synthetic-data-and-its-limits** — generating training data from a larger model is fast and
  bounded by the teacher's own errors, which propagate silently.
- **co-15 · train-validation-test-discipline** — held-out splits are what keep a reported improvement from
  being memorization, and leakage between them invalidates everything downstream.
- **co-16 · data-leakage-and-contamination** — an evaluation case present in training data produces a
  result that does not transfer to production.
- **co-17 · full-fine-tuning** — updating all parameters is the most powerful and the most expensive
  option, and the most prone to degrading unrelated capability.
- **co-18 · parameter-efficient-fine-tuning** — training a small set of added parameters while freezing
  the base captures most of the benefit at a fraction of the cost.
- **co-19 · low-rank-adaptation** — the LoRA family injects trainable low-rank matrices into the model's
  layers, leaving base weights untouched.
- **co-20 · rank-and-capacity** — the adapter's rank bounds how much behaviour change it can express,
  trading capacity against size and overfitting risk.
- **co-21 · adapters-are-composable-artefacts** — adapters are small, versionable, swappable, and
  serveable independently of the base, which is an operational advantage over full fine-tuning.
- **co-22 · catastrophic-forgetting** — adaptation degrades capability outside the training distribution,
  and the degradation is invisible unless deliberately measured.
- **co-23 · overfitting-in-fine-tuning** — a small dataset trained too long memorizes rather than
  generalizes, and training loss will not reveal it.
- **co-24 · hyperparameters-that-matter** — learning rate, epochs, and adapter rank dominate; most other
  knobs are noise relative to dataset quality.
- **co-25 · evaluate-against-the-base** — the only meaningful result is a measured comparison against the
  unadapted base on the target task **and** on a regression suite covering untouched capability.
- **co-26 · regression-suite-for-forgetting** — an eval set of capabilities the fine-tune was not meant to
  change is what makes co-22 detectable.
- **co-27 · distillation** — training a smaller student to reproduce a larger teacher's behaviour, for
  latency and cost rather than for capability gain.
- **co-28 · distillation-limits** — the student inherits the teacher's errors and cannot exceed it;
  distillation is a cost optimization, not a quality one.
- **co-29 · serving-an-adapted-model** — adapters are loaded, swapped, and served against the stack from
  [`inference-serving-and-model-deployment`](./inference-serving-and-model-deployment.md), with their own
  memory and routing implications.
- **co-30 · the-maintenance-obligation** — a fine-tune is pinned to a base-model version and to a data
  distribution; both drift, and re-adaptation is a recurring cost owned by whoever shipped it.
- **co-31 · licensing-and-data-rights** — base-model licences and training-data rights constrain what may
  be trained and shipped, and are verified before training rather than after.
- **co-32 · when-to-undo-a-fine-tune** — retiring an adapter in favour of a better base model or a
  retrieval solution is a normal, healthy outcome and should be planned for.

## Tensions & trade-offs — when NOT to reach for this

- **Fine-tuning vs retrieval**: this is the decision this course exists to get right. Retrieval keeps
  facts current, cites its sources, updates without retraining, and degrades gracefully. Fine-tuning
  bakes behaviour in at a fixed point in time. If the gap is "the model does not know X", the answer is
  almost always retrieval; if it is "the model does not behave like Y", adaptation becomes a candidate —
  and even then only after prompting and scoping have failed.
- **Fine-tuning vs prompting**: a substantial share of quality gaps close with better instructions,
  few-shot examples, and enforced output structure — at zero training cost, with instant iteration and no
  maintenance obligation. The iteration-speed difference alone usually decides it.
- **Parameter-efficient vs full fine-tuning**: adapters are cheaper, faster, composable, and far less
  destructive to unrelated capability, at some ceiling on how much behaviour they can change. For nearly
  every application case the adapter is correct, and a full fine-tune should have to argue for itself
  against a measured adapter baseline.
- **Distillation's ceiling**: a distilled student cannot exceed its teacher and inherits its errors.
  Distillation buys latency and cost, never quality — treating it as a quality technique guarantees
  disappointment.
- **When NOT to fine-tune, stated plainly**: when the gap is missing knowledge; when the base model has
  not been given a fair attempt with good prompting; when the task has not been scoped down; when you
  cannot assemble a few hundred consistent correct examples; when you have no eval suite to prove the
  adapted model beats the base; when the base model will be replaced by a better one before your
  maintenance cost amortizes; or when licensing forbids it. Each of these is common, and each alone is
  sufficient reason to stop.
- **The default expectation**: most application engineers will correctly decide not to fine-tune most of
  the time. That is the intended outcome of this course, not a failure of it.

## Lineage — why it beat the alternative

- Task-specific fine-tuning was the standard adaptation method before large instruction-following models
  existed: to make a model do a task, you trained it on that task, because there was no other mechanism.
  Two developments demoted it. First, models became capable enough to be steered by instructions and
  examples at inference time, which meant most task adaptation stopped requiring weight updates at all —
  the gap that used to demand training now often closes with a better prompt. Second, retrieval-augmented
  generation established that the knowledge problem and the behaviour problem are different problems with
  different solutions: injecting facts through weights produces a model stale the moment training ends
  and unable to cite its sources, while retrieval keeps facts current, attributable, and updatable
  without touching the model. Together these left fine-tuning with a real but much narrower remit —
  shaping behaviour, format, and register that instructions describe poorly, and shrinking a model for
  latency and cost. Within that remit, full fine-tuning then lost to parameter-efficient adaptation on
  the same abstraction-and-its-cost logic that recurs throughout this library: training a small set of
  added low-rank parameters while freezing the base captures most of the benefit at a fraction of the
  compute, degrades unrelated capability far less, and produces a small composable artefact that can be
  versioned, swapped, and served independently. That operational property — an adapter as a deployable
  artefact rather than a whole new model — is why the technique won, as much as the cost saving. This
  course therefore sits deliberately late and deliberately small: after
  [`creating-ai-powered-apps`](./creating-ai-powered-apps.md) has established the alternatives it must
  rule out, after [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md) has supplied the
  only instrument that can tell whether an adaptation helped, and beside
  [`inference-serving-and-model-deployment`](./inference-serving-and-model-deployment.md), where the
  resulting artefact is actually operated.

## Worked examples

Colocated under `fine-tuning-and-adaptation/learning/code/`; each is typed, `pyright`-clean Python. The
examples use a **tiny open-weights base model** sized so every training run completes on CPU or a small
consumer GPU, keeping the dataset work, the training loop, and the evaluation discipline fully
exercisable without a training cluster. Runs needing larger hardware are marked **[GPU]** and ship with
committed reference artefacts so the analysis is reproducible offline. Contiguous `ex-01..ex-50`. Every
example cites the `co-NN` it exercises. Concepts come before examples.

> **Volume-target floor**: this syllabus lists **50** of the required **≥75** (the 75–85 By-Example/
> Primer band, floor not cap — see
> [prd.md §Volume-target bands](../../prd.md#new-course--capstone-specifications)).
> The maker adds **≥25** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its by-example quality gate.

### Beginner — the decision, not the technique (ex 01–16)

- **ex-01 · measure-the-gap-first** — quantify the actual quality gap with an eval before proposing any
  remedy — verify the gap is real and sized. (co-06, co-25)
- **ex-02 · behaviour-vs-knowledge-triage** — classify five real complaints as behaviour-shaped or
  knowledge-shaped — verify each classification against an example output. (co-01)
- **ex-03 · the-knowledge-injection-mistake** — fine-tune a tiny model on facts, then show it stale and
  unable to cite — verify the failure mode. (co-02, co-01)
- **ex-04 · retrieval-beats-it** — solve the same knowledge gap with retrieval — verify current, cited,
  and updatable answers at lower cost. (co-04, co-02)
- **ex-05 · prompting-closes-the-gap** — close a gap blamed on the model with instructions and few-shot
  examples — verify the eval improvement with zero training. (co-03)
- **ex-06 · structured-output-closes-the-gap** — enforce a schema instead of training for format — verify
  the format problem disappears. (co-03)
- **ex-07 · scoping-closes-the-gap** — narrow the task until the base model succeeds — verify the
  measured success on the narrowed task. (co-05)
- **ex-08 · the-decision-procedure** — implement the ordered gate as a written checklist applied to a real
  case — verify it produces a defensible go or no-go. (co-06)
- **ex-09 · a-correct-no-go** — apply the gate to a case that should not be fine-tuned — verify the
  documented decision not to train. (co-06, co-04)
- **ex-10 · legitimate-case-format** — a consistent output format instructions cannot reliably enforce —
  verify the gate passes. (co-07)
- **ex-11 · legitimate-case-register** — a domain register with no compact textual description — verify
  the gate passes. (co-07)
- **ex-12 · legitimate-case-smaller-model** — replacing a large model with an adapted small one for
  latency and cost — verify the gate passes on economics. (co-07, co-27)
- **ex-13 · total-cost-of-a-fine-tune** — budget data labour, compute, evaluation, and ongoing
  maintenance — verify the total against the naive compute-only estimate. (co-08)
- **ex-14 · the-maintenance-obligation** — annotate what happens to this fine-tune when the base model is
  superseded — verify the recurring cost. (co-30, co-08)
- **ex-15 · licence-and-data-rights-check** — verify the base model's licence and the training data's
  rights permit the intended use — verify the check precedes training. (co-31)
- **ex-16 · decision-diagram** — a Mermaid decision diagram from complaint through prompting, retrieval,
  and scoping to adaptation — verify every branch terminates in a decision. (co-06, co-03, co-04, co-05)

### Intermediate — the dataset and the training run (ex 17–34)

- **ex-17 · first-sft-dataset** — assemble a small instruction/response dataset for a real behaviour —
  verify schema and format validity. (co-09, co-10)
- **ex-18 · quality-beats-quantity** — train on 300 clean examples and on 10,000 noisy ones — verify the
  smaller clean set wins on eval. (co-11, co-10)
- **ex-19 · inconsistent-examples** — plant examples disagreeing about the target behaviour — verify the
  model learns the inconsistency. (co-12)
- **ex-20 · consistency-audit** — audit a dataset for internal disagreement before training — verify the
  audit catches the planted conflicts. (co-12, co-10)
- **ex-21 · source-from-production-traffic** — build a dataset from real traffic — verify distribution
  match and the bias introduced. (co-13)
- **ex-22 · expert-authored-examples** — a small expert-written set — verify quality and cost against the
  traffic-sourced set. (co-13, co-11)
- **ex-23 · synthetic-generation** — generate training data from a larger model — verify speed and volume.
  (co-14, co-13)
- **ex-24 · teacher-errors-propagate** — plant an error in the teacher — verify it appears in the student's
  behaviour. (co-14, co-28)
- **ex-25 · train-validation-test-split** — construct disjoint splits — verify no overlap. (co-15)
- **ex-26 · leakage-inflates-the-result** — leak eval cases into training — verify the inflated score and
  the detection. (co-16, co-15)
- **ex-27 · first-full-fine-tune** — full fine-tune the tiny base model — verify the target behaviour
  changes. (co-17, co-09)
- **ex-28 · full-fine-tune-cost** — measure memory, time, and artefact size — verify the cost profile.
  (co-17, co-08)
- **ex-29 · first-lora-adapter** — train a low-rank adapter on the same data with the base frozen — verify
  comparable behaviour change. (co-18, co-19)
- **ex-30 · adapter-vs-full-cost** — compare memory, time, and artefact size — verify the fraction. (co-18,
  co-17)
- **ex-31 · rank-sweep** — sweep adapter rank against eval score and artefact size — verify the capacity
  trade-off curve. (co-20)
- **ex-32 · rank-too-high-overfits** — verify excess rank on a small dataset degrades held-out
  performance. (co-20, co-23)
- **ex-33 · learning-rate-and-epochs** — sweep the two hyperparameters that matter — verify their
  dominance over the rest. (co-24)
- **ex-34 · hyperparameters-cannot-fix-data** — hold the noisy dataset fixed and sweep every knob — verify
  no configuration recovers the clean-data result. (co-24, co-10)

### Advanced — evaluation, distillation, and operation (ex 35–50)

- **ex-35 · evaluate-against-the-base** — a paired comparison of adapted against base on the target task —
  verify the improvement is statistically supported, not two printed numbers. (co-25)
- **ex-36 · regression-suite** — build an eval set of capabilities the fine-tune was not meant to change —
  verify coverage of untouched behaviour. (co-26)
- **ex-37 · catastrophic-forgetting-measured** — run the regression suite on the adapted model — verify
  the degradation the target-task eval hid. (co-22, co-26)
- **ex-38 · forgetting-is-worse-for-full-fine-tune** — compare regression-suite damage from a full
  fine-tune against an adapter — verify the difference. (co-22, co-18)
- **ex-39 · overfitting-invisible-in-training-loss** — a run whose training loss improves while held-out
  score falls — verify training loss is not the signal. (co-23, co-15)
- **ex-40 · early-stopping-on-validation** — stop on validation rather than epochs — verify the better
  held-out result. (co-23, co-24)
- **ex-41 · the-fine-tune-that-did-not-help** — a completed adaptation that fails to beat the base —
  verify the decision to discard it. (co-25, co-32)
- **ex-42 · distil-a-smaller-student** — train a small student to reproduce a larger teacher's behaviour —
  verify latency and cost improvement. (co-27)
- **ex-43 · student-cannot-exceed-teacher** — verify the student's ceiling against the teacher on the same
  eval. (co-28, co-27)
- **ex-44 · distillation-decision-record** — a written record framing distillation as a cost optimization
  with a measured quality cost — verify both figures. (co-28, co-08)
- **ex-45 · serve-an-adapter** — load and serve the adapter against the stack from
  [`inference-serving-and-model-deployment`](./inference-serving-and-model-deployment.md) — verify the
  adapted behaviour in production shape. (co-29, co-21)
- **ex-46 · hot-swap-adapters** — swap between two adapters over one base — verify both behaviours from a
  single served base. (co-21, co-29)
- **ex-47 · adapter-memory-and-routing** — measure the serving-side memory and routing cost of multiple
  adapters — verify the capacity impact. (co-29, co-21)
- **ex-48 · version-pinning-to-a-base** — pin the adapter to its base version and simulate a base upgrade
  — verify the re-adaptation requirement. (co-30, co-21)
- **ex-49 · retire-an-adapter** — replace the adapter with a better base model or a retrieval solution —
  verify the retirement is a clean, planned outcome. (co-32, co-04)
- **ex-50 · capstone-justified-adaptation** — the complete arc: a measured gap, a documented decision
  procedure ruling out prompting, retrieval, and scoping, a curated and consistency-audited dataset with
  leak-free splits, a rank-justified adapter, a paired evaluation against the base with a
  forgetting-regression suite, a licence check, a served swappable artefact, and a written maintenance and
  retirement plan — verify the adaptation is justified end to end or correctly abandoned at the gate.
  (co-01–co-32)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: carry one real behaviour gap through the entire adaptation arc with the decision gate taken
  seriously — measure the gap, prove prompting, retrieval, and scoping cannot close it, curate and audit a
  dataset, train a rank-justified low-rank adapter, evaluate it against the base on both the target task
  and a forgetting-regression suite with a paired statistical comparison, serve it as a swappable
  artefact, and write its maintenance and retirement plan. **A correctly documented decision not to
  fine-tune is a passing capstone** provided the gate is evidenced with measurements rather than
  asserted.
- **Concepts exercised**: [ ] a measured gap and the ordered decision gate (co-01–co-06) [ ] alternatives
  genuinely exhausted with eval evidence (co-03–co-05) [ ] total cost including maintenance, and the
  licence check (co-08, co-30, co-31) [ ] a curated, consistency-audited, leak-free dataset (co-10–co-16)
  [ ] a parameter-efficient adapter with a justified rank (co-18–co-20, co-24) [ ] paired evaluation
  against the base plus a forgetting-regression suite (co-22, co-25, co-26) [ ] overfitting controlled on
  validation (co-23) [ ] the artefact served and swappable (co-21, co-29) [ ] a written retirement plan
  (co-32).
- **Ordered steps**:
  1. `fine-tuning-and-adaptation/learning/capstone/decision/` — measure the gap with a real eval, then
     attempt to close it with better prompting, with retrieval, and with task scoping, recording the eval
     result of each attempt. Complete the ordered decision gate and the licence and data-rights check.
     Verify each alternative was genuinely attempted and measured, and that the go or no-go decision cites
     those measurements. **If the gate says no, document it and stop here — this is a passing outcome.**
  2. `dataset/` — curate the instruction/response dataset, run the consistency audit, document sourcing
     and its bias, and construct disjoint train/validation/test splits with a leakage check. Verify the
     audit is clean, the splits are disjoint, and no eval case appears in training.
  3. `train/` — train the low-rank adapter with the base frozen, sweeping rank and stopping early on
     validation. Verify the chosen rank is justified against the sweep rather than defaulted, and that the
     stopping point is set by validation rather than epoch count.
  4. `evaluate/` — run the paired comparison against the unadapted base on the target task, and run the
     forgetting-regression suite over capability the fine-tune was not meant to change. Verify the target
     improvement is statistically supported using the machinery from
     [`statistics-for-evaluation`](./statistics-for-evaluation.md), and that any regression on untouched
     capability is measured and reported rather than discovered later.
  5. `operate/` — serve the adapter as a swappable artefact against the serving stack, pin it to its base
     version, and write the maintenance and retirement plan covering base-model upgrade and the conditions
     under which the adapter is retired. Verify hot-swap works, the version pin is explicit, and the
     retirement conditions are concrete.
- **Acceptance criteria**: the decision gate is evidenced with eval measurements for each rejected
  alternative rather than asserted, and a documented no-go is accepted as complete; where training
  proceeds, the dataset passes its consistency audit, the splits are disjoint with a clean leakage check,
  and the adapter's rank is justified against a sweep; the adapted model is compared against the base with
  a paired statistical test on the target task **and** against a forgetting-regression suite covering
  untouched capability, with any degradation reported; early stopping is driven by validation rather than
  epoch count; the base-model licence and training-data rights are verified before training; the artefact
  is served, hot-swappable, and pinned to its base version; a written maintenance and retirement plan
  states the conditions for re-adaptation and for retirement; and the entire suite runs on CPU or a small
  consumer GPU with `[GPU]`-marked runs backed by committed reference artefacts.
- **Done bar**: runnable end-to-end (tiny base model, CPU or small consumer GPU) + web-verified.

## Read more

> The LoRA citation and the Huyen framing quoted in this course's scope note are both
> `[Needs Verification]`: locate and read the primary source before writing either, and cite the version
> read. Do not reproduce a citation from memory.

- **Designing Machine Learning Systems** — Chip Huyen (2022). The production framing this course's
  de-emphasis of fine-tuning follows; verify the specific fine-tuning passages at authoring.
- **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** — Patrick Lewis et al. (2020). The
  alternative this course requires you to rule out before adapting weights, and the reason the
  knowledge/behaviour split is the central distinction. <https://arxiv.org/abs/2005.11401>
- **Language Models are Few-Shot Learners** — Tom B. Brown et al. (2020). The result that made
  instruction-and-example steering a substitute for task-specific training, and thereby narrowed
  fine-tuning's remit. <https://arxiv.org/abs/2005.14165>
- The originating paper for **low-rank adaptation** — verify authors, year, and canonical formulation
  against the primary source at authoring, then cite it here.

## In which paths

- `immediately-effective/software-engineer-to-ai-engineer` — **owning path**: placed late and framed as a
  decision skill, per the deliberate de-emphasis stated in the scope note.
- `interview-ready/software-engineer` — candidate placement in the AI & harness engineering deepening
  tail — pending manifest re-verification (D8 four-path rule).
- `immediately-effective/software-engineer` — candidate placement in the deepening band — pending
  manifest re-verification (D8 four-path rule).
- `fundamentally-strong/software-engineer` — candidate placement in Stage 12 · AI & harness engineering
  — pending manifest re-verification (D8 four-path rule).

---

← Back to [README.md — course library catalog](./README.md)
