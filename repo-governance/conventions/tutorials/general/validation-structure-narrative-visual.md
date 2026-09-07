---
description: "Lists the structure, narrative, and visual validation checklist items that docs-tutorial-checker verifies on a tutorial."
when_to_use: "Read when checking a tutorial's required sections, narrative quality, or visual completeness against the validation checklist."
---

# Validation Criteria: Structure, Narrative, and Visual Validation

These criteria define what `docs-tutorial-checker` validates. Every tutorial must pass all checks.

## Structure Validation

**Required Sections Checklist**: - [ ] Title and metadata (frontmatter with title, description, tags) - [ ] Introduction with hook and motivation - [ ] Prerequisites clearly stated - [ ] Learning objectives (3-7 specific outcomes) - [ ] 4-8 content sections - [ ] Practice exercises (at least one per major section) - [ ] Challenges section (2-4 challenges recommended) - [ ] Summary with key takeaways - [ ] Next steps with links

**Section Organization**: - [ ] Logical progression (simple → complex) - [ ] Clear section numbering - [ ] Consistent heading hierarchy - [ ] Smooth transitions between sections

## Narrative Validation

**Story Arc**: - [ ] Clear beginning (introduction with hook) - [ ] Developed middle (building knowledge) - [ ] Satisfying end (summary and next steps) - [ ] Maintains narrative flow throughout

**Progressive Scaffolding**: - [ ] Starts with simple concepts - [ ] Gradually increases complexity - [ ] No sudden jumps in difficulty - [ ] Support decreases as learner progresses

**Voice and Tone**: - [ ] Uses teaching voice (encouraging, supportive) - [ ] Consistent use of "you" and "we" - [ ] Anticipates learner confusion - [ ] Maintains conversational tone - [ ] Avoids overly academic jargon

**Transitions**: - [ ] Every section has clear transition - [ ] Connections between concepts explained - [ ] Building/connecting language used - [ ] No abrupt topic changes

## Visual Validation

**Diagrams**: - [ ] At least one diagram per major concept - [ ] Diagrams use Mermaid - [ ] Vertical orientation preferred (mobile-friendly) - [ ] Clear labels and styling - [ ] Captions or legends provided

**Mathematical Formulas**: - [ ] All formulas use LaTeX notation - [ ] Display-level equations use `$$` delimiters (not single `$`) - [ ] All `\begin{align}` blocks use `$$` delimiters - [ ] Single `$` ONLY for inline math (same line as text) - [ ] Variables defined after formulas - [ ] Worked examples with step-by-step calculations

**Code Examples**: - [ ] Complete, runnable code - [ ] Clear comments - [ ] Expected output shown - [ ] Progressive complexity - [ ] Follows language conventions

**Visual Aids**: - [ ] Abstract concepts have visualizations - [ ] Tables for comparing values - [ ] Timelines for time-based concepts - [ ] Appropriate use of emoji for emphasis
