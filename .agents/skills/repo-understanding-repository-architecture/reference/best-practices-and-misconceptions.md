# Repository Architecture — Best Practices and Common Misconceptions

## Best Practices

### When Creating New Conventions

1. **Check principles first** - Which principle does this implement?
2. **Add traceability section** - "Principles Implemented/Respected"
3. **Document in Conventions Index** - Add to README.md
4. **Consider agent impact** - Which agents need to enforce this?

### When Creating New Development Practices

1. **Check both principles AND conventions** - What do you implement/respect?
2. **Add both traceability sections** - Principles AND Conventions
3. **Document in Development Index** - Add to README.md
4. **Consider automation** - Git hooks? AI agents?

### When Creating New Agents

1. **Identify governing layers** - Which conventions/practices does this enforce?
2. **Define atomic responsibility** - One clear purpose
3. **Choose tools carefully** - Match to task (Read-only, Write, Edit, Bash)
4. **Document in Agents Index** - Add to README.md

### When Creating Workflows

1. **Identify step sequence** - What agents, procedures, and/or nested workflows needed, in what order?
2. **Define termination criteria** - When does workflow complete?
3. **Add approval checkpoints** - Where does user review?
4. **Document state management** - How does state flow between steps?

## Common Misconceptions

### Misconception 1: "Skills are Layer 4.5"

❌ **Wrong**: Skills are not a layer between Development and Agents.

✅ **Correct**: Skills are delivery infrastructure (like AGENTS.md), not governance layer.

### Misconception 2: "Agents can ignore conventions if skilled"

❌ **Wrong**: Skills provide knowledge but don't override governance.

✅ **Correct**: Agents MUST follow conventions. Skills help agents understand conventions better.

### Misconception 3: "Workflows replace agents"

❌ **Wrong**: Workflows don't replace agents, they orchestrate them.

✅ **Correct**: Workflows compose multiple agents into multi-step processes.

### Misconception 4: "Principles can conflict"

❌ **Wrong**: Principles sometimes contradict each other.

✅ **Correct**: Principles complement each other. Apparent conflicts require nuanced application, not choosing one over another.
