---
title: "Implementation Checklist and References"
description: "The phased checklist for setting up new-repository documentation, plus related and further-reading references"
category: explanation
subcategory: conventions
tags:
  - conventions
  - documentation
  - open-source
  - repository-standards
created: 2026-04-04
when_to_use: "Read this when setting up documentation for a brand-new repository, or to find related conventions."
---

# Implementation Checklist and References

## Implementation Checklist

When setting up a new repository:

**Phase 1: Essential Files**

- [ ] `README.md` with all essential sections
- [ ] `LICENSE` file
- [ ] `.gitignore` appropriate for tech stack

**Phase 2: Contribution Infrastructure**

- [ ] `CONTRIBUTING.md` with setup and process
- [ ] `CODE_OF_CONDUCT.md` (use Contributor Covenant if no custom policy)
- [ ] `SECURITY.md` with vulnerability reporting

**Phase 3: Architecture Documentation**

- [ ] Create `docs/adr/` directory
- [ ] Create `docs/adr/README.md` index
- [ ] Write first ADR documenting major architectural decisions

**Phase 4: Continuous Improvement**

- [ ] `CHANGELOG.md` (once versioned releases begin)
- [ ] `AUTHORS.md` or contributor recognition
- [ ] Documentation review schedule
- [ ] Link checking automation

## Related Documentation

- [Diátaxis Framework](../../structure/diataxis-framework.md) — Organization of internal documentation
- [File Naming Convention](../../structure/file-naming.md) — Naming files within `docs/`
- [Linking Convention](../../formatting/linking.md) — How to link between documentation
- [Commit Message Convention](../../../development/workflow/commit-messages.md) — Git commit standards
- [Trunk Based Development](../../../development/workflow/trunk-based-development.md) — Git workflow

## Further Reading

**README Best Practices:**

- [GitHub README Best Practices](https://github.com/jehna/readme-best-practices)
- [Make a README](https://www.makeareadme.com/)
- [Standard README Specification](https://github.com/RichardLitt/standard-readme)

**Contributing Guidelines:**

- [How to Build a CONTRIBUTING.md](https://contributing.md/how-to-build-contributing-md/)
- [CONTRIBUTING.md Template](https://gist.github.com/PurpleBooth/b24679402957c63ec426)

**Architecture Decision Records:**

- [ADR GitHub Organization](https://adr.github.io/)
- [AWS ADR Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html)
- [Microsoft Azure ADR Guide](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)

**Financial Services Open Source:**

- [FINOS - Financial Services Open Source Foundation](https://www.finos.org/) (financial services as one enterprise domain)
- [State of Open Source in Financial Services](https://www.linuxfoundation.org/research/the-2023-state-of-open-source-in-financial-services)
