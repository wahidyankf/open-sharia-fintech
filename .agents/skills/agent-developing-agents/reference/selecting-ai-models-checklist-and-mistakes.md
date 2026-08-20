# Developing AI Agents — Model Selection Checklist and Common Mistakes

## Decision Checklist

Before selecting a model, ask:

1. **Does the task require judgment calls?**
   - Yes → Sonnet
   - No → Haiku

2. **Are there multiple valid interpretations?**
   - Yes → Sonnet
   - No → Haiku

3. **Does it need deep analysis of context?**
   - Yes → Sonnet
   - No → Haiku

4. **Will it make complex decisions?**
   - Yes → Sonnet
   - No → Haiku

5. **Is it high-volume, low-complexity?**
   - Yes → Haiku
   - No → Sonnet

6. **Does cost matter more than quality?**
   - Yes → Haiku
   - No → Sonnet

## Common Mistakes

❌ **Using Sonnet for Simple Tasks**:

```yaml
# Overkill - use haiku
model: sonnet # Just checking if files exist
```

❌ **Using Haiku for Complex Analysis**:

```yaml
# Insufficient - use sonnet
model: haiku # Analyzing code quality and architecture
```

✅ **Match Model to Task Complexity**:

```yaml
# Simple pattern matching
model: haiku

# Complex reasoning
model: sonnet
```

## Key Takeaways

- **Sonnet** = Complex reasoning, sophisticated analysis, multi-step orchestration
- **Haiku** = Simple tasks, pattern matching, straightforward validation
- **Document rationale** = Include model selection justification in agent files
- **Consider trade-offs** = Balance cost/speed vs quality/capability
- **Match complexity** = Use appropriate model for task requirements
- **When in doubt** = Choose sonnet for quality, haiku for speed/cost

Proper model selection ensures optimal performance, cost-effectiveness, and task completion quality.
