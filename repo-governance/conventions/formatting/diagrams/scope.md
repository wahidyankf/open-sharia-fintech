---
description: "Lists what this convention covers (Mermaid, ASCII art, plan-doc UI mockups) and what it explicitly excludes."
when_to_use: "Use when checking whether a diagram or mockup question falls inside this convention's scope."
---

# Scope

## What This Convention Covers

- **Mermaid diagram syntax** - Flowcharts, sequence diagrams, class diagrams, state diagrams, and all supported Mermaid types
- **Color accessibility requirements** - Mandatory color-blind friendly palette for all diagrams
- **Mobile-friendly orientation** - Vertical diagram orientation for mobile viewing
- **Mermaid comment syntax** - Correct use of `%%` comments (not `%%{ }%%`)
- **ASCII art guidelines** - When and how to use ASCII as optional fallback
- **Diagram placement** - Where to use diagrams in different markdown contexts

## What This Convention Does NOT Cover

- **Diagram content strategy** - What diagrams to create (covered in specific domain conventions)
- **Vector graphics or images** - This convention is only for text-based diagrams (Mermaid and ASCII), **except** the high-fidelity `.excalidraw.png` plan mockups governed by the [UI Mockups in Plan Docs](./ui-mockups-principles-and-scope.md) section below
- **Interactive diagram features** - Platform-specific interactivity (zoom, pan) is implementation detail
- **Diagram export formats** - Exporting Mermaid to PNG, SVG, PDF (tool-specific, not repository standard)
