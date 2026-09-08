---
description: Co-locate docs with code, review them, and validate them automatically.
when_to_use: Use as a checklist for where docs live and how they stay accurate.
---

# PASS: Best Practices — Co-location, Review, and Automated Validation

## 5. Keep Documentation Close to Code

**Location strategy**:

- **README files**: Next to the code they describe (every library, every app)
- **Inline comments**: In the source code (for complex logic, edge cases)
- **API documentation**: Generated from code comments (JSDoc, TypeScript doc comments)
- **High-level docs**: In `docs/` directory (conventions, explanations, tutorials)

**Why this works**: Co-location increases the chance documentation stays up-to-date. Developers see docs when changing code.

## 6. Make Documentation Reviewable

**Include documentation in code review**:

- README changes reviewed alongside code changes
- Inline comments reviewed as part of function implementation
- Convention documents reviewed before enforcement

**Why this works**: Review catches documentation errors, missing context, and unclear explanations before they spread.

## 7. Validate Documentation Automatically

**Use checker agents** to validate:

- PASS: README files exist in all libraries and apps
- PASS: Links in documentation are valid
- PASS: Code examples in docs actually work
- PASS: API documentation matches actual code signatures
- PASS: Convention documents exist for all enforced rules

**Why this works**: Automation catches documentation drift. Agents ensure docs stay accurate as code evolves.
