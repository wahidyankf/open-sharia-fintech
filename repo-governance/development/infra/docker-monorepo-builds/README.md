---
description: "Patterns and pitfalls for building Docker images in an npm workspace monorepo"
when_to_use: "Read this index to find the right Docker Monorepo Build Patterns child document."
---

# Docker Monorepo Build Patterns

- [Workspace Symlinks and the Direct Injection Pattern](./workspace-symlinks-and-direct-injection-pattern.md) — Explains why npm workspace symlinks break inside Docker builds and the direct node_modules injection pattern that fixes it. Use when a Docker build inside this monorepo fails to resolve a workspace symlink or reports a shared library module not found.
- [Build Context and Transitive Dependency Hoisting](./build-context-and-dependency-hoisting.md) — Covers the repo-root build context requirement for docker-compose files and how to handle npm's transitive dependency hoisting in Docker builds. Use when a docker-compose build fails to find libs/ files, or when a Docker build fails on a module that is not a direct dependency of the app.
- [Checklists and Common Pitfalls](./checklists-and-common-pitfalls.md) — Checklists for adding a new libs/\* dependency or shared library, plus the four most common Docker monorepo build pitfalls and their fixes. Use when adding a new shared library dependency to an app's Dockerfile, creating a new shared library, or diagnosing a recurring Docker build failure.
- [Validation, References, and Principles](./validation-references-and-principles.md) — How to validate a Docker monorepo build locally and in CI, related references, and the principles and conventions this pattern implements. Use when verifying a Docker build before pushing, or when tracing this convention back to the principles and conventions it implements.
