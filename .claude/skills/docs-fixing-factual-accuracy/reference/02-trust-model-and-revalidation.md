# Trust Model and Re-Validation Guidelines

## Trust Model: Checker Verifies, Fixer Applies

**CRITICAL DESIGN**: This agent does NOT have WebFetch or WebSearch tools.

**Why No Web Tools?**

1. **Separation of Concerns**: Checker does expensive web verification once, fixer applies validated
   fixes
2. **Performance**: Avoid duplicate web requests (checker already verified)
3. **Clear Responsibility**: Checker = research/verification, Fixer = application/execution
4. **Audit Trail**: Checker documents all verification sources in audit report
5. **Trust Model**: Fixer trusts checker's verification work

**How Fixer Re-validates Without Web Access**:

- **Read audit report**: Extract checker's documented verification sources
- **Analyze findings**: Review checker's cited URLs, registry data, API docs
- **Pattern matching**: Apply known patterns for common errors
- **File-based checks**: Verify syntax, format, consistency without web
- **Conservative approach**: When in doubt, classify as MEDIUM (manual review)

**When Fixer Doubts a Finding**:

- Don't re-fetch: Fixer cannot independently verify web sources
- Classify MEDIUM or FALSE_POSITIVE: Flag for manual review
- Document reasoning: Explain why checker's finding seems questionable
- Suggest improvement: Provide actionable feedback for checker

## Re-Validation Guidelines

**Key Principle**: Only objective, verifiable errors get HIGH confidence. Everything else requires
human judgment.

### Factual Accuracy Re-Validation

**Command Syntax**:

- Re-validate using checker's documented verification
- Extract checker's source URL and conclusion
- Verify command components match checker's findings
- **HIGH**: Command verified against official docs (objective error)
- **MEDIUM**: Command might be deprecated but unclear (needs research)
- **FALSE_POSITIVE**: Checker flagged valid command (checker error)

**Version Numbers**:

- Re-validate using checker's registry findings
- Extract checker's latest version and all versions
- Compare claimed vs actual per checker's verification
- **HIGH**: Version verifiably wrong (objective error)
- **MEDIUM**: Version old but claim doesn't say "latest" (editorial judgment)
- **FALSE_POSITIVE**: Checker flagged correct version (checker error)

**Feature Existence**:

- Re-validate using checker's documentation verification
- Extract checker's doc URL and conclusion
- Review checker's documented results
- **HIGH**: Feature doesn't exist in official docs (objective error)
- **MEDIUM**: Feature exists but named differently (terminology issue)
- **FALSE_POSITIVE**: Checker missed the feature (checker error)

### Code Example Re-Validation

- Extract API calls and methods from code snippet
- Read checker's API documentation verification
- Compare code usage with checker's documented findings
- **HIGH**: API method doesn't exist per checker's verification
- **MEDIUM**: API deprecated but still functional (judgment call)
- **FALSE_POSITIVE**: Checker incorrectly flagged valid API

### Contradiction Detection Re-Validation

- Extract both conflicting statements
- Analyze context: Are statements about different scenarios?
- Check if contradiction is real or context-dependent
- **HIGH**: Contradiction is objective and unambiguous
- **MEDIUM**: Contradiction may be contextual or intentional
- **FALSE_POSITIVE**: Statements apply to different contexts (not contradictory)

### Outdated Information Re-Validation

- Read checker's "outdated" claim and verification
- Analyze if information is objectively obsolete or still valid
- Consider if "outdated" is factual or subjective judgment
- **HIGH**: Information objectively obsolete (e.g., service shut down)
- **MEDIUM**: Information old but "outdated" is subjective
- **FALSE_POSITIVE**: Information still current (checker error)
