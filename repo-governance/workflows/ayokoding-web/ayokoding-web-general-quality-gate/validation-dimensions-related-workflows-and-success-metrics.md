---
description: Lists what each of the three validators (content, facts, links) checks, which other workflows this one composes with, and the metrics tracked across executions.
when_to_use: Use when you need to know exactly what a given validator checks, which workflows to compose this with, or what metrics to track.
---

# Validation Dimensions, Related Workflows, and Success Metrics

## Validation Dimensions

### Content Validation (apps-ayokoding-www-general-checker)

- Content quality principles
- Bilingual consistency

### Facts Validation (apps-ayokoding-www-facts-checker)

- Technical accuracy using web verification
- Code examples correctness
- Tutorial sequences validity
- Bilingual factual consistency

### Links Validation (apps-ayokoding-www-link-checker)

- Internal link validity
- External link accessibility
- Broken link detection

## Related Workflows

This workflow can be composed with:

- Deployment workflows (validate before deploying ayokoding-web)
- Content creation workflows (validate after bulk content creation)
- Translation workflows (validate bilingual consistency)

## Success Metrics

Track across executions:

- **Average iterations to completion**: How many cycles typically needed
- **Success rate**: Percentage reaching zero findings
- **Findings by dimension**: Which validators find most issues
- **Fix success rate**: Percentage of fixes applied without errors
- **Common issue categories**: What problems appear most frequently
