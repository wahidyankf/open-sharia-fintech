---
description: Five common misconceptions about the architecture, corrected
when_to_use: Use when you suspect a misunderstanding about the layers.
---

# Common Misconceptions

## Misconception 1: "agent skills are Layer 4.5"

❌ **Wrong**: agent skills are not a layer between Development and Agents.

✅ **Correct**: agent skills are delivery infrastructure (like AGENTS.md), not governance layer. They serve agents through inline knowledge delivery or fork-based task delegation.

## Misconception 2: "Agents can ignore conventions if skilled"

❌ **Wrong**: agent skills provide knowledge but don't override governance.

✅ **Correct**: Agents MUST follow conventions. Agent skills help agents understand conventions better and provide implementation patterns.

## Misconception 3: "Workflows replace agents"

❌ **Wrong**: Workflows don't replace agents, they orchestrate them.

✅ **Correct**: Workflows compose agents, procedures, and/or other workflows into multi-step processes. Agents remain atomic; workflows handle sequencing and composition.

## Misconception 4: "Principles can conflict"

❌ **Wrong**: Principles sometimes contradict each other.

✅ **Correct**: Principles complement each other. Apparent conflicts require nuanced application, not choosing one over another.

## Misconception 5: "Layer 2 and Layer 3 are the same"

❌ **Wrong**: Conventions and Development practices are interchangeable.

✅ **Correct**:

- **Layer 2 (Conventions)**: WHAT documentation rules (scope: docs/, plans/, web content)
- **Layer 3 (Development)**: HOW software practices (scope: source code, builds, git, agents)
- Layer 3 practices must respect Layer 2 conventions
