# Product Requirements — Learning Path Manifest (AI-engineer)

## Product Overview

One **path manifest** composes a from-scratch AI-engineering journey: an ordered,
prerequisite-consistent `courseOrder` list — a **path ID**
(`careers/immediately-effective/ai-engineer`), a display **title**, a **description** — stored as a
standalone YAML data file under
`apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/ai-engineer.yaml`.
It gets a thin content **landing anchor** (prose/SEO only, no `courseOrder`) at
`/en/learn/paths/careers/immediately-effective/ai-engineer`, and a card in the paths hub's `careers/`
group (hub layout owned by `ayokoding-learning-path-03-navigation-ui`).

The path assumes **no** prior software-engineering competence: shared SWE-fundamentals prerequisite
courses are **included** at the head of `courseOrder`, not linked out, so a reader with zero
programming background can start at `courseOrder[0]` and finish the whole path from this one manifest.
It **walks** (includes, never links) the nine-course AI/harness cluster directly, and teaches
**building** AI systems, not driving them.

**This product surface is composition only.** No course body is authored here; no rendering component
is built here. What ships is: one YAML manifest, one landing anchor, one hub card, the integrity and
smoothness verification that keeps it honest, and the growth that closes its smoke-test-scoped
composition as the AI/harness cluster lands.

## Persona

- **A reader with no assumed prior software-engineering competence, aiming straight at AI engineering**
  — owns none of the SWE fundamentals the sibling plan's three manifests teach; wants to become
  immediately effective at **building** AI systems (models, agents, evals, inference serving), not at
  driving coding agents. Its foundational SWE prerequisites are **included at the head of
  `courseOrder`**, not linked out — a reader with zero programming background can start at
  `courseOrder[0]` and finish. Those included prerequisites are existing library courses; no new course
  body is authored for them. Converges on a distinct AI-engineering endpoint, never the
  software-engineering endpoint the sibling plan's three manifests share.
- **A reader who lands on a shared course by deep-link / share** — arrives at a course URL without a
  path context. Once this manifest is published, that reader's "this course is part of" affordance can
  name this path alongside whichever of the sibling plan's three manifests already include the same
  course (the definitive four-way version of that affordance is the sibling plan's own final-phase
  responsibility).
- **Maintainer** — owns this path's from-scratch architecture and authors its landing content via the
  ayokoding maker agents.

## User Stories

- As a **reader with no software-engineering background**, I want the AI-engineering path's manifest to
  **include** its SWE-fundamentals prerequisites at the head of `courseOrder` rather than link out to
  them, so that I can start at `courseOrder[0]` with zero prior programming knowledge and finish the
  whole path from one manifest.
- As a **reader walking the AI-engineering path**, I want `courseOrder` to actually **walk** the
  agent-building courses after the included SWE fundamentals, so that the path teaches what its own
  scope promises once the foundation is laid.
- As a **reader on this path's landing**, I want the courses listed in the manifest's exact order with
  the path context carried into every link, so that "next" always means the next course in this arc.
- As the **maintainer**, I want this manifest verified prerequisite-consistent at its own phase gate, so
  that an invalid ordering fails at the boundary that introduced it.
- As the **maintainer**, I want this manifest published early over partial content to carry a
  falsifiable before/after check for the AI/harness-cluster courses it deliberately defers, so that a
  truncated path cannot pass as complete.
- As the **maintainer**, I want this plan's own start to be gated on a specific, checkable merge event
  in the sibling plan (not a calendar assumption), so that authoring priority #1 is honored mechanically.
- As a **screen-reader / keyboard user**, I want this path's ordered course list and its hub card to be
  fully navigable without a mouse.

## Acceptance Criteria (Gherkin)

Each scenario uses exactly one primary `Given`, one `When`, and one `Then`; every extra precondition,
action, or outcome chains with `And`.

```gherkin
Scenario: This plan's authoring begins only once the sibling plan's interview-ready delivery unit has merged
  Given the careers/interview-ready/software-engineer MVP (owned by ayokoding-learning-path-12-careers-se-manifests) has merged its delivery unit to origin/main
  When this plan's Phase 0 checks its start precondition
  Then the merged-PR check for that delivery unit returns a non-zero count
  And this plan's Phase 1 authoring begins only after that check passes
```

```gherkin
Scenario: The AI-engineer path includes its software-engineering prerequisites instead of linking them
  Given the careers/immediately-effective/ai-engineer path manifest is published
  When a reader with no prior software-engineering competence inspects its courseOrder
  Then the shared software-engineering-fundamentals courses this path's AI-specific spine depends on are present at the head of courseOrder, ordered prerequisite-consistently
  And that reader can start at courseOrder[0] and finish the whole path from this one manifest, with no external prerequisite link required
```

```gherkin
Scenario: The AI-engineer manifest walks the full nine-course AI/harness cluster after growth
  Given the nine-course AI/harness cluster has landed as authored bodies across two course-authoring successor plans
  When the growth phase appends them to this plan's manifest
  Then all nine cluster course IDs are present in courseOrder at their correct topological position
  And the manifest's entry count has grown by exactly nine over its recorded pre-growth count
```

```gherkin
Scenario: This plan's AI-engineer manifest layer builds and validates green
  Given this plan's one path manifest and its landing anchor are published
  When the app build, the affected test tiers, and the link and heading validators run
  Then the build and every affected tier succeed
  And manifest integrity and prerequisite consistency report zero violations for this plan's manifest
```

## Product Scope

### In scope

- One `PathManifest` YAML data file at
  `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml`.
- One thin landing anchor at `<PATHS>careers/immediately-effective/ai-engineer/_index.md`.
- This plan's one-card slice of the paths-hub population.
- Manifest integrity and prerequisite-consistency verification at every phase gate.
- The from-scratch progression-smoothness audit.
- Growth of this one manifest from its smoke-test-scoped starting composition to its full walk of the
  nine-course AI/harness cluster.

### Out of scope

- The three `software-engineer`-role manifests, their landings, hub cards, and the three cross-manifest
  checks that bind them — owned entirely by `ayokoding-learning-path-12-careers-se-manifests`.
- The four-manifest "names every path" check and the terminal 127-course catalog assertion — the
  sibling plan's own final-phase responsibility (see [README JC-5](./README.md#jc-5-this-plan-does-not-perform-its-own-four-manifest-check)).
- Any course body, rendering component, schema, URL/redirect work, or `skills/` category manifest.

### UI-design-funnel disposition

This plan adds **no net-new screen and no net-new component**. It publishes content and data into two
screens whose design funnels are already complete and owned by
`ayokoding-learning-path-03-navigation-ui`. Full exemption record in
[tech-docs §UI-design-funnel exemption](./tech-docs.md#ui-design-funnel-exemption-recorded-explicitly).
The exemption is scoped to the design funnel only — the **Rule-15 three-tester retest remains
mandatory**, scoped to this plan's one landing plus its hub-card slice, and runs in
[Phase 4](./delivery.md#phase-4-manual-ui-verification-and-rule-15-three-tester-retest).

## Product-Level Risks

- **Order/manifest drift**: mitigated by manifest-integrity + prerequisite-consistency checks at every
  gate and stable course-ID slugs.
- **Silent truncation**: mitigated by a falsifiable before/after entry-count-delta check, a dedicated
  growth phase, and a terminal gate asserting the full nine-course walk.
- **Prerequisite-inclusion regression** (a future edit accidentally drops one of the included
  SWE-fundamentals IDs): mitigated by a persisted presence check for the named set, re-run at every
  gate.
- **Duplication creep**: mitigated by callout-only framing and referencing shared courses by ID only.
- **Ownership erosion**: mitigated by the invariant stated in this plan's own docs and its own
  boundary-check phase.
- **Coupling misread as circular**: mitigated by the explicit sequence diagram and distinct-node framing
  in both READMEs — the two edges live in different phases of the **sibling's** sequence, not this
  plan's.
- **This plan starting on an unverified assumption that the sibling's Phase 1 has merged**: mitigated by
  a literal merged-PR check as this plan's Phase 0 start condition.
- **Hub incoherence mid-flight**: mitigated by a per-href presence check for this plan's own one card,
  never a whole-file count (since the sibling plan edits the same shared hub file concurrently).
