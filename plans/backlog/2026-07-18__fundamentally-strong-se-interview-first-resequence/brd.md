# Business Requirements — Fundamentally Strong SE Interview-First Resequence

## Business Goal

Re-frame the completed "Fundamentally Strong Software Engineer" section around the **order in which a
working engineer actually needs the material**, so the section earns its keep at the moment of highest
stakes (an interview) first, then builds broad market-relevant productivity, then deepens the rest.
The subject content is already authored; this change is about **sequence and framing**, plus a thin
layer of NEW interview-technique modules that the spiral never had.

## Primary Beneficiary Persona (north-star)

The **primary persona is an experienced software engineer re-entering the job market** — recently
laid off, returning after a gap/sabbatical, or an employed senior who wants to switch. The north-star
for every decision in this plan is: **"immediately useful" for this person.** They already have the
editor workflow and the deep fundamentals; what they need is to **refresh breadth fast, relearn
interview technique they haven't exercised in years, and get interview-ready — at mid/senior/staff
level — without walking a from-scratch curriculum first.** Beyond the interview, they need to become
**productive in real 2026 codebases** — this workspace family (`ose-public`/`ose-primer`/`ose-infra`),
an AI-agent-infra org (`remotebrowser`), and three security codebases (`wazuh/wazuh`,
`anggipradana/vacti`, `anggipradana/vacti-pentest-engine`) — and to be able to **build their own
agentic coding tool AND an agentic pentest engine**, the highest-leverage differentiators in today's
market. A from-scratch learner (career-switcher
/ returning-to-basics) is a legitimate **secondary** persona whom the canonical order still serves, but
the arc is optimized for the re-entrant.

This is why the arc leads with **Interview Preparation (through senior)** and why `overview.md` gains
an explicit **"experienced & job-hunting? start here" fast-path** that routes a re-entrant straight
into Phase 1 — the editor prologue stays canonically first for a from-scratch reader but is
**explicitly skippable** for the experienced (see [prd.md](./prd.md) and [delivery.md](./delivery.md)
Phase 8).

## Business Rationale

The sibling plan sequenced 94 topics as an _immediately-effective_ five-pass spiral — excellent for a
learner working top-to-bottom over a long horizon. But the maintainer's read of how the section is
actually consumed differs [Judgment call]:

- The **highest-frequency, highest-pressure** entry point is interview preparation for an experienced
  re-entrant — someone who lands here days-to-weeks before a senior loop, not months before a career
  arc. The spiral buries interview-relevant fundamentals across Passes 1-2, never teaches interview
  _technique_ (coding-interview patterns, the system-design interview rubric, behavioral/STAR rounds)
  at all, and forces the experienced reader through an editor prologue and from-scratch fundamentals
  they do not need.
- After interviews, the next real need is **market-relevant productivity** across platforms, and the
  market has a de-facto demand order — web first, then cloud/backend-at-scale, then mobile, then
  desktop. The spiral's ◆ "pick-your-path" branching leaves that order implicit; the maintainer wants
  one fixed, opinionated linear walk.
- The remaining breadth is **depth for its own sake** — valuable, but consumed at leisure, best
  ordered shallow → deep rather than interleaved across passes.

Re-sequencing to Prologue → Interview → Multi-Platform → Deepening makes the section's front door
match its most common, most valuable use. This is a framing/ordering change on top of finished
content, so the business cost is low relative to the alignment payoff [Judgment call].

## Business Impact

**Pain points addressed**:

- A reader preparing for interviews currently has no interview-technique material and must reconstruct
  the interview-facing subset from a spiral not organized for it.
- The platform-productivity path is a branch-your-own-adventure rather than an opinionated market-demand
  sequence, which is exactly the guidance a mid-career switcher wants.
- The five-pass narrative describes a learning cadence the maintainer no longer considers the primary
  reading model.

**Expected benefits** (qualitative reasoning; no fabricated metrics):

- The section's most time-critical use (interview prep) becomes a first-class, self-contained front
  section with real technique modules, not an emergent subset.
- The productivity path becomes a single confident recommendation aligned to hiring-market reality.
- The depth material is ordered so a reader can go as deep as they want without the spiral's
  back-and-forth.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns the arc decision and the interview-first framing.
- **Content author** (via the `apps-ayokoding-www-*-maker` agents) — writes the NEW interview modules.
- **Content reviewer** (via the `apps-ayokoding-www-*-checker` + facts/link checkers) — validates.

Consuming agents: `apps-ayokoding-www-by-example-maker`, `apps-ayokoding-www-annotated-concept-maker`,
`apps-ayokoding-www-primer-maker` and their matching checkers, plus `apps-ayokoding-www-facts-checker`
and `apps-ayokoding-www-link-checker` [Repo-grounded].

## Business-Level Success Metrics

Success is judged by how well the arc serves the **experienced re-entrant** first:

- **Productive in seven real target codebases** (observable, first-class signal): a reader who works
  the section can contribute to `ose-public` / `ose-primer` / `ose-infra` (Nx monorepo; TypeScript/
  Next.js `-www` + `-app-web`; F#/Giraffe backends; Rust CLIs; GitHub-Actions CI; Playwright E2E; the
  multi-harness AI-agent binding), to `remotebrowser` (async-Python/FastAPI + CDP browser automation +
  MCP), and to three **security** codebases — `wazuh/wazuh` (C++/C/Python manager+agent, Java
  indexer, TypeScript dashboard, XML detection ruleset), `anggipradana/vacti` (Nx/Next.js/tRPC/Drizzle
  — the same web stack as the ose family), and `anggipradana/vacti-pentest-engine` (agentic swarm +
  MCP + CDP applied to security). The
  [Productive in Target Codebases](./tech-docs.md#productive-in-target-codebases-proof-of-transfer-outcome-anchor)
  mapping proves each stack skill is delivered by a named module, with gaps filled by the new
  `async-python-and-fastapi-services`, `browser-automation-with-cdp`, harness, `just-enough-cpp`, and
  `detection-engineering-and-siem-operations` modules. (`wazuh` is web-verified; the two `vacti` repos
  are maintainer-supplied and were not publicly discoverable on 2026-07-18 — treated as unverified.)
- **Can build their own agent harness AND agentic pentest engine** (observable, first-class signal):
  the harness-engineering cluster + `capstone-build-your-own-coding-agent` let the reader build a
  minimal Claude-Code-style coding agent from scratch, and the security suite +
  `detection-engineering-and-siem-operations` + `capstone-build-your-own-pentest-engine` let them
  build an agentic pentest/scanning engine (swarm + MCP + CDP + tool-chaining) — a re-entrant who can
  build both agent tooling and security tooling is maximally market-relevant in 2026 [Judgment call].
- **Time-to-interview-ready** (qualitative reasoning): a re-entrant can reach Phase 1 via the
  fast-path and refresh interview technique + breadth without first walking the prologue or
  from-scratch fundamentals — the section delivers value on the first sitting.
- **Refresh, not first-learn** (observable): the four NEW interview modules are written in a
  refresh/technique register (assume prior professional experience), not a teach-from-zero register —
  verified by the matching checker + inspection.
- **Layoff/gap-narrative coverage** (observable): the behavioral module explicitly covers framing an
  employment gap / layoff / re-entry story in behavioral rounds — a persona-specific need.
- **Senior-loop orientation** (observable): `overview.md` carries a fast-path affordance and an
  interview-loop-map framing so a re-entrant orients to a 2026 senior loop quickly.
- **Arc coherence** (observable): `overview.md` and `_index.md` describe exactly the new
  3-phase-plus-prologue arc with no residual five-pass framing. Verified by inspection + link check.
- **Ordering integrity** (observable): the rendered nav order matches the canonical mapping table
  row-for-row; every existing topic slug resolves to a real folder (no invented slugs).
- **Interview coverage** (observable): the four NEW interview modules each ship both a learning and a
  drilling track and pass their checker + facts-checker + link-checker.
- **No regressions** (observable): `nx run ayokoding-www:build` renders green; heading-hierarchy,
  markdownlint, and link validation pass across the section.

## Business-Scope Non-Goals

- Re-writing the pedagogy or depth of any of the 94 existing topics.
- Adding an Indonesian mirror.
- Changing any application/component code under `apps/ayokoding-www/src/`.
- Introducing interactive/JS flashcards — drilling stays static markdown, matching the sibling.

## Business Risks and Mitigations

| Risk                                                                              | Mitigation                                                                                                                                                 |
| --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dependency not actually done — resequencing a partially-authored tree breaks nav. | Phase 0 precondition gate hard-blocks until the sibling plan is confirmed DONE (all 94 topics + capstones live). See [delivery.md](./delivery.md) Phase 0. |
| Weight recompute collisions or off-by-one shift nav silently.                     | Snapshot current weights first; recompute mechanically from the mapping table; verify rendered nav order against the table as a gate.                      |
| Content cross-links inside topics reference the old pass framing.                 | Link-checker sweep + a grep for "Pass 0".."Pass 5" / "five-pass" across the section; fix stragglers as Root-Cause-Orientation work.                        |
| Syllabus renumbering ripples into the sibling plan's prd table (source of truth). | DN-6 routes the renumbering decision explicitly; recommended path updates the sibling prd table in the same PR to keep one source of truth.                |
