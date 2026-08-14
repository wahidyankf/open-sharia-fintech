# Factual Validation — Common Mistakes and Best Practices

## Mistake 1: Using outdated sources

**Wrong**: Citing 5-year-old blog post for current syntax

**Right**: Check official documentation for latest version

## Mistake 2: Missing version context

**Wrong**: "React hooks were introduced recently"

**Right**: "React hooks were introduced in React 16.8 (February 2019)"

## Mistake 3: Trusting unofficial sources

**Wrong**: Using random Stack Overflow answer as sole source

**Right**: Verify with official docs, use SO for supplementary context

## Mistake 4: Not documenting verification source

**Wrong**: Marking [Verified] without citing source

**Right**: Always include verification source URL in finding

## Mistake 5: Conflating verification with subjective quality

**Wrong**: [Error] for "code style not following best practices"

**Right**: Use [Error] only for objective incorrectness (won't compile, wrong syntax)

## Validation Checklist

Before marking content as validated:

- [ ] Identified all objective, verifiable claims
- [ ] Used authoritative sources (official docs, registries)
- [ ] Documented verification source URLs
- [ ] Applied correct confidence classification
- [ ] Recorded validation date and expiry
- [ ] Classified criticality level
- [ ] Provided clear remediation steps for errors

## Batch Validation Workflow

1. **Extract claims**: Scan content for all verifiable claims
2. **Group by type**: Commands, versions, code examples, APIs
3. **Prioritize**: Critical paths first (install commands, quick starts)
4. **Validate systematically**: One claim type at a time
5. **Document findings**: Use standardized format
6. **Update metadata**: Record validation dates and sources

## Tool Usage Pattern

```
Step 1: WebSearch to find authoritative source
  Query: "npm install flags official documentation"
  Result: Multiple sources, identify official docs

Step 2: WebFetch to retrieve content
  URL: https://docs.npmjs.com/cli/v9/commands/npm-install
  Extract: Flag list, examples, usage patterns

Step 3: Compare and classify
  Claim vs Source → Determine classification
  Document finding with source citation
```
