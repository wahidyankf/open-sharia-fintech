# Worked-Example Structure, Diagram Requirements, and ayokoding-web Integration

## Worked-Example Structure (Both Modes)

```markdown
### Worked Example N: Title

**Context**: [The concept this worked example demonstrates and why it matters]

[Code block with 1.0-2.25 density annotations, OR pseudocode/config block, OR a captioned accessible
Mermaid diagram — whichever medium fits the concept, OR, in no-code sub-mode, the scenario narrative

- decision artifact]

**Key takeaway**: [1-2 sentences summarizing the lesson]

**Why It Matters**: [50-100 words on design implications, trade-offs, and related concepts]
```

## Diagram Requirements

Every Mermaid diagram MUST use the verified WCAG-compliant palette from the
`docs-creating-accessible-diagrams` Skill: Blue `#0173B2`, Orange `#DE8F05`, Teal `#029E73`, Purple
`#CC78BC`, Brown `#CA9161`. Use diagrams where a visual relationship, data flow, state machine, or
decision structure materially aids understanding — skip diagrams for simple, self-explanatory
concepts. There is no separate diagram-count floor: in standard mode a diagram can itself be the
worked example's medium (counted as one of the 45-60); in no-code sub-mode a diagram supports a
scenario without being counted separately.

## ayokoding-web Integration

The `apps-ayokoding-www-developing-content` Skill provides ayokoding-web specific guidance:

- **Bilingual strategy**: Default English, Indonesian translation
- **Content workflow**: tRPC API, content management
- **Linking conventions**: ayokoding-web specific patterns
