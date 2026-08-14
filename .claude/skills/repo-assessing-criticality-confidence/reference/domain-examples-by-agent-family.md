# Criticality-Confidence — Domain Examples by Agent Family

**docs-fixer** (Factual accuracy domain):

```markdown
**HIGH Confidence**:

- Broken command syntax verified by checker's cited sources
- Incorrect version number verified by checker's registry findings
- Wrong API method verified by checker's documentation review
- Broken internal link verified by file existence check

**MEDIUM Confidence**:

- Contradiction that may be context-dependent
- Outdated information where "outdated" is subjective
- Content duplication where duplication may be intentional

**FALSE_POSITIVE**:

- Checker flagged correct LaTeX as incorrect
- Checker flagged valid command as broken
```

**readme-fixer** (README quality domain):

```markdown
**HIGH Confidence**:

- Paragraph exceeding 5 lines (count is objective)
- Specific jargon patterns without context
- Acronym without expansion
- Passive voice patterns (pattern match)

**MEDIUM Confidence**:

- Overall tone assessment (subjective)
- Engagement quality (context-dependent)
- Sentence length appropriateness (judgment call)

**FALSE_POSITIVE**:

- Checker flagged technical term as jargon (domain-appropriate)
- Checker flagged intentional passive voice (style choice)
```

**docs-tutorial-fixer** (Tutorial quality domain):

```markdown
**HIGH Confidence**:

- Missing hands-on element verified by structure check
- Wrong tutorial type verified by content analysis
- Missing visual aid in complex section (objective criteria met)

**MEDIUM Confidence**:

- Narrative flow issues (subjective assessment)
- Pedagogical effectiveness (requires teaching expertise)
- Example clarity (reader-dependent)

**FALSE_POSITIVE**:

- Checker flagged advanced tutorial as beginner (correct level)
- Checker reported missing visual where text is sufficient
```
