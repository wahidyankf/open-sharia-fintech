<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: lms-init

## Learning: the mermaid gate threshold is looser than the binding label rule

- **Context**: authoring `tech-docs.md`. `rhino-cli md mermaid validate` reported
  `label_too_long` at 30 characters, so the diagrams were rewritten to sit at or just under 30.
  The gate then passed, but the rendered diagram visibly clipped every label past roughly 27
  characters.
- **Observation**: the binding rule is
  [Rule 3](../../../repo-governance/conventions/formatting/diagrams/common-syntax-errors-label-constraints-rule-3-line-length.md)
  — **20** characters per `<br/>` segment. The gate's default `--max-label-len` is **30**, which
  that document describes as "Mermaid's `wrappingWidth` baseline" and explicitly pairs with the
  advice to "use `--max-label-len 20` for stricter validation". So a green default-threshold run
  proves the diagram is under the backstop, not under the rule. The repository already documents
  this in three places, including a dedicated
  [render-fidelity caveat](../../../repo-governance/conventions/formatting/diagrams/mermaid-render-fidelity-caveat.md)
  stating that a green validate is "necessary, not sufficient".
- **Why it might generalize**: an author who meets the number the gate prints, rather than the
  number the convention states, ships a clipped diagram with a green gate. The failure mode is
  silent and only visible in rendered output. Candidate durable fixes to weigh at triage: lower the
  flowchart default to 20; or emit the Rule-3 number in the violation message so the printed
  threshold and the binding rule agree; or note in the flowchart width-constraints document that
  authors should run the strict flag before committing. The existing
  `plans/ideas/q2-not-urgent-important/mermaid-state-label-render-clipping-warn.md` two-pager
  covers the neighbouring `stateDiagram` case and may be the right place to fold this in rather
  than opening a new brief — check it first, and note that its own analysis warns any such rule
  must WARN rather than FAIL given the corpus size.
