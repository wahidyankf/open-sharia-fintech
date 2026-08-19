# Developing AI Agents — Documenting Model Selection and Cost Trade-offs

## Documenting Model Selection

### Model Selection Justification Pattern

Include in agent documentation to explain model choice:

**For Sonnet Agents**:

```markdown
**Model Selection Justification**: This agent uses `model: sonnet` because it requires:

- [Reasoning capability 1 - e.g., "Advanced reasoning to analyze technical claims"]
- [Reasoning capability 2 - e.g., "Deep web research to verify facts"]
- [Reasoning capability 3 - e.g., "Pattern recognition across multiple files"]
- [Decision-making type - e.g., "Complex decision-making for criticality levels"]
- [Orchestration need - e.g., "Multi-step validation workflow orchestration"]
```

**For Haiku Agents**:

```markdown
**Model Selection Justification**: This agent uses `model: haiku` because it performs straightforward tasks:

- [Simple task 1 - e.g., "Pattern matching to extract URLs"]
- [Simple task 2 - e.g., "Sequential URL validation via web requests"]
- [Simple task 3 - e.g., "File existence checks"]
- [Simple task 4 - e.g., "Cache management (read/write/compare)"]
- [Simple task 5 - e.g., "Simple status reporting"]
- No complex reasoning or content generation required
```

### Placement in Agent Files

Add justification near the top of agent file, after agent description:

```markdown
---
name: example-agent
description: Agent description here
model: sonnet
---

# Agent Name

## Agent Metadata

- **Role**: [Role description]

**Model Selection Justification**: [justification here]

[Rest of agent documentation]
```

## Cost and Performance Considerations

### Sonnet Trade-offs

**Costs**:

- Higher per-token cost (~10x haiku)
- Slower response time
- More resource-intensive

**Benefits**:

- Higher quality reasoning
- Better context understanding
- More accurate decisions
- Handles ambiguity well

**Use when**: Quality and accuracy more important than cost/speed

### Haiku Trade-offs

**Benefits**:

- Lower per-token cost (~10x cheaper)
- Faster response time
- Efficient for high-volume tasks

**Limitations**:

- Less sophisticated reasoning
- May struggle with ambiguity
- Better for deterministic tasks

**Use when**: Cost and speed more important than complex reasoning
