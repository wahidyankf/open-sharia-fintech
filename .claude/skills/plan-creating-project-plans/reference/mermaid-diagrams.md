# Mermaid Diagrams in Plans

Plans MUST include **extensive Mermaid diagrams where appropriate**: every distinct architectural concern the plan touches that a reader would otherwise reconstruct mentally from prose SHOULD receive its own diagram — one diagram per concern, not one diagram total.

Concerns that warrant their own diagram when present:

- **Component interactions** — service/agent/library call graph
- **Sequence or flow between agents or systems** — order-of-operations across processes
- **State transitions** — entity lifecycle with named states and triggers
- **Decision branches** — conditional logic with multiple outcomes
- **Dependency position** — upstream/downstream plan or system dependencies
- **Phase/delivery flow** — phased progression with gates and transition conditions

Prefer multiple focused diagrams over one overloaded diagram. Trivial/linear plans (config bumps,
renames, doc fixes) may skip diagrams when a visual would not materially improve understanding.

**Authoritative rule**: [repo-governance/conventions/structure/plans.md §Diagrams in Plans](../../../../repo-governance/conventions/structure/plans/diagrams-required.md#diagrams-in-plans)

**Palette and accessibility**: use the `docs-creating-accessible-diagrams` skill for the verified WCAG-compliant hex codes and color-blind-friendly palette.
