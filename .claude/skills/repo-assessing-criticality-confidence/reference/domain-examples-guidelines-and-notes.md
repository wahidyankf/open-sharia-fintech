# Criticality-Confidence — Domain Examples: Guidelines, Placement, Anti-Patterns

## Guidelines for Creating Examples

**Be Specific**:

- Use concrete error types from your domain
- Reference actual verification methods
- Include pattern examples
- Show real scenarios

**Cover Common Cases**:

- Include the 3-5 most common HIGH confidence scenarios
- Include 2-3 common MEDIUM confidence scenarios
- Include 2-3 common FALSE_POSITIVE scenarios
- Don't try to be exhaustive (guidelines, not rules)

**Keep It Actionable**:

- Focus on verification methods: "verified by [method]"
- Explain ambiguity: "where [reason for uncertainty]"
- Show reasoning: "that may be [valid reason]"

**Domain-Appropriate**:

- docs-fixer: Command syntax, versions, APIs, links
- readme-fixer: Jargon, paragraphs, tone, engagement
- tutorial-fixer: Hands-on elements, flow, visuals
- link-fixer: Path format, target existence, redirects
- structure-fixer: Folder patterns, weights, organization

## Placement in Agent Files

Add "Domain-Specific Confidence Examples" section:

- After confidence level definitions
- Before re-validation guidelines
- In fixer agent files (not checker files)

## Benefits

✅ Reduces ambiguity in confidence assessment
✅ Provides concrete guidance for edge cases
✅ Improves consistency across similar fixers
✅ Documents domain conventions
✅ Helps new fixer implementations

## Anti-Patterns

❌ **Too Generic**: Examples that could apply to any domain
❌ **Too Exhaustive**: Trying to cover every possible scenario
❌ **No Verification Method**: Not explaining how to verify
❌ **Missing Context**: Not explaining why something is MEDIUM
❌ **In Skill**: Domain examples belong in agents, not Skills

## Key Takeaways

- Include domain-specific examples in fixer agents
- Cover HIGH/MEDIUM/FALSE_POSITIVE confidence cases
- Use concrete scenarios from your domain
- Explain verification methods
- Keep examples actionable and specific
- Place in fixer agents, not in this Skill
