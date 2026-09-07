---
description: "Covers dark/light mode compliance, required shape differentiation, and a worked implementation example for accessible Mermaid colors."
when_to_use: "Use when implementing accessible colors in a Mermaid diagram and need a concrete classDef example."
---

# Mermaid Color Accessibility: Dark Mode, Shape Differentiation, and Implementation Example

## Dark and Light Mode Compliance

All colors must provide sufficient contrast in BOTH rendering modes:

**Light mode background**: White (`#FFFFFF`)
**Dark mode background**: Dark gray/black (`#1E1E2E`)

**Contrast Requirements (WCAG AA):**

- Minimum contrast ratio: **4.5:1** for normal text
- Large text (18pt+ or 14pt+ bold): **3:1**
- Element borders must be distinguishable by shape + color, not color alone

## Shape Differentiation (Required)

**Never rely on color alone.** Always use multiple visual cues:

- Different node shapes (rectangle, circle, diamond, hexagon)
- Different line styles (solid, dashed, dotted)
- Clear text labels
- Icons or symbols where appropriate

## Implementation Example

**Good Example (accessible):**

````markdown
<!-- Uses accessible colors: blue (#0173B2), orange (#DE8F05), teal (#029E73) -->

```mermaid
graph TD
  A["User Request<br/>(Blue)"]:::blue
  B["Processing<br/>(Orange)"]:::orange
  C["Response<br/>(Teal)"]:::teal

  A --> B
  B --> C

  classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
  classDef orange fill:#DE8F05,stroke:#000000,color:#FFFFFF,stroke-width:2px
  classDef teal fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:2px
```
````

**Bad Example (not accessible):**

````markdown
<!-- Uses inaccessible colors: red and green -->

```mermaid
graph TD
  A["Success"]:::green
  B["Error"]:::red

  classDef green fill:#029E73,stroke:#000000  FAIL: Invisible to protanopia/deuteranopia
  classDef red fill:#DE8F05,stroke:#000000    FAIL: Invisible to protanopia/deuteranopia
```
````
