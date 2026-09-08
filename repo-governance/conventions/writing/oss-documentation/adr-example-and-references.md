---
description: "A complete worked ADR (choosing Nx for monorepo management) and the external references this section is based on"
when_to_use: "Read this for a full worked example to model a new ADR on."
---

# ADRs: Full Example and References

## Example ADR

```markdown
# 0001. Use Nx for Monorepo Management

Date: 2025-11-20

## Status

Accepted

## Context

We are building an enterprise platform that will consist of multiple applications (web, mobile, APIs) and shared libraries (utilities, components, domain logic). We need to decide how to organize and build this codebase.

Options considered:

1. **Polyrepo** - Separate repositories for each app and library
2. **Manual Monorepo** - Single repository with custom build scripts
3. **Nx Monorepo** - Single repository with Nx build system
4. **Turborepo** - Single repository with Turborepo build system

Key factors:

- Need to share code between apps (authentication, domain models, UI components)
- Want fast builds (only rebuild what changed)
- TypeScript is primary language
- Small team (< 10 developers initially)
- Need clear dependency management

## Decision

We will use Nx as our monorepo build system.

Rationale:

- Nx provides excellent TypeScript support with automatic project references
- Built-in task caching dramatically speeds up CI/CD
- Dependency graph visualization helps understand system
- Affected detection rebuilds only changed projects
- Strong documentation and community support

## Consequences

## Positive Consequences

- **Fast Builds:** Task caching reduces build time from minutes to seconds for unchanged projects
- **Code Sharing:** Easy to share libraries across apps with TypeScript path mappings
- **Dependency Management:** Nx enforces proper dependency boundaries, preventing circular dependencies
- **Developer Experience:** Single `nx` command interface for all projects
- **Scalability:** Architecture supports growth from 5 to 50+ projects

## Negative Consequences

- **Learning Curve:** Team must learn Nx commands and concepts
- **Vendor Lock-in:** Migration away from Nx would require significant effort
- **Configuration Complexity:** Each project needs `project.json` configuration
- **Build Tool Dependency:** Reliant on Nx team for bug fixes and updates

## Neutral Consequences

- **Node.js Ecosystem:** Committed to Node.js/TypeScript ecosystem (not polyglot)
- **Repository Size:** Single repository will grow large over time
```

## References

Standards based on:

- [ADR GitHub Organization](https://adr.github.io/)
- [AWS ADR Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html)
- [Master ADRs: AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
- [Microsoft Azure ADR Guide](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
