# 18 · Technical Communication (Annotated-concept, ‡ no-code)

**prd row**: Pass 1 · Core Foundations · Annotated-concept · ‡ no-code · Learn 118 / Drill 218 · Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: writing that moves work forward — RFCs, ADRs, and design docs; pull-request
descriptions; incident write-ups; and reader-first structure. Pulled early despite spanning the whole
curriculum because communication compounds: every later topic is easier to learn and to ship when you
can write about it clearly. `‡`: no code — the deliverables are documents, and the acceptance bar is a
reader-review pass rather than a compiler.

## Why this exists · the big idea

- **The problem before the solution**: a good decision no one can find, follow, or trust dies in a
  hallway conversation; undocumented context becomes tribal knowledge that walks out the door with the
  person who held it.
- **Keep-this-if-you-forget-everything**: write for the reader's question, not your discovery order —
  lead with the decision and the "why", put the evidence under it, and make the document skimmable in
  thirty seconds.
- **Big ideas touched**: `correctness-vs-pragmatism` (a design doc's job is a decision that ships and
  holds, not an exhaustive treatise — capture the trade-off and move), `coupling-vs-cohesion` (a
  well-scoped ADR/RFC keeps one decision and its rationale together and cross-links rather than
  inlining everything, so documents change independently).

## Prerequisites

- **Prior topics**: [topic 9 Project Management](./09-project-management.md).
- **Tools & environment**: a plain-text/Markdown workflow in version control; an ADR/RFC template; a
  diagramming tool (a C4-style context/container view) for architecture; Neovim/VSCode with Markdown
  and spellcheck (DD-17). No runtime.
- **Assumed knowledge**: how work is scoped and tracked (topic 09); enough of the domain you're
  writing about to have a defensible point of view.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the referenced conventions are stable and correctly unpinned — RFC 2119
  keyword semantics (clarified by RFC 8174), Michael Nygard's ADR format, and the C4 model are all
  current and notation-independent. There are no version numbers to pin.
- 2026-07-12 — verified (GAP for plan owner): this is a no-code topic, so the "runnable" acceptance bar
  is reframed as a reader-review/comprehension pass — there is nothing to execute, and the shipped text
  reflects that.
- 2026-07-16 — re-verified, no changes since 2026-07-12: RFC 2119 (rfc-editor.org/rfc/rfc2119, S.
  Bradner, March 1997, BCP 14) remains unsuperseded and is only "Updated by" RFC 8174
  (rfc-editor.org/rfc/rfc8174, May 2017), which still confirms the ALL-CAPS-only special meaning for
  MUST/SHOULD/MAY — no obsoletion for either. Michael Nygard's ADR post
  (cognitect.com/blog/2011/11/15/documenting-architecture-decisions) is still live and still cited by
  adr.github.io as the origin of the context/decision/status/consequences format, with no competing
  standard supplanting it as the default. c4model.com is still live, still authored by Simon Brown, and
  still describes the same four levels (System Context, Container, Component, Code) as
  "notation independent" and "tooling independent," with no breaking version change. All three claims:
  still current.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 8 (Annotated-concept ‡). Each example below cites the co-NN it exercises. -->

- **co-01 · reader-first-bluf** — Lead with the bottom line up front: the decision and the ask come first,
  so a reader gets the answer before the discovery-order narrative that produced it.
- **co-02 · inverted-pyramid** — Order content most-important to least, so a reader who stops early still
  has the conclusion; supporting detail sinks to the bottom where it can be skipped.
- **co-03 · thirty-second-skim-test** — A well-structured doc yields its decision and next action from
  headings, bold, and first sentences alone in about thirty seconds.
- **co-04 · design-doc-rfc-structure** — A design doc/RFC states problem, context, options considered,
  decision, trade-offs, and open questions — decided and undecided kept explicitly separate.
- **co-05 · rfc-review-process** — An RFC earns "accepted" by running through a comment/approval cycle in
  which every open question is answered or explicitly deferred, not by being posted.
- **co-06 · adr-one-decision-format** — An Architecture Decision Record captures exactly one decision with
  its context and consequences — one decision per record, not a design treatise.
- **co-07 · adr-lifecycle-status** — An ADR carries a status (proposed → accepted → superseded); a changed
  decision is a new ADR that supersedes and links back, never a silent edit.
- **co-08 · adr-colocation-immutability** — An ADR lives in the repo next to the code it governs and is
  dated and immutable, so the decision record stays trustworthy instead of drifting in a wiki.
- **co-09 · pr-description-structure** — A pull-request description says what changed, why, how it was
  verified, and where a reviewer should look first — directing attention to the risky diff.
- **co-10 · blameless-postmortem-structure** — An incident write-up records timeline, impact, root cause,
  and owned follow-ups in actor-neutral language, treating failure as systemic, not personal.
- **co-11 · diagrams-as-communication** — A diagram earns its place when it conveys a structure or flow
  faster than the prose it replaces; the diagram and its prose must name the same things.
- **co-12 · c4-model-levels** — The C4 model pictures architecture at nested levels (context → container →
  component → code), each answering a different reader's question without one overloaded diagram.
- **co-13 · rfc2119-keyword-precision** — MUST/SHOULD/MAY (RFC 2119, clarified by RFC 8174) make a
  requirement's strength unambiguous, replacing vague "should probably" language.
- **co-14 · editing-cut-hedging-filler** — Cutting filler (just, really, basically) and hedging (I think,
  sort of) makes every remaining claim stand on its own — editing is removal, not addition.
- **co-15 · audience-register-match** — Vocabulary, detail, and framing are chosen for the reader: the same
  decision is written differently for an executive than for the engineer who implements it.
- **co-16 · doc-proportionality** — The artifact weight matches the decision's stakes and reversibility: a
  reversible low-stakes call gets a comment or PR note, not a heavyweight RFC.
- **co-17 · doc-rot-close-to-code** — Documentation kept close to the code, dated, and version-controlled
  resists rot; a living wiki nobody updates becomes a confident lie.

## Tensions & trade-offs — when NOT to reach for this

- **More words is not more clear**: an exhaustive doc no one reads is worse than a one-page decision
  they act on — over-documentation carries a real maintenance and attention cost.
- **Docs drift from reality**: an ADR checked in beside the code and dated stays trustworthy; a design
  doc in a wiki nobody updates becomes a confident lie. Prefer close-to-code, dated, immutable-decision
  formats over living prose you must constantly police.
- **When NOT to write the long form**: a reversible, low-stakes decision doesn't need an RFC — a
  comment or a PR description is proportionate. Reserve heavyweight docs for decisions that are
  expensive to reverse or that many people must align on.

## Lineage — why it beat the alternative

- Engineering teams learned the hard way that architecture lived only in senior engineers' heads and
  eroded with every re-org. The IETF's RFC tradition showed that durable, referenceable design writing
  scales a distributed community; Nygard's ADRs (2011) shrank that idea to a decision-sized,
  version-controlled unit that lives with the code; the C4 model gave architecture a lightweight,
  notation-independent picture. These beat "big up-front design documents" because they are cheap to
  write, cheap to find, and scoped to change independently. The habit compounds across the curriculum —
  every judgment topic's trade-off is worth more once it's written down — and it feeds directly into
  the decision records that [`42-software-architecture`](./42-software-architecture.md) formalizes.

## Worked examples

Worked scenarios / communication artifacts under `technical-communication/learning/artifacts/` (prose +
diagrams; no `code/` runtime — DD-27 leadership kind). Each is a real document you draft and revise, and
each cites the `co-NN` it exercises; the "runnable" check is a reader-review pass against a rubric, not a
compiler (DD-20/DD-30). Contiguous `ex-01..ex-25`.

### Beginner

- **ex-01 · bluf-rewrite** — rewrite a rambling status update so the bottom line comes first — verify the
  decision and the ask appear in the first sentence. (co-01)
- **ex-02 · inverted-pyramid-restructure** — reorder a doc so conclusions precede supporting detail —
  verify a reader who stops after two paragraphs still has the answer. (co-02)
- **ex-03 · thirty-second-skim-test** — apply the skim test (headings, bold, first sentences) to a doc —
  verify the skimmed-only path still yields the decision plus next action. (co-03)
- **ex-04 · pr-description-what-why-verify** — write a PR description (what / why / how-verified /
  look-here) for a real change — verify a reviewer knows where to start. (co-09)
- **ex-05 · cut-hedging-and-filler** — edit a paragraph removing filler (just, really, basically) and
  hedging (I think, sort of) — verify word count drops and every remaining claim stands unhedged. (co-14)
- **ex-06 · rfc2119-keyword-precision** — replace vague "should probably" language with precise
  MUST/SHOULD/MAY per RFC 2119 — verify each requirement's strength is unambiguous. (co-13)
- **ex-07 · audience-register-match** — write two versions of one update (executive vs implementing
  engineer) — verify each matches its audience's vocabulary and detail level. (co-15)
- **ex-08 · title-and-tldr-first** — add a one-line title plus a TL;DR summary to a doc — verify the
  summary alone conveys the outcome. (co-01, co-03)

### Intermediate

- **ex-09 · adr-one-decision** — write an ADR capturing one decision (context / decision / consequences) —
  verify it records exactly one decision, not a design treatise. (co-06)
- **ex-10 · adr-status-lifecycle** — supersede an old ADR with a new one carrying a status field
  (proposed → accepted → superseded) — verify the old ADR is marked superseded and links forward. (co-07)
- **ex-11 · adr-colocated-immutable** — place a dated ADR in-repo next to the code and amend by adding a
  new record, not editing — verify the decision record is immutable and colocated. (co-08)
- **ex-12 · rfc-options-and-tradeoff** — write an RFC with at least two options considered and the decisive
  trade-off — verify each option lists pros/cons and the decision cites the trade-off. (co-04)
- **ex-13 · rfc-review-process** — route an RFC through a comment/approval cycle and resolve open
  questions — verify every open question is answered or explicitly deferred before "accepted". (co-05)
- **ex-14 · design-doc-open-questions** — separate decided from undecided in a design doc's Open Questions
  section — verify no undecided item is stated as a decision. (co-04)
- **ex-15 · doc-proportionality** — choose the right artifact (comment vs PR description vs ADR vs RFC) for
  three decisions of varying reversibility — verify a low-stakes reversible decision gets a lightweight
  artifact. (co-16)
- **ex-16 · pr-description-review-guidance** — add a "what to review first / risk areas" section to a large
  PR — verify the reviewer's attention is directed to the risky diff. (co-09)
- **ex-17 · c4-context-diagram** — draw a C4 Level-1 context diagram (people + external systems) — verify
  every external actor and system boundary appears. (co-11, co-12)
- **ex-18 · c4-container-diagram** — draw a C4 Level-2 container diagram (apps/datastores + protocols) —
  verify each container names its technology and how it talks to its neighbors. (co-12)

### Advanced

- **ex-19 · blameless-postmortem-timeline** — write an incident timeline (detection → mitigation →
  resolution) with no blame language — verify every entry is timestamped and actor-neutral. (co-10)
- **ex-20 · postmortem-root-cause-and-followups** — complete a postmortem: impact, root cause (5-whys), and
  owned follow-ups — verify every follow-up has an owner and the root cause is systemic, not personal.
  (co-10)
- **ex-21 · diagram-beats-prose** — replace a dense prose description of a flow with a diagram plus caption
  — verify the diagram conveys the flow faster than the paragraph it replaced. (co-11)
- **ex-22 · diagram-prose-consistency** — reconcile a C4 diagram with its accompanying prose so names and
  arrows match — verify no component named in prose is missing from the diagram, and vice versa. (co-11,
  co-12)
- **ex-23 · doc-rot-close-to-code** — move a drifted wiki design doc into the repo, date it, and link it
  from the code — verify the doc now lives with the code it governs and is dated. (co-17)
- **ex-24 · rfc-to-adr-distillation** — take an accepted RFC and distill its decision into an ADR that
  outlives it — verify the ADR captures the decision and consequence without the RFC's deliberation.
  (co-04, co-06)
- **ex-25 · reader-review-rubric-pass** — run a full doc through a reader-review rubric (skimmable,
  decision-first, jargon-defined, register-matched) — verify a peer restates the decision from the doc
  alone. (co-01, co-03, co-15)

## Capstone spec — intra-topic (subject → full deliverable set)

- **Goal**: document one real decision and one real incident to a professional bar — an RFC/ADR a peer
  can act on without a meeting, and a blameless postmortem a stranger can follow — proving your writing
  moves work forward.
- **Concepts exercised**: [ ] BLUF/reader-first structure (co-01, co-02, co-03) [ ] an ADR (decision +
  status + consequences, colocated) (co-06, co-07, co-08) [ ] an RFC with options + trade-off + review
  (co-04, co-05) [ ] a PR description (co-09) [ ] a blameless incident write-up (co-10) [ ] a C4-style
  diagram (co-11, co-12) [ ] precise RFC 2119 keywords + edited, register-matched prose (co-13, co-14,
  co-15) [ ] proportional, close-to-code artifacts (co-16, co-17).
- **Ordered steps**:
  1. `.../learning/capstone/adr-0006-notification-worker-idempotency-cache.md` and `.../rfc.md` — the
     decision, options, trade-off, and open questions. Verify a peer reviewer can restate the
     decision and its rationale from the document alone.
  2. `.../pr-description.md` — a real change described (what / why / how-verified / where-to-look).
     Verify a reviewer knows where to start within thirty seconds.
  3. `.../postmortem.md` + `.../context.md` (C4) — timeline, impact, root cause, follow-ups, and a
     context diagram. Verify there is no blame language and every follow-up has an owner.
- **Acceptance criteria**: each document passes a reader-review rubric (skimmable, decision-first, no
  unexplained jargon); the postmortem is blameless and actionable; the diagram matches the prose.
- **Done bar**: reader-review-verified end-to-end + web-verified.

## Read more

**Books**

- **On Writing Well** — William Zinsser (7th ed.). Classic guide to clear, humane nonfiction prose,
  widely adapted for technical writing.
- **The Elements of Style** — Strunk, White (4th ed., 1999). Foundational terse guide to clarity and
  grammar.
- **Docs for Developers: An Engineer's Field Guide to Technical Writing** — Bhatti, Corleissen,
  Lambourne, Nunez, Waterhouse (2021). Current engineer-authored playbook for READMEs, API docs, and
  doc systems.

**Papers & articles**

- **RFC 2119: Key words for use in RFCs** — S. Bradner (1997, clarified by RFC 8174, 2017). Defines
  MUST/SHOULD/MAY used across specifications. <https://www.rfc-editor.org/rfc/rfc2119>
- **C4 model** — Simon Brown (maintained). Lean, notation-independent standard for visualizing
  architecture at context/container/component/code. <https://c4model.com/>

---

← Previous: [17 · Security Essentials](./17-security-essentials.md) · Next: [19 · Computer Science Foundations](./19-computer-science-foundations.md) →
