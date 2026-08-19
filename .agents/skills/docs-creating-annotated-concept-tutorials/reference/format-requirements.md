# Annotated-Concept Format Requirements

## 1. Worked-Example / Scenario Count

**Standard mode**: minimum 45 worked examples, target band 45-60. **No-code sub-mode**: minimum 20
worked scenarios, target band 20-30. **Floor, not a cap**: flag ONLY when the count is below the
floor. Never flag for exceeding the band — more worked examples than the target is acceptable depth.

## 2. Annotation Density (Standard Mode Only)

For each code-bearing worked example: count code/pseudocode lines (excluding blank and
full-comment-only lines) and comment/annotation lines, then `density = comment_lines ÷ code_lines`
(same direction as By Example — never inverted). Flag if density <1.0 (under-annotated) or >2.5
(over-annotated). Worked examples whose medium is a diagram or config-only are exempt from this
specific check but must still carry a clear caption/explanation.

## 3. Structure

Each worked example (standard mode) or scenario (no-code sub-mode) has: context/brief explanation;
a medium (code, pseudocode, config, or diagram) that genuinely fits the concept; a key takeaway
(1-2 sentences); "Why It Matters" (50-100 words, flag if >100). No-code sub-mode additionally
requires a decision artifact with the reasoning spelled out, not just the conclusion.

## 4. Self-Containment (Standard Mode)

Code-bearing worked examples are copy-paste-runnable within the topic's scope: full imports
present, helper functions included in-place, no external references required.

## 5. Mode Integrity (CRITICAL)

**Standard-mode topic**: a `code/` directory exists with colocated runnable files for every
code-bearing worked example. **No-code sub-mode topic**: zero code blocks anywhere in the tutorial,
no `code/` directory, no runnable files referenced. Flag any code block found in a no-code
sub-mode topic as CRITICAL (mode violation).

## 6. Grouping

Per-theme clustering (not fixed beginner/intermediate/advanced tiers), incremental
simple-to-real-world progression within and across clusters, clear cluster headers.

## 7. Diagram Accessibility

Every Mermaid diagram uses the WCAG-compliant palette: Blue `#0173B2`, Orange `#DE8F05`, Teal
`#029E73`, Purple `#CC78BC`, Brown `#CA9161`. Diagrams are used only where a visual relationship,
flow, or structure materially aids understanding — not decorative filler. No separate numeric
diagram-count floor applies; a diagram may itself be a worked example's medium.

## 8. ayokoding-web Compliance

Per `apps-ayokoding-www-developing-content`: bilingual content (id/en), content structure and
metadata, linking conventions.
