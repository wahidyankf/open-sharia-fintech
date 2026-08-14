# Requirements: Standard and No-Code Modes

## Annotated-Concept Requirements (Standard Mode)

- **45-60 worked examples** per topic (a floor, not a cap — a topic may exceed 60 when the subject
  genuinely demands more; never fewer than 45)
- Each concept is introduced via an **annotated worked example** using whichever medium fits best:
  - **Code** in the topic's designated primary language
  - **Pseudocode** only where code genuinely does not fit
  - **Config** (YAML/HCL/JSON, etc.) where the concept is inherently configuration-shaped
  - A **captioned accessible Mermaid diagram** where the concept is a relationship, flow, or
    structure better shown than coded
- **Annotation density 1.0-2.25** comment lines per code/pseudocode line, on every code-bearing
  worked example — identical standard to By Example, measured per worked example
- **Incremental progression**: simple → real-world, grouped into **per-theme clusters** (not fixed
  beginner/intermediate/advanced tiers — cluster by concept family, e.g., "Automata & Formal
  Languages", "Complexity & Big-O", "Computability")
- `code/` directory with colocated runnable files for every code-bearing worked example

## Annotated-Concept Requirements (No-Code Sub-Mode)

- **20-30 worked scenarios** per topic (floor, not a cap)
- Each scenario follows an annotation-equivalent structure: the reasoning behind every
  recommendation or decision is spelled out (the "why", not just the "what"), matching the spirit of
  the 1.0-2.25 density rule even though no code lines exist to count
- Scenarios produce a **decision artifact** (a filled-in decision record, prioritization matrix,
  governance checklist, runbook excerpt) rather than a code listing
- **No** `code/` directory, **no** runnable files
- Grouped into per-theme clusters, same as standard mode
