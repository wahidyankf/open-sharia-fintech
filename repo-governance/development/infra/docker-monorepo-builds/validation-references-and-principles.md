---
title: "Validation, References, and Principles"
description: How to validate a Docker monorepo build locally and in CI, related references, and the principles and conventions this pattern implements.
category: explanation
subcategory: development/infra
tags:
  - docker
  - monorepo
  - npm-workspaces
  - build
  - node_modules
created: 2026-03-28
when_to_use: Use when verifying a Docker build before pushing, or when tracing this convention back to the principles and conventions it implements.
---

# Validation, References, and Principles

## Validation

Verify that Docker builds work correctly before pushing:

```bash
# Build the Docker image locally
docker compose -f infra/dev/<app>/docker-compose.yml build

# Check that the build context resolves libs/ correctly
docker compose -f infra/dev/<app>/docker-compose.ci.yml config | grep context
```

The E2E CI workflow for each frontend app runs a full Docker build as part of its pipeline.
A green CI run on the app's E2E workflow confirms the Docker build and the injected libraries are
both working.

## References

**Related Development Standards:**

- [Nx Target Standards](../nx-targets.md) - Canonical target names and build dependency patterns
- [Vercel Deployment Convention](../vercel-deployment.md) - Related build context and dependency
  chain considerations

**Agents:**

- `rules-checker` - Can validate docker-compose context settings
- `rules-fixer` - Corrects docker-compose context misconfigurations

## Principles Implemented/Respected

This convention implements/respects the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  Shared library source must be explicitly injected into `node_modules/` inside the Docker build
  stage. Relying on npm workspace symlink resolution inside Docker is implicit and will fail. Every
  `COPY libs/...` line is a deliberate, visible declaration of the dependency.

- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**:
  The Docker image build must produce the same result locally and in CI. Explicit `COPY` injection
  and repo-root build context ensure the build is deterministic regardless of environment.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**:
  The root cause of module-not-found errors in Docker is symlink resolution failure, not a missing
  package. This pattern fixes the root cause by injecting source directly rather than patching
  around broken symlinks with workarounds like `--legacy-peer-deps` or volume mounts.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**:
  Checklists for adding new library dependencies and creating new shared libraries ensure that
  Docker build maintenance is systematic rather than ad hoc, reducing the chance of build failures
  discovered only in CI.

## Conventions Implemented/Respected

- **[File Naming Convention](../../../conventions/structure/file-naming.md)**: Dockerfile and
  docker-compose filenames follow kebab-case consistent with repository naming conventions.
- **[Indentation Convention](../../../conventions/formatting/indentation.md)**: All YAML and
  Dockerfile examples in this document use 2-space indentation per the project standard.
- **[Content Quality Principles](../../../conventions/writing/quality.md)**: Documentation uses
  active voice, proper heading hierarchy, and code blocks with language specifiers throughout.
