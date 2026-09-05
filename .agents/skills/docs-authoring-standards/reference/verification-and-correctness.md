# Verification and Correctness

## Foundational Principle: Documentation First

You operate under the
[Documentation First](../../../../repo-governance/principles/content/documentation-first.md)
principle: documentation is mandatory, not optional. Write it before or with code, never
"we'll document it later" — "self-documenting code" shows HOW, documentation explains WHY.
Every repository, library, and application needs a README; every convention needs an
explanation document; every architectural decision needs rationale documentation.

## Critical Requirement: Accuracy and Correctness

Correctness is non-negotiable. Always verify information through code reading, testing, and
external source validation rather than relying on assumptions or outdated knowledge.

### Verification Requirements

- **Code & Implementation**: Read actual source code, verify function signatures, test examples
- **File System**: Verify paths exist using Glob, validate link targets, confirm directory
  structures
- **External Information**: Per the
  [Web Research Delegation Convention](../../../../repo-governance/conventions/writing/web-research-delegation.md),
  delegate multi-page research (2+ `WebSearch` calls or 3+ `WebFetch` calls for one claim) to
  `web-researcher` and use its cited findings. Use in-context `WebSearch`/`WebFetch` only for
  single-shot verification against a known authoritative URL. Cite sources with URLs and dates.
- **Commands & Examples**: Test all command sequences, run code examples, verify outputs
- **Links & References**: Check internal links point to existing files with `.md` extension
- **Versions & Dependencies**: State version requirements explicitly
- **Consistency**: Match terminology to source code; cite file paths (e.g., `src/auth/login.ts:42`)

### Correctness Verification Checklist

Before considering documentation complete:

- [ ] File name follows naming convention (plain kebab-case; category encoded by directory)
- [ ] Nested bullets use 2 spaces per level (not tabs)
- [ ] Frontmatter uses 2 spaces per level (not tabs), including all nested fields
- [ ] Code blocks use language-idiomatic indentation (2 spaces for JS/TS/YAML/JSON/CSS/Bash,
      4 for Python, tabs only for Go)
- [ ] All code examples tested; all file paths verified against actual structure
- [ ] All internal links verified to exist, correct relative paths, `.md` extension
- [ ] Version numbers, command options, and parameters current
- [ ] No assumptions left unstated; terminology consistent with source code and existing docs
- [ ] Step-by-step instructions followed completely and verified
- [ ] Edge cases and limitations documented
- [ ] Accuracy checked against source code and actual behaviour
