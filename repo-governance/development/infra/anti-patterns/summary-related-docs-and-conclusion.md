---
description: Summary table of all anti-patterns, related documentation links, the closing anti-pattern checklist, and the principles/conventions this document implements.
when_to_use: Use for a quick-reference table of every anti-pattern and solution, or to find related conventions and principles documents.
---

# Anti-Patterns Summary, Related Documentation, and Conclusion

## Summary of Anti-Patterns

| Anti-Pattern                          | Problem                    | Solution                           |
| ------------------------------------- | -------------------------- | ---------------------------------- |
| **Scattered Temporary Files**         | Repository clutter         | Use designated directories         |
| **Placeholder UUIDs**                 | Defeats audit trail        | Generate real UUIDs and timestamps |
| **Buffering Reports**                 | Lost during compaction     | Write progressively                |
| **Missing Tools**                     | Can't generate reports     | Add Write and Bash tools           |
| **Global Tracking**                   | Race conditions            | Scope-based tracking               |
| **Mismatched Reports**                | Breaks audit trail         | Use same UUID and timestamp        |
| **Unrelated actions in one scenario** | Hides independent outcomes | Split at the behaviour boundary    |
| **Vague Criteria**                    | Not testable               | Use Gherkin format                 |
| **Never Cleaning Up**                 | Directory bloat            | Periodic cleanup                   |
| **Conversation-Only Output**          | Lost during compaction     | Write report files                 |
| **Undocumented Temp Files**           | Purpose unclear            | Add README documentation           |

## Related Documentation

- [Temporary Files Convention](../temporary-files.md) - Complete temporary file standards
- [Acceptance Criteria Convention](../acceptance-criteria.md) - Gherkin acceptance criteria guide
- [Best Practices](../best-practices.md) - Recommended patterns
- [Explicit Over Implicit Principle](../../../principles/software-engineering/explicit-over-implicit.md) - Why clear organization matters

## Conclusion

Avoiding these anti-patterns ensures:

- Organized temporary file structure
- Traceable audit trails
- Persistent report generation
- Testable acceptance criteria
- Concurrent execution support
- Clean workspace hygiene
- Clear documentation
- Reliable infrastructure

When managing infrastructure, ask: **Am I adding clarity or clutter?** If clutter, refactor to follow infrastructure development best practices.

## Principles Implemented/Respected

- **Explicit Over Implicit**: Clear file locations, documented purposes
- **Automation Over Manual**: Progressive writing, automated tracking
- **Simplicity Over Complexity**: Designated directories, simple naming

## Conventions Implemented/Respected

- **[File Naming Convention](../../../conventions/structure/file-naming.md)**: Report files and temporary files follow standardized naming patterns
- **[Content Quality Principles](../../../conventions/writing/quality.md)**: Clear, structured documentation of anti-patterns and solutions
- **[Linking Convention](../../../conventions/formatting/linking.md)**: GitHub-compatible links to related documentation
