# Inference Serving & Model Deployment (By Example, Python)

**Course ID**: `inference-serving-and-model-deployment` · **Format**: By Example · **Language**: Python.
**NEW** — this material is **entirely absent** from the library today; no existing course covers serving
a model rather than calling someone else's.

**Scope note**: running the model yourself — what happens between an HTTP request and a returned token
when you own the GPU. Covers the **two-phase shape of transformer inference** (a compute-bound prefill
over the prompt, then a memory-bandwidth-bound decode emitting one token at a time), the **KV cache**
as the data structure that makes decode affordable and the resource that limits concurrency,
**batching** (why static batching wastes a GPU on variable-length generation and what continuous
batching does about it), **GPU memory arithmetic** (weights plus KV cache plus activations, and how that
arithmetic determines your maximum concurrent requests), **quantization** as a memory-for-quality trade,
**throughput versus latency** as the central serving tension with its own vocabulary (time-to-first-token,
inter-token latency, tokens per second per user versus aggregate), **capacity planning and autoscaling**
against a workload whose requests have unpredictable output lengths, and **the self-hosting decision**
itself — when owning inference beats paying an API, and the substantial ways it does not. Serving
frameworks of the vLLM/TGI class are the concrete vehicle for the examples and are treated as
**volatile**: every framework name, flag, and version lives in an accuracy note, never in the spine.

## Why this exists · the big idea

- **The problem before the solution**: an engineer who has only ever called a hosted model API has no
  mental model of what their token bill is buying, why latency behaves the way it does, why the same
  hardware serves eight concurrent users comfortably and falls over at twelve, or whether self-hosting
  would help. Serving looks like ordinary request/response infrastructure and is not — the unit of work
  is a token, the request's cost is not known when it arrives, and the dominant resource is GPU memory
  held for the duration of a generation rather than CPU consumed at its start.
- **Keep-this-if-you-forget-everything**: generation is memory-bandwidth-bound, the KV cache is the
  resource you are really scheduling, and every serving decision is a throughput-versus-latency trade
  made explicit.
- **Big ideas touched**: `abstraction-and-its-cost` (the token API hides a scheduler, a cache, and a
  memory budget you eventually have to see), `taming-state` (the KV cache is per-request mutable state
  whose lifetime and size dominate capacity), `correctness-vs-pragmatism` (quantization trades measurable
  quality for capacity, deliberately).

## Prerequisites

- **Prior topics**: [`creating-ai-powered-apps`](./creating-ai-powered-apps.md) (tokens, context windows,
  what a completion request is), [`backend-at-scale`](./backend-at-scale.md) (load, queueing, capacity,
  autoscaling), [`containers-and-orchestration`](./containers-and-orchestration.md) (packaging and
  scheduling a GPU workload), [`computer-architecture`](./computer-architecture.md) (memory hierarchy and
  bandwidth, which is the entire reason decode behaves as it does),
  [`site-reliability-engineering`](./site-reliability-engineering.md) (SLOs, load testing, capacity
  planning), [`just-enough-python`](./just-enough-python.md).
- **Tools & environment**: a macOS/Linux terminal; Python 3.x under `uv`; a serving framework of the
  vLLM/TGI class and a small open-weights model, both pinned CVE-clean at authoring; a load-generation
  tool; container tooling. **GPU access is optional throughout**: every example runs against either a
  small CPU-servable model or a deterministic simulator of the scheduler and KV cache, so the mechanics
  are learnable without hardware, with GPU-only measurements clearly marked as such and supplied as
  committed reference data.
- **Assumed knowledge**: HTTP services and load testing; tokens and context windows; containers; the idea
  of a memory hierarchy and that bandwidth, not capacity, is often the binding constraint.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-20 — **durable spine**: the prefill/decode split, the KV cache as the mechanism trading memory
  for recomputation, the memory-bandwidth-bound character of autoregressive decode, the arithmetic
  relating model weights and cache size to concurrency, continuous batching as the response to
  variable-length generation, and the throughput-versus-latency tension are architectural facts about
  transformer inference. They have been stable since the architecture was introduced and are independent
  of any serving framework.
- 2026-07-20 — `[Needs Verification]` **volatile, accuracy-note only**: every serving framework name
  (vLLM, TGI, and their successors), every version, every configuration flag, and every default. Frameworks
  in this space change substantially within a single release cycle. Pin exact versions at authoring, keep
  all framework-specific configuration in an accuracy-note sidebar, and never state a spine concept in
  terms of a framework's flag name.
- 2026-07-20 — `[Needs Verification]` **volatile**: GPU model names, VRAM capacities, memory bandwidths,
  hourly rental prices, and every hosted-API per-token price used in a build-versus-buy calculation. These
  are snapshots with a short half-life. Teach the **calculation** in the spine and place every input
  number in a dated sidebar the reader is told to re-source.
- 2026-07-20 — `[Needs Verification]` **volatile**: named memory-management and attention-kernel
  techniques and their published speedup figures. Teach the underlying problem — cache fragmentation
  under variable-length generation, and the memory-bandwidth cost of attention — as durable, and treat
  every named technique and benchmark number as dated.
- 2026-07-20 — `[Needs Verification]` **at authoring**: quantization format names, their bit widths, and
  published quality-degradation measurements. The trade-off is durable; the specific formats and their
  measured costs are not. Any quality claim must be re-verified and cited to the source read.
- 2026-07-20 — every open-weights model ID used in an example is a pinned snapshot; read it from
  configuration and re-verify licensing terms at authoring.

## Concepts

<!-- co-NN · concept enumeration. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · inference-is-not-ordinary-request-response** — the unit of work is a token, the request's
  total cost is unknown on arrival, and the dominant resource is memory held for the generation's
  duration.
- **co-02 · prefill-phase** — processing the input prompt is a parallel, compute-bound pass whose cost
  scales with prompt length.
- **co-03 · decode-phase** — emitting tokens is sequential and memory-bandwidth-bound, and this asymmetry
  explains almost every counterintuitive serving behaviour.
- **co-04 · why-decode-is-bandwidth-bound** — each decoded token reads the full weight set and the growing
  cache, so throughput tracks memory bandwidth rather than arithmetic throughput.
- **co-05 · kv-cache-purpose** — caching per-token key and value tensors avoids recomputing attention over
  the whole sequence on every step.
- **co-06 · kv-cache-size-arithmetic** — cache size scales with sequence length, batch size, layers, and
  heads, and computing it is the prerequisite to every capacity decision.
- **co-07 · kv-cache-is-the-scarce-resource** — available cache memory, not compute, usually sets the
  maximum number of concurrent requests.
- **co-08 · cache-fragmentation** — variable and unpredictable generation lengths fragment naively
  allocated cache memory, stranding capacity.
- **co-09 · paged-cache-allocation** — allocating cache in fixed blocks rather than contiguous
  per-request regions recovers the stranded capacity, on the same principle as OS paging.
- **co-10 · prefix-sharing** — requests sharing a prompt prefix can share its cached keys and values,
  which is the serving-side counterpart of prompt caching.
- **co-11 · static-batching-wastes** — batching requests together and waiting for all to finish idles the
  GPU on every request that finished early.
- **co-12 · continuous-batching** — admitting and retiring requests at token granularity keeps the batch
  full and is the single largest throughput win in modern serving.
- **co-13 · scheduling-and-admission-control** — the scheduler decides which waiting requests join the
  batch, and its policy determines fairness, latency distribution, and tail behaviour.
- **co-14 · preemption-and-recompute** — under cache pressure a request can be evicted and its cache
  recomputed later, trading latency for the ability to admit more work.
- **co-15 · throughput-vs-latency** — batching more raises aggregate tokens per second and raises each
  user's inter-token latency; this trade is the central serving decision.
- **co-16 · serving-latency-vocabulary** — time-to-first-token, inter-token latency, per-user tokens per
  second, and aggregate throughput are distinct metrics optimized by opposing choices.
- **co-17 · ttft-vs-itl-tradeoff** — prioritizing prefill improves time-to-first-token and stalls
  in-flight decodes; prioritizing decode does the reverse.
- **co-18 · gpu-memory-budget** — weights plus KV cache plus activations plus framework overhead must fit,
  and the remainder after weights is what buys concurrency.
- **co-19 · quantization-tradeoff** — reducing numeric precision shrinks weights and cache, buying
  concurrency and speed at a measurable quality cost that must be evaluated rather than assumed.
- **co-20 · model-parallelism-basics** — a model too large for one device is split across devices, adding
  interconnect traffic and a new failure mode.
- **co-21 · capacity-planning-for-token-workloads** — capacity is planned against a distribution of
  prompt and output lengths, not a request rate, because request cost is not uniform.
- **co-22 · load-testing-a-token-service** — a load test must reproduce the real prompt-length and
  output-length distributions or it measures a workload that does not exist.
- **co-23 · autoscaling-a-gpu-service** — long cold starts from loading weights and coarse, expensive
  scaling units make GPU autoscaling behave unlike stateless CPU autoscaling.
- **co-24 · deployment-packaging** — the served artefact is weights plus runtime plus configuration, and
  it is versioned and rolled out as a unit.
- **co-25 · rollout-and-rollback-of-a-model** — changing the served model is a production change with
  quality consequences, requiring the same staged rollout and rollback discipline as any release.
- **co-26 · observability-for-serving** — queue depth, batch occupancy, cache utilization, preemption
  rate, and the latency metrics of co-16 are the signals that explain a serving problem.
- **co-27 · self-hosting-decision** — self-hosting wins on sustained high utilization, data residency,
  latency floors, and model control, and loses on operational burden, idle cost, and elasticity.
- **co-28 · total-cost-of-ownership** — the honest comparison includes idle hours, engineering time,
  on-call, and the utilization you will actually achieve — not the hourly GPU price against the API
  price at full load.

## Tensions & trade-offs — when NOT to reach for this

- **Throughput vs latency**: every lever in this course moves the same slider. Larger batches serve more
  users per GPU-hour and make each user wait longer between tokens. There is no configuration that
  optimizes both, only a configuration chosen deliberately against a stated SLO — which means you cannot
  tune a serving stack without first deciding which metric you are accountable for.
- **Quantization vs quality**: lower precision buys real capacity and costs real quality, and the cost is
  task-dependent enough that a published degradation figure does not transfer to your workload. This is
  the clearest case in the course for measuring rather than trusting — evaluate the quantized model on
  your own eval suite from
  [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md) before accepting the trade.
- **Self-hosting vs an API**: self-hosting looks cheaper the moment you compare hourly GPU cost against
  per-token API pricing at full utilization, and that comparison is almost always wrong. Real utilization
  is spiky, idle GPUs bill continuously, and the operational load is a standing engineering commitment.
  The build-versus-buy calculation must use realistic utilization or it is not a calculation.
- **When NOT to reach for this**: if your traffic is low, spiky, or unpredictable, a hosted API is
  cheaper, faster to ship, and more elastic — and the correct engineering decision. This course exists to
  make that a reasoned conclusion rather than a default, and to equip you for the cases where it flips.
- **When NOT to self-host at all**: a team without GPU operations experience, without on-call coverage,
  and without a data-residency or model-control requirement forcing the issue should not be operating
  inference infrastructure. Recognising that is part of the material.

## Lineage — why it beat the alternative

- The first generation of model serving treated inference as ordinary request/response infrastructure:
  load the model into a process, batch a fixed group of requests together, run them to completion, return
  the results. Two properties of autoregressive generation destroyed that design. First, the two phases
  behave completely differently — prefill is a parallel compute-bound pass while decode is a sequential
  memory-bandwidth-bound one — so hardware sized and tuned for one is wrong for the other. Second, and
  more damaging, output length is not known when a request arrives, so a static batch runs at the speed
  of its longest generation while every finished sequence holds its slot and idles the device. The
  responses that won are both borrowed from operating systems, which is the clearest signal that this is
  a scheduling and memory-management problem wearing machine-learning clothes. Continuous batching
  applied preemptive scheduling at token granularity, admitting and retiring requests continuously so the
  batch stays full. Paged cache allocation applied virtual-memory paging to the KV cache, replacing
  contiguous per-request regions — which fragment badly under variable lengths — with fixed blocks, and
  in doing so made prefix sharing across requests almost free. Together they moved the binding constraint
  from "compute you cannot keep busy" to "cache memory you must schedule", which is why every capacity
  question in this course reduces to the arithmetic in co-06 and co-18. This material connects the token
  economics taught abstractly in [`creating-ai-powered-apps`](./creating-ai-powered-apps.md) and
  [`agent-context-and-memory`](./agent-context-and-memory.md) to the hardware that actually produces
  them, and it applies the capacity and load-testing discipline of
  [`backend-at-scale`](./backend-at-scale.md) and
  [`site-reliability-engineering`](./site-reliability-engineering.md) to a workload whose per-request cost
  is a random variable.

## Worked examples

Colocated under `inference-serving-and-model-deployment/learning/code/`; each is typed, `pyright`-clean
Python. Examples run against either a small CPU-servable open-weights model or a **deterministic
scheduler-and-cache simulator** committed with the course, so the mechanics — batching policy, cache
occupancy, preemption, admission control — are fully learnable and testable **without GPU access**.
Examples requiring real GPU measurement are marked **[GPU]** and ship with committed reference
measurements so the analysis is reproducible offline. Contiguous `ex-01..ex-50`. Every example cites the
`co-NN` it exercises. Concepts come before examples.

> **Volume-target floor**: this syllabus lists **50** of the required **≥75** (the 75–85 By-Example/
> Primer band, floor not cap — see
> [prd.md §Volume-target bands](../../prd.md#new-course--capstone-specifications)).
> The maker adds **≥25** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its by-example quality gate.

### Beginner (ex 01–16)

- **ex-01 · serve-a-model-locally** — stand up a small open-weights model behind an HTTP endpoint —
  verify a completion returns. (co-01, co-24)
- **ex-02 · token-is-the-unit-of-work** — annotate why request count is a meaningless load unit here —
  verify two same-count workloads costing very differently. (co-01)
- **ex-03 · unknown-cost-on-arrival** — show two identical-looking prompts producing 10 and 500 output
  tokens — verify the cost is unknowable at admission. (co-01, co-21)
- **ex-04 · measure-prefill** — time the prompt-processing phase across prompt lengths — verify the cost
  scales with input length. (co-02)
- **ex-05 · measure-decode** — time per-token emission across output lengths — verify the near-constant
  per-token cost. (co-03)
- **ex-06 · prefill-vs-decode-profile** — profile one request's phase split — verify the two phases are
  separable and behave differently. (co-02, co-03)
- **ex-07 · bandwidth-bound-demonstration** — vary batch size and observe decode throughput — verify the
  bandwidth-bound signature. (co-04, co-03)
- **ex-08 · phase-diagram** — a Mermaid diagram of the request lifecycle through prefill and decode —
  verify both phases and the cache write. (co-02, co-03, co-05)
- **ex-09 · no-cache-recomputation** — implement attention without a cache and measure the cost growth —
  verify the quadratic blowup. (co-05)
- **ex-10 · add-the-kv-cache** — cache keys and values across steps — verify the same output at far lower
  cost. (co-05)
- **ex-11 · compute-cache-size** — compute cache bytes from layers, heads, dimension, precision, and
  sequence length — verify against the simulator's measurement. (co-06)
- **ex-12 · cache-growth-over-a-generation** — plot cache occupancy across a long generation — verify the
  linear growth. (co-06, co-07)
- **ex-13 · concurrency-limited-by-cache** — compute maximum concurrent requests from a memory budget —
  verify the simulator refuses the next admission at that point. (co-07, co-18)
- **ex-14 · memory-budget-breakdown** — account weights, cache, activations, and overhead against a stated
  budget — verify the remainder available for concurrency. (co-18)
- **ex-15 · budget-diagram** — a Mermaid diagram of GPU memory partitioned across the four consumers —
  verify each is shown to scale. (co-18, co-06)
- **ex-16 · latency-vocabulary** — measure time-to-first-token, inter-token latency, per-user tokens per
  second, and aggregate throughput on one run — verify all four are distinct. (co-16)

### Intermediate (ex 17–34)

- **ex-17 · static-batching** — implement fixed-group batching in the simulator — verify correct output.
  (co-11)
- **ex-18 · static-batching-idle-waste** — measure device idle time caused by early-finishing sequences —
  verify the wasted capacity. (co-11)
- **ex-19 · continuous-batching** — admit and retire at token granularity — verify batch occupancy stays
  high. (co-12)
- **ex-20 · throughput-gain-measured** — compare static against continuous batching on the same workload
  — verify the throughput difference and its source. (co-12, co-11)
- **ex-21 · batch-size-vs-itl** — sweep batch size against inter-token latency — verify the trade-off
  curve. (co-15, co-16)
- **ex-22 · throughput-latency-frontier** — plot aggregate throughput against per-user latency — verify no
  configuration optimizes both. (co-15)
- **ex-23 · admission-control-policy** — implement a queue admission policy under a cache limit — verify
  rejected and queued requests are handled predictably. (co-13, co-07)
- **ex-24 · scheduling-policy-affects-tails** — compare first-come-first-served against a
  shortest-remaining policy — verify the p99 difference. (co-13)
- **ex-25 · scheduler-starvation** — a policy starving long generations — verify the starvation and the
  fairness fix. (co-13)
- **ex-26 · prefill-priority-hurts-itl** — prioritize prefill and measure the stall in in-flight decodes —
  verify the time-to-first-token gain and inter-token cost. (co-17, co-16)
- **ex-27 · chunked-prefill** — split a long prefill so decodes are not stalled — verify both metrics
  improve against the naive policy. (co-17, co-13)
- **ex-28 · contiguous-cache-fragmentation** — allocate cache contiguously per request under mixed lengths
  — verify stranded capacity. (co-08)
- **ex-29 · paged-cache-allocation** — allocate in fixed blocks instead — verify the stranded capacity is
  recovered. (co-09, co-08)
- **ex-30 · paging-analogy** — annotate the correspondence to OS virtual memory — verify each concept maps.
  (co-09)
- **ex-31 · prefix-sharing** — two requests sharing a system-prompt prefix share cache blocks — verify the
  memory and prefill saving. (co-10, co-09)
- **ex-32 · prefix-sharing-limits** — a workload with no shared prefix — verify the optimization does not
  apply and why. (co-10)
- **ex-33 · preemption-under-pressure** — evict a request's cache under pressure and recompute later —
  verify admission improves and that request's latency worsens. (co-14)
- **ex-34 · preemption-thrashing** — over-aggressive preemption causing repeated recompute — verify the
  throughput collapse and the fix. (co-14, co-13)

### Advanced (ex 35–50)

- **ex-35 · quantize-a-model** — serve a quantized variant — verify the memory reduction and the
  concurrency gain. (co-19, co-18)
- **ex-36 · quantization-quality-cost** — evaluate the quantized model on a real eval suite from
  [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md) — verify the measured quality
  delta rather than a published figure. (co-19)
- **ex-37 · quantization-decision-record** — a written trade decision citing measured capacity gain and
  measured quality loss — verify both numbers are the learner's own. (co-19, co-28)
- **ex-38 · model-parallel-split** — **[GPU]** split a model across devices with committed reference
  measurements — verify interconnect traffic appears as a new cost. (co-20)
- **ex-39 · parallelism-failure-mode** — annotate the failure introduced by a multi-device split — verify
  it has no single-device equivalent. (co-20)
- **ex-40 · workload-length-distribution** — characterize real prompt and output length distributions —
  verify the distribution, not the mean, drives capacity. (co-21)
- **ex-41 · realistic-load-test** — drive load reproducing those distributions — verify results differ
  from a uniform-length test. (co-22, co-21)
- **ex-42 · load-test-that-lies** — a fixed-length load test — verify it under-predicts real tail latency.
  (co-22)
- **ex-43 · capacity-model** — derive required replicas from the distribution and a latency SLO — verify
  the model against a load test. (co-21, co-15)
- **ex-44 · gpu-cold-start** — measure weight-load time on scale-up — verify autoscaling cannot react at
  request timescales. (co-23)
- **ex-45 · autoscaling-policy** — a policy sized for cold starts and coarse scaling units — verify it
  holds the SLO through a traffic ramp. (co-23, co-21)
- **ex-46 · package-the-deployment** — version weights, runtime, and configuration as one artefact —
  verify reproducible startup. (co-24)
- **ex-47 · staged-model-rollout** — roll a new served model out behind a ramp with quality guardrails —
  verify a regression triggers rollback. (co-25, co-24)
- **ex-48 · serving-observability-dashboard** — expose queue depth, batch occupancy, cache utilization,
  preemption rate, and the four latency metrics — verify each explains a distinct incident. (co-26)
- **ex-49 · build-vs-buy-calculation** — compute total cost of ownership at realistic utilization against
  hosted API pricing — verify the answer flips with utilization and that idle cost is included. (co-27,
  co-28)
- **ex-50 · capstone-inference-service** — a complete self-hosted service: continuous batching over a
  paged cache with prefix sharing, an admission and scheduling policy tuned to a stated SLO, a documented
  memory budget, a quantization decision backed by measured quality, realistic load testing, an
  autoscaling policy accounting for cold starts, full serving observability, and a build-versus-buy
  recommendation — verify it holds its SLO under a realistic workload and that every configuration choice
  is justified by a measurement. (co-01–co-28)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: stand up and tune a self-hosted inference service for a small open-weights model against a
  stated latency SLO and a realistic workload distribution — continuous batching over a paged KV cache
  with prefix sharing, an admission and scheduling policy chosen deliberately on the
  throughput/latency frontier, a documented GPU memory budget, a quantization decision backed by a
  measured quality evaluation, an autoscaling policy that survives cold starts, full serving
  observability — and conclude with a defensible build-versus-buy recommendation. Runs end to end against
  the committed simulator and a CPU-servable model; GPU-only figures come from committed reference
  measurements.
- **Concepts exercised**: [ ] prefill/decode phases and the bandwidth-bound decode (co-02–co-04) [ ] KV
  cache arithmetic and its role as the scarce resource (co-05–co-07, co-18) [ ] paged allocation and
  prefix sharing (co-08–co-10) [ ] continuous batching, scheduling, admission control, preemption
  (co-11–co-14) [ ] the throughput/latency frontier and the four latency metrics (co-15–co-17)
  [ ] quantization evaluated rather than assumed (co-19) [ ] capacity planning and realistic load testing
  against a length distribution (co-21, co-22) [ ] autoscaling with cold starts, packaging, staged model
  rollout (co-23–co-25) [ ] serving observability (co-26) [ ] a total-cost-of-ownership decision (co-27,
  co-28).
- **Ordered steps**:
  1. `inference-serving-and-model-deployment/learning/capstone/serve/` — serve the model, instrument the
     four latency metrics, and document the GPU memory budget with the cache arithmetic that yields a
     maximum concurrency. Verify the computed concurrency limit matches the point at which the simulator
     refuses admission.
  2. `scheduler/` — implement continuous batching over a paged cache with prefix sharing, plus an
     admission and scheduling policy with preemption under pressure. Verify batch occupancy stays high
     under mixed generation lengths, that fragmentation-stranded capacity is recovered against a
     contiguous baseline, and that no request class starves.
  3. `tune/` — plot the throughput/latency frontier, select an operating point against the stated SLO, and
     make the quantization decision by evaluating the quantized model on a real eval suite. Verify the
     operating point is justified in writing and that the quantization trade cites the learner's own
     measured quality delta, not a published one.
  4. `capacity/` — characterize the workload's prompt and output length distributions, run a load test
     reproducing them, derive a capacity model, and write an autoscaling policy sized for weight-load cold
     starts. Verify the capacity model predicts the load test's behaviour and that the policy holds the
     SLO through a traffic ramp.
  5. `operate/` — package weights, runtime, and configuration as one versioned artefact; wire the serving
     observability dashboard; execute a staged model rollout with a quality guardrail and a rollback. Then
     write the build-versus-buy recommendation. Verify each dashboard signal explains a distinct injected
     incident, that the rollout rolls back on a planted regression, and that the recommendation uses
     realistic utilization including idle cost.
- **Acceptance criteria**: the service holds its stated latency SLO under a load test that reproduces
  realistic prompt and output length distributions; the documented memory budget's computed concurrency
  limit matches observed behaviour; continuous batching over a paged cache measurably outperforms static
  batching over a contiguous cache on the same workload, with the improvement attributed to the specific
  mechanism; the chosen operating point on the throughput/latency frontier is justified in writing
  against the SLO; the quantization decision cites a quality delta the learner measured on their own eval
  suite; the autoscaling policy accounts for measured cold-start time; a staged model rollout rolls back
  on a planted quality regression; every serving observability signal is shown to explain a distinct
  incident; the build-versus-buy recommendation uses realistic utilization and includes idle and
  operational cost; and the entire suite runs offline without GPU access, with GPU-only figures drawn
  from committed reference measurements.
- **Done bar**: runnable end-to-end (offline, simulator plus CPU-servable model) + web-verified.

## Read more

> Framework documentation and benchmark figures are `[Needs Verification]` and volatile: cite the exact
> version read at authoring and place every number in a dated accuracy note rather than in prose.

- **Attention Is All You Need** — Ashish Vaswani et al. (2017). The architecture whose attention mechanism
  is the reason the KV cache exists and the reason decode is bandwidth-bound.
  <https://arxiv.org/abs/1706.03762>
- **Designing Machine Learning Systems** — Chip Huyen (2022). Production ML infrastructure framing,
  including the build-versus-buy and capacity questions this course makes concrete.
- The serving framework's own documentation for the pinned version used in the examples — the authoritative
  reference for batching, cache, and scheduling configuration. Select, pin, and cite at authoring; treat
  every flag and default as volatile.

## In which paths

- `immediately-effective/software-engineer-to-ai-engineer` — **owning path**: the infrastructure half of
  the AI-engineer transition, placed after the model-application and agent material so the learner knows
  what they are serving.
- `interview-ready/software-engineer` — candidate placement in the AI & harness engineering deepening
  tail — pending manifest re-verification (D8 four-path rule).
- `immediately-effective/software-engineer` — candidate placement in the deepening band — pending
  manifest re-verification (D8 four-path rule).
- `fundamentally-strong/software-engineer` — candidate placement in Stage 12 · AI & harness engineering
  — pending manifest re-verification (D8 four-path rule).

---

← Back to [README.md — course library catalog](./README.md)
