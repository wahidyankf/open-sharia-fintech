---
description: "Gives the format-selection decision table mapping diagram purpose to the required format."
when_to_use: "Use when picking which diagram format (Mermaid vs. ASCII) to use for a specific piece of content."
---

# Format Selection Rule and Decision Table

The choice between ASCII art and Mermaid is **not optional** for the diagram intents listed below. The rule is enforceable: `rules-checker` flags violations when a folder-tree appears as Mermaid, or when a relationship/flow diagram appears as plain ASCII art.

## Decision Table

| Diagram intent                   | Required format                   | Rationale                                                                                                                       |
| -------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Folder / file tree               | **ASCII art** (`├──`, `└──`, `│`) | Mirrors `ls`/`tree` terminal output; renderable in every context including raw text; no parser risk; no width-validator concern |
| Flow chart                       | **Mermaid**                       | Semantic structure; color-blind friendly palette; machine-validatable                                                           |
| Sequence diagram                 | **Mermaid**                       | Semantic structure; renders interaction over time correctly                                                                     |
| State machine                    | **Mermaid**                       | Explicit states and transitions; semantic meaning                                                                               |
| Architecture / component diagram | **Mermaid**                       | Spatial relationships; color-coded components                                                                                   |
| Dependency-direction diagram     | **Mermaid**                       | Arrow direction carries semantic meaning; validator checks width                                                                |
| User-flow diagram                | **Mermaid**                       | Decision branches and outcomes need relational rendering                                                                        |
| ER / class diagram               | **Mermaid**                       | Structured relationships and cardinality; screen-reader accessible                                                              |
| C4 model diagram                 | **Mermaid**                       | Layered architecture levels; color coding by C4 boundary                                                                        |
