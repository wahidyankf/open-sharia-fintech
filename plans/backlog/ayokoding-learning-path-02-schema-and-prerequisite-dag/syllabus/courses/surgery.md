# Course Surgery Plan — shared-library edits and their four-path blast radius

**Status**: PLANNED, NOT EXECUTED. Every trim, seam, and forward-link described below is specified here
and applied in a later delivery step. Nothing in this document has been carried out against the donor
courses.

This document exists because of **D8**: course surgery is a **four-path change**. The course library is
shared, so any edit, split, or merge ripples to **every manifest that carries the edited course** — and
verification against the current files shows that all three existing manifests carry every course
touched below, so the blast radius of each surgery here is **all four manifests, without exception**.
Each surgery therefore states its blast radius explicitly before it is applied, and every affected
manifest must be re-verified prerequisite-consistent afterward.

**The four manifests**:

| Key   | Manifest                                                                                                  | Status                                       |
| ----- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| IR-SE | [`interview-ready/software-engineer`](../paths/manifest-interview-ready-software-engineer.md)             | exists on disk                               |
| IE-SE | [`immediately-effective/software-engineer`](../paths/manifest-immediately-effective-software-engineer.md) | exists on disk                               |
| FS-SE | [`fundamentally-strong/software-engineer`](../paths/manifest-fundamentally-strong-software-engineer.md)   | exists on disk                               |
| IE-AI | `immediately-effective/software-engineer-to-ai-engineer`                                                  | **new** (D3) — authored as part of this plan |

> **Membership verification (2026-07-20)**: the `## In which paths` block of every course named in this
> document lists all three existing manifests. There is no course below whose surgery touches fewer than
> four manifests. Any future surgery must re-run this check rather than assuming it.

## Surgery index

| #   | Surgery                                        | Kind                    | Donors                                                                                      | Blast radius       | Risk     |
| --- | ---------------------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------- | ------------------ | -------- |
| S1  | Extract evals into a single owner              | Extract + trim to links | `creating-ai-powered-apps`, `agentic-ai`, `agent-orchestration-subagents-and-observability` | All four manifests | **HIGH** |
| S2  | `creating-ai-powered-apps` ↔ `agentic-ai` seam | Split along a seam      | `creating-ai-powered-apps`, `agentic-ai`                                                    | All four manifests | **HIGH** |
| S3  | Guardrails — explicit no-op                    | **No change**           | `agent-permissions-and-sandboxing`                                                          | None               | none     |

---

## S1 — Extract evals into a single owner

### The defect

Evaluation is currently **triple-taught with no owner**. Three courses each teach a partial, overlapping
treatment, and none of them is authoritative:

| Donor                                             | Current eval material                                                                                                                                                      | Verified location                  |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `creating-ai-powered-apps`                        | co-19 `evaluation` — golden-set eval, LLM-as-judge, schema assertion. Examples ex-49, ex-50, ex-51. Also carries an **Accuracy notes** "Evaluation" bullet.                | co-19; ex-49–ex-51                 |
| `agentic-ai`                                      | co-25 `agent-evaluation` (trajectory eval, task success rate, LLM-as-judge) and co-26 `evals-in-ci`. Examples ex-52–ex-58. Also an **Accuracy notes** "Evaluation" bullet. | co-25, co-26; ex-52–ex-58          |
| `agent-orchestration-subagents-and-observability` | co-19 `evals-as-tests`, co-20 `eval-driven-improvement`, co-21 `regression-evals`. **Theme D · Observability & evals**, examples ex-39–ex-44.                              | co-19–co-21; ex-39–ex-44 (Theme D) |

The three treatments disagree in depth, overlap in content, and collectively still omit the material
that matters most — error analysis, measured judge-human agreement, judge-scope reliability, and a
regression bar justified against a noise floor. A learner meets "LLM-as-judge" three times and is never
told to measure the judge.

### The surgery

1. **The new [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md) becomes the single
   owner** of evaluation depth. It is already authored to absorb all three treatments and to add the
   missing rigor.
2. **The new [`evaluating-ai-output-essentials`](./evaluating-ai-output-essentials.md) owns the light
   gate** — dataset, deterministic scorers, pass rate, before/after comparison — placed early, before
   RAG and agents (D5).
3. **Trim each donor to a forward-link.** Donors retain only the minimum needed for their own narrative
   to make sense, and point at the owner for everything else.
4. **Do NOT create a fourth parallel treatment.** This is the explicit failure mode D8 names. The two
   new eval courses are one owner split by depth along a stated scope guard, not two more voices in the
   same argument.

### Per-donor trim specification

**`creating-ai-powered-apps`**

- **Keep** co-19, retitled in substance to the light-gate scope: an eval harness scores answers against
  golden datasets. This course is where a learner first needs the idea, and removing it entirely breaks
  the capstone.
- **Remove** the LLM-as-judge material from co-19 and from ex-50 — a judge taught without agreement
  measurement is exactly the anti-pattern the deep course exists to correct, and it must not be a
  learner's first exposure.
- **Retain** ex-49 (golden set) and ex-51 (schema assertion); both are light-gate material.
- **Replace** ex-50 (`eval-llm-as-judge`) with a forward-link annotation to
  [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md) co-09–co-16.
- **Amend** the capstone's eval step to reference the light gate rather than implying this course teaches
  eval depth.
- **Add** a scope-guard note under the **Scope note** naming the two eval owners.
- **Renumbering**: none. ex-50 is replaced in place, keeping `ex-01..ex-80` contiguous.

**`agentic-ai`**

- **Collapse** co-25 and co-26 into a **single** forward-linking concept covering only what an agent
  chapter must state: an agent is evaluated on its trajectory as well as its outcome, and the eval suite
  gates CI. Depth moves to the owner.
- **Remove** the LLM-as-judge treatment (ex-54) and the standalone scoring examples (ex-53, ex-55) —
  these are the owner's co-09–co-17.
- **Retain** ex-52 (trajectory eval) as the agent-specific hook, re-pointed at the owner's co-18.
- **Move** ex-56, ex-57, ex-58 (eval dataset, evals in CI, regression bar) to the owner's co-21, co-23,
  co-24; leave one CI-gate mention in `agentic-ai` with a forward link.
- **Amend** the **Tensions & trade-offs** bullet "No evals means no safety net" to keep the argument and
  forward-link the method.
- **Amend** the **Accuracy notes** "Evaluation" bullet: keep the durable trajectory-versus-outcome
  distinction, move the tooling detail to the owner.
- **Renumbering**: **required**. Removing ex-53, ex-54, ex-55, ex-56, ex-57, ex-58 leaves a gap in a
  contiguous `ex-NN` sequence. Either renumber the tail or backfill the freed slots with agent material
  the course currently lacks. **Backfill is preferred** — renumbering invalidates every external
  reference to a later `ex-NN` in this file.

**`agent-orchestration-subagents-and-observability`**

- **Keep** co-19 `evals-as-tests` **only** as the statement that a stochastic system needs a graded test
  suite — the observability narrative depends on it.
- **Remove** co-20 `eval-driven-improvement` and co-21 `regression-evals`; both are the owner's co-27
  and co-24.
- **Retitle Theme D** from "Observability & evals" to observability only, and **move** ex-39 through
  ex-43 to the owner.
- **Retain** ex-44 (`observability-dashboard`) — it is an observability example that happens to display
  eval scores — and re-point its eval citation at the owner.
- **Amend** the **Lineage** sentence "And evals brought the test-suite discipline to stochastic systems"
  to keep the historical claim and forward-link the method.
- **Amend** the **Accuracy notes** eval bullet to a forward link.
- **Renumbering**: **required**. Theme D is `ex-35..ex-46`; removing ex-39–ex-43 breaks contiguity.
  **Backfill with observability material is preferred** over renumbering, for the same reason as above,
  and this course has the clearer backfill case — tracing, structured logging, and metrics are
  under-exampled once evals leave.

### Blast radius — S1

| Manifest | Carries the donors?             | Impact                                                                                                                                                                                | Required re-verification                                                                                                                                       |
| -------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IR-SE    | Yes — all three, deepening tail | Donor courses shrink. **Decided**: the two new eval courses are **not** added to this manifest — eval depth is owned exclusively by the fourth path (per-role convergence, D2/DD-22). | IR-SE ships without dedicated eval-depth coverage; recorded here as the accepted, documented consequence (matches this manifest's own forward-reference note). |
| IE-SE    | Yes — all three, deepening band | Same loss shape as IR-SE. **Decided**: not inserted here either, despite the "immediately effective" framing — eval depth stays exclusive to the fourth path.                         | IE-SE ships without dedicated eval-depth coverage; recorded here as the accepted, documented consequence (matches this manifest's own forward-reference note). |
| FS-SE    | Yes — all three, Stage 12       | Same loss shape. **Decided**: not inserted here either — a fundamentals-first path losing measurement rigor is an accepted trade, not grounds for a fourth eval treatment (D8).       | FS-SE ships without dedicated eval-depth coverage; recorded here as the accepted, documented consequence (matches this manifest's own forward-reference note). |
| IE-AI    | New manifest                    | Owns both eval courses by construction (D5): light gate early, deep course after agents.                                                                                              | Verify the light gate precedes RAG and agents, and that `statistics-for-evaluation` precedes the deep course.                                                  |

**Prerequisite-consistency checks after S1** — all four manifests:

- No manifest may place [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md) before
  [`statistics-for-evaluation`](./statistics-for-evaluation.md); the deep course declares it a **hard**
  prerequisite.
- No manifest may place the deep course before
  [`agentic-ai`](./agentic-ai.md) or
  [`agent-orchestration-subagents-and-observability`](./agent-orchestration-subagents-and-observability.md);
  it evaluates trajectories those courses produce.
- No manifest may place [`evaluating-ai-output-essentials`](./evaluating-ai-output-essentials.md) after
  the RAG material in [`creating-ai-powered-apps`](./creating-ai-powered-apps.md); the light gate's
  entire rationale (D5) is that it precedes retrieval and agents.
- Every manifest carrying a trimmed donor must be re-read for a forward reference to removed material.
- `Composition total` arithmetic must be recomputed in **all four** manifests.

### Risk — S1

**HIGH.** Three courses are edited simultaneously and coverage can silently vanish from three existing
manifests if the new courses are not inserted in the same change. The mitigation is a **single atomic
delivery unit**: donors are trimmed and manifests are updated together, never in separate steps.

---

## S2 — The `creating-ai-powered-apps` ↔ `agentic-ai` seam

### The defect

These two are the **sharpest existing overlap in the library**. Both teach tool-calling, the agentic
loop, MCP, evaluation, and cost control, verified by direct file read:

| Topic        | `creating-ai-powered-apps` | `agentic-ai`                | Also owned elsewhere                           |
| ------------ | -------------------------- | --------------------------- | ---------------------------------------------- |
| Tool-calling | co-08, ex-37–ex-41         | present throughout          | `agent-tools-and-mcp` co-01–co-07 — real owner |
| Agentic loop | co-17, ex-44–ex-46         | the course's entire subject | `the-agent-loop` — real owner                  |
| MCP          | co-18, ex-42–ex-43         | co-19                       | `agent-tools-and-mcp` co-08–co-22 — real owner |
| Evaluation   | co-19                      | co-25, co-26                | **S1 gives this an owner**                     |
| Cost control | co-20–co-22                | co-24                       | split, no owner                                |

The overlap is worse than a duplication problem: for three of the five rows, **neither** course is the
real owner — the harness cluster is. `creating-ai-powered-apps` and `agentic-ai` are each teaching a
preview of material that `the-agent-loop` and `agent-tools-and-mcp` own properly.

### The proposed seam

**`creating-ai-powered-apps` = one model call, done well. `agentic-ai` = many model calls, coordinated.**

The seam is **the loop**. Everything that is true of a single request/response — prompting, sampling,
streaming, structured output, embeddings, retrieval, multimodal input, moderation, cost of a call —
belongs to `creating-ai-powered-apps`. Everything that only becomes a problem once the model's output
feeds its own next input — iteration control, trajectory, accumulated cost, compounding error, the
amplified injection surface — belongs to `agentic-ai`.

Applying the seam:

| Material               | Current                    | Proposed                                                                                                                  |
| ---------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Tool-calling contract  | Both                       | **`creating-ai-powered-apps`** — a single tool round-trip is a single-call concern. Depth stays in `agent-tools-and-mcp`. |
| Agentic loop           | Both                       | **`agentic-ai`**. `creating-ai-powered-apps` keeps one motivating example and forward-links.                              |
| MCP                    | Both                       | **Neither** — forward-link both to `agent-tools-and-mcp`, the actual owner.                                               |
| Evaluation             | Both                       | **Neither** — resolved by S1.                                                                                             |
| Cost/latency of a call | `creating-ai-powered-apps` | **`creating-ai-powered-apps`** — unchanged.                                                                               |
| Accumulated agent cost | `agentic-ai` co-24         | **`agentic-ai`** — unchanged, and the seam makes the distinction from the row above explicit rather than accidental.      |

### Blast radius — S2

| Manifest | Impact                                                                                                                                       | Required re-verification                                                                                                |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| IR-SE    | Both courses carried. MCP material leaves both; if `agent-tools-and-mcp` is optional in this manifest's tail, IR-SE could lose MCP entirely. | Confirm `agent-tools-and-mcp` is reachable wherever MCP is forward-linked, or keep a minimal MCP mention in the donors. |
| IE-SE    | Same. The deepening band's optionality creates the same reachability risk.                                                                   | Same check.                                                                                                             |
| FS-SE    | Both carried in Stage 12 alongside the full harness cluster; forward-link targets are reliably present.                                      | Confirm ordering places `agent-tools-and-mcp` after both donors, not before.                                            |
| IE-AI    | Both carried; the seam is what makes the AI path's ordering coherent.                                                                        | Verify single-call material precedes loop material, and that the harness cluster follows both.                          |

**The reachability trap**: S2's forward links only work if the link target is in the same manifest. In
IR-SE and IE-SE the harness cluster sits in an **optional deepening tail**, so a forward link can point
at a course the learner never reaches. Either the trim keeps a self-contained minimum in the donor, or
the target is promoted out of the optional tail. **This must be decided per manifest before S2 executes.**

### Risk — S2

**HIGH**, and higher than S1 in one respect: S1 removes material that a new owner definitely provides,
whereas S2 removes material whose owner may be unreachable in two of the four manifests. **S2 should not
execute before S1**, and should not execute before the reachability decision is recorded per manifest.

---

## S3 — Guardrails: explicit no-op

**[`agent-permissions-and-sandboxing`](./agent-permissions-and-sandboxing.md) is not touched by any
surgery.** This is a deliberate, recorded decision (D8), not an omission.

The course is a **clear owner** with no competing treatment in the library: co-01–co-22 cover the
deny/ask/allow model, sandboxing, egress control, injection defense, secret hygiene, and audit logging,
and no other course teaches any of it as its own material. It is assessed as the library's **strongest
area**. Adjacent mentions in other courses (`agent-tools-and-mcp` co-19 `security-at-the-tool-boundary`,
`agentic-ai` co-22 `tool-permissioning`, co-28–co-30) are already correctly shaped as **forward-links to
this owner**, not as parallel treatments — this is precisely the structure S1 is trying to create for
evaluation, and it should be left intact as the reference example.

**Blast radius**: none. No manifest changes.

**One additive exception, not a surgery**: D11 adds the concept `train-vs-production-permission-asymmetry`
to this course. That is a concept addition into declared headroom (this course needs ≥27 more examples),
not a trim, split, or merge, and it changes no manifest.

---

## Execution order and gating

Surgeries are **dependent**, not parallel:

1. **Author the new courses first.** S1's trims are only safe once
   [`evaluating-ai-output-essentials`](./evaluating-ai-output-essentials.md),
   [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md), and
   [`statistics-for-evaluation`](./statistics-for-evaluation.md) exist. **Done** — all three are on
   disk.
2. **Record the per-manifest coverage decisions** for S1 (does each existing manifest gain the eval
   courses?) and the reachability decisions for S2. Both are manifest-owner decisions and are **blocking
   inputs**, not outcomes, of the surgery.
3. **Execute S1 as one atomic unit** — three donor trims plus all four manifest updates in a single
   change, so eval coverage is never absent from a manifest at any point.
4. **Execute S2 only after S1**, and only after its reachability decisions are recorded. S2's evaluation
   row is resolved by S1; running S2 first would re-open it.
5. **S3 executes never.** It is recorded here so a future reader does not rediscover the overlap
   question and "fix" a course that is already correct.

**Gate for every surgery**: after execution, re-run the membership verification at the top of this
document and re-verify prerequisite consistency in **all four** manifests. `Composition total`
arithmetic must be recomputed in all four.

---

← Back to [README.md — course library catalog](./README.md)
