---
description: Purpose, characteristics, example use cases, and in-project location for each of the four Diátaxis categories (Tutorials, How-To, Reference, Explanation).
when_to_use: Use when deciding which of the four Diátaxis categories a piece of documentation belongs in.
---

# The Four Categories

## Tutorials (Learning-Oriented)

**Purpose**: Teach newcomers through hands-on experience

**When to use**: When you want to help someone learn a skill or concept through practice

**Characteristics**:

- Learning by doing
- Step-by-step instructions
- Concrete outcomes
- Minimal explanation (save for "Explanation" category)
- Assumes no prior knowledge
- Encouraging tone

**Example use cases**:

- "Initial Setup for the Project"
- "Your First API Call"
- "Setting Up the Development Environment"

**In our project**:

- Location: `docs/tutorials/`
- Examples: `getting-started.md`, `first-deployment.md`

## How-To Guides (Problem-Oriented)

**Purpose**: Solve specific problems and accomplish specific tasks

**When to use**: When users know what they want to do but need guidance on how

**Characteristics**:

- Goal-oriented
- Assumes familiarity with the project
- Focused on outcomes
- Multiple approaches when applicable
- Practical and direct
- Troubleshooting included

**Example use cases**:

- "How to Configure Sharia Compliance Rules"
- "How to Deploy to Production"
- "How to Add a New Payment Provider"

**In our project**:

- Location: `docs/how-to/`
- Examples: `configure-api.md`, `deploy-docker.md`

## Reference (Information-Oriented)

**Purpose**: Provide accurate, comprehensive technical information

**When to use**: When users need to look up specific details, parameters, or specifications

**Characteristics**:

- Austere and neutral tone
- Organized for lookup
- Comprehensive coverage
- Accurate and up-to-date
- Structure over explanation
- Examples for clarity

**Example use cases**:

- "API Endpoint Reference"
- "Configuration Options Reference"
- "Database Schema Reference"

**In our project**:

- Location: `docs/reference/`
- Examples: `api-reference.md`, `configuration-reference.md`

## Explanation (Understanding-Oriented)

**Purpose**: Deepen understanding of concepts, design decisions, and "why"

**When to use**: When users need to understand context, reasoning, or broader perspective

**Characteristics**:

- Conceptual and theoretical
- Background and context
- Design decisions and trade-offs
- Multiple perspectives
- Connections between concepts
- No instructions (save for other categories)

**Example use cases**:

- "Why We Use Conventional Commits"
- "Sharia Compliance Architecture"
- "Understanding Our Authentication Model"

**In our project**:

- Location: `docs/explanation/`
- Examples: `architecture.md`, `file-naming-convention.md`
