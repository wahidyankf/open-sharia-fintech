# Common Development Workflow — Reference Documentation Patterns and TDD

## Standard Project Documentation

**All language developers reference**:

- **[CLAUDE.md](../../../../CLAUDE.md)**: Primary guidance for all agents
- **[Monorepo Structure](../../../../docs/reference/monorepo-structure.md)**: Nx workspace organization
- **[Commit Messages Convention](../../../../repo-governance/development/workflow/commit-messages.md)**: Conventional Commits detailed guide
- **[Code Quality Convention](../../../../repo-governance/development/quality/code.md)**: Git hooks and automation
- **[Trunk Based Development](../../../../repo-governance/development/workflow/trunk-based-development.md)**: Git workflow philosophy
- **[Development Environment Setup](../../../../repo-governance/workflows/infra/development-environment-setup.md)**: Complete toolchain setup (doctor, rhino-cli env, all language runtimes)

## Language-Specific Documentation

Each language has authoritative coding standards in:

```
docs/explanation/software-engineering/programming-languages/[language]/README.md
```

A guide exists only for a language this repository builds on. Today that is:

- TypeScript: `docs/explanation/software-engineering/programming-languages/typescript/README.md`
- Rust: `docs/explanation/software-engineering/programming-languages/rust/README.md`
- F#: `docs/explanation/software-engineering/programming-languages/f-sharp/README.md`
- C#: `docs/explanation/software-engineering/programming-languages/c-sharp/README.md` (.NET interop with F#)

Read the parent
[`programming-languages/README.md`](../../../../docs/explanation/software-engineering/programming-languages/README.md)
index rather than assuming a guide exists for a given language.

**Each language README covers**:

1. Language idioms and patterns
2. Best practices for clean code
3. Anti-patterns to avoid
4. Framework-specific guidance
5. Testing strategies

## Test-Driven Development

TDD is **required** for all code changes across every language. Write the failing test first,
confirm it fails for the right reason, implement the minimum code to pass, then refactor. This rule
applies at every test level — unit, integration, E2E, contract, property/fuzz, snapshot/visual,
manual verification, performance, and accessibility. Pick the cheapest level that meaningfully
captures the behavior under change.

**Manual verification is TDD-compatible** when it is a written, dated, repeatable script with
discrete expected observations — not an informal "click around" check. Use Playwright MCP for UI
and `curl` for API verification. Promote manual scripts to automated tests whenever feasible.

**Mini-TDD passes are encouraged**: split a feature into multiple small Red→Green→Refactor cycles,
one per behavior. Each cycle is independently committable.

**Canonical reference**:
[Test-Driven Development Convention](../../../../repo-governance/development/workflow/test-driven-development.md)
— covers the full Red→Green→Refactor cycle, all test levels, the "Scope: Which Tests TDD Covers"
table, manual verification guidance, and applying TDD to delivery checklists.

See also:
[Manual Behavioral Verification](../../../../repo-governance/development/quality/manual-behavioral-verification.md),
[Three-Level Testing Standard](../../../../repo-governance/development/quality/three-level-testing-standard.md).
