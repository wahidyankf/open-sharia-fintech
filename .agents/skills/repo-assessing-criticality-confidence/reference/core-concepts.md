# Criticality-Confidence — Core Concepts

## Two Orthogonal Dimensions

The system uses TWO independent dimensions:

**Criticality** (CRITICAL/HIGH/MEDIUM/LOW):

- Measures **importance and urgency**
- Answers: "How soon must this be fixed?"
- Set by **checker agents** during validation
- Objective criteria based on impact

**Confidence** (HIGH/MEDIUM/FALSE_POSITIVE):

- Measures **certainty and fixability**
- Answers: "How certain are we this needs fixing?"
- Assessed by **fixer agents** during re-validation
- Based on re-validation results

**Key Insight**: These dimensions are ORTHOGONAL - they measure different things and combine to determine priority.

## Four Criticality Levels

**🔴 CRITICAL** - Breaks functionality, blocks users, violates mandatory requirements

- Missing required fields (build breaks)
- Broken internal links (404 errors)
- Security vulnerabilities
- Syntax errors preventing execution
- MUST requirement violations

**🟠 HIGH** - Significant quality degradation, convention violations

- Wrong format (system functions but non-compliant)
- Accessibility violations (WCAG AA failures)
- SHOULD requirement violations
- Incorrect link format (works but violates convention)

**🟡 MEDIUM** - Minor quality issues, style inconsistencies

- Missing optional fields (minimal impact)
- Formatting inconsistencies
- Suboptimal structure (still functional)
- MAY/OPTIONAL requirement deviations

**🟢 LOW** - Suggestions, optimizations, enhancements

- Performance optimizations
- Alternative implementation suggestions
- Future-proofing recommendations
- Best practice suggestions (not requirements)

## Three Confidence Levels

**HIGH** - Objectively correct, safe to auto-fix

- Re-validation confirms issue exists
- Issue is objective and verifiable
- Fix is straightforward and safe
- No ambiguity, low risk

**MEDIUM** - Uncertain, requires manual review

- Re-validation is unclear or ambiguous
- Issue is subjective (human judgment needed)
- Multiple valid interpretations
- Context-dependent decision

**FALSE_POSITIVE** - Checker was wrong

- Re-validation clearly disproves issue
- Content is actually compliant
- Checker's detection logic flawed
- Report to improve checker
