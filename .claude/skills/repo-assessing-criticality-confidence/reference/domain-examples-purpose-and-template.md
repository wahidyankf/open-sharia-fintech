# Criticality-Confidence — Domain Examples: Purpose and Template

Fixer agents should include domain-specific examples of HIGH/MEDIUM/FALSE_POSITIVE confidence assessments to guide re-validation decisions.

## Purpose of Domain Examples

**Why include domain-specific examples?**

- Provide concrete guidance for re-validation decisions
- Clarify what constitutes HIGH vs MEDIUM confidence in specific domain
- Help fixer agents make consistent confidence assessments
- Reduce ambiguity in edge cases
- Document domain conventions and patterns

**Where to include**: In fixer agent files (not in this Skill - keep examples domain-specific)

## Example Structure Template

```markdown
### Domain-Specific Confidence Examples

**HIGH Confidence** (Apply automatically):

- [Objective error type 1] verified by [verification method]
- [Objective error type 2] verified by [verification method]
- [Pattern-based error] verified by [pattern check]
- [File-based error] verified by [file check]

**MEDIUM Confidence** (Manual review):

- [Subjective issue 1] that may be [context-dependent reason]
- [Ambiguous issue] where [ambiguity explanation]
- [Quality judgment] requiring [human judgment reason]
- [Context-dependent issue] that could be [valid reason]

**FALSE_POSITIVE** (Report to checker):

- Checker flagged [correct thing] as incorrect ([reason for false positive])
- Checker reported [missing thing] that actually exists ([reason])
- Checker [misunderstood] [context explanation]
```
