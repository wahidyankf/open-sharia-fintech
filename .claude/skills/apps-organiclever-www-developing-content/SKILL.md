---
name: apps-organiclever-www-developing-content
description: Guide for developing organiclever-www, the OrganicLever life journal at www.organiclever.com. Covers DDD bounded-context architecture, PGlite local-first storage, Effect TS, XState, Next.js 16 App Router, and Vercel deployment. Essential for development tasks on organiclever-www.
---

# organiclever-www Development Skill

## Purpose

Guidance for developing and managing **organiclever-www** — the OrganicLever life journal at www.organiclever.com, a Next.js 16 local-first productivity tracker using PGlite for in-browser storage, structured around DDD bounded contexts. Use when developing features, working with PGlite/Effect TS, or configuring Vercel deployment.

## Core Concepts and Directory Structure

Next.js 16 App Router app using DDD bounded contexts, PGlite local-first storage, Effect TS, and XState. See [Core Concepts and Directory Structure](./reference/core-concepts-and-directory-structure.md) for the tech stack and full layout.

## Bounded-Context Architecture

Every feature lives inside one bounded context under `src/contexts/<bc>/` with strict `domain`/`application`/`infrastructure`/`presentation` layer rules (ESLint `boundaries`, error severity). See [Bounded-Context Architecture](./reference/bounded-context-architecture.md) for layer rules, the feature-adding workflow, and XState placement.

## Design System

Uses the OrganicLever warm OKLCH design system — tokens from `@open-sharia-enterprise/web-ui-token`, components from `@open-sharia-enterprise/web-ui`. See [Design System](./reference/design-system.md) for token import chain, fonts, dark mode, key tokens, and component usage.

## Component Architecture and Next.js App Router Conventions

Components live inside the bounded context that owns them, not a global `src/components/`; `src/app/` holds only thin routing wrappers. See [Component Architecture and Next.js App Router Conventions](./reference/component-architecture-and-routing.md) for Server vs Client rules and the route structure.

## Vercel Deployment

Production branch `prod-organiclever-www` deploys to www.organiclever.com via Vercel auto-build after force-push from `main`. See [Vercel Deployment](./reference/vercel-deployment.md) for config, process, and why force-push is safe here.

## Comparison with Other Apps and Development Commands

Differs from ayokoding-web and ose-web mainly in its DDD bounded-context architecture and PGlite storage. See [Comparison with Other Apps and Development Commands](./reference/comparison-and-development-commands.md) for the comparison table and Nx/Docker Compose dev workflows.

## Common Patterns

See [Common Patterns](./reference/common-patterns.md) for the pattern for adding a feature to an existing bounded context and for using web-ui components.

## Content Validation Checklist and Common Mistakes

See [Content Validation Checklist and Common Mistakes](./reference/validation-checklist-and-common-mistakes.md) for the pre-commit checklist and common mistakes (business logic in page files, cross-context imports, missing `"use client"`, direct commits to the prod branch).

## Domain-Driven Design

Follows DDD with a canonical bounded-context registry, per-context glossaries, and `specs structure validate` `bc:`/`ul:` layer enforcement in `test:quick`. See [Domain-Driven Design](./reference/domain-driven-design.md) for registry links, layer rules, XState placement, cross-context call rules, and the glossary authoring rule.

## Reference Documentation

**Project Configuration**:

- [apps/organiclever-www/project.json](../../../apps/organiclever-www/project.json) - Nx project config
- [apps/organiclever-www/next.config.mjs](../../../apps/organiclever-www/next.config.mjs) - Next.js config
- [apps/organiclever-www/vercel.json](../../../apps/organiclever-www/vercel.json) - Vercel deployment config

**Infrastructure**:

- [infra/dev/organiclever-www/README.md](../../../infra/dev/organiclever-www/README.md) - Docker Compose setup for frontend
- [infra/dev/organiclever-www/docker-compose.yml](../../../infra/dev/organiclever-www/docker-compose.yml) - Service definition
- [infra/dev/organiclever-www/Dockerfile.web.dev](../../../infra/dev/organiclever-www/Dockerfile.web.dev) - Frontend container image

**Related Skills**:

- `repo-practicing-trunk-based-development` - Git workflow and branch strategy
- `swe-programming-typescript` - TypeScript coding standards

**Related Agents**:

- `apps-organiclever-app-web-deployer` - Deploys organiclever-www to production
- `swe-typescript-dev` - TypeScript/Next.js development
- `swe-e2e-dev` - E2E testing with Playwright

---

This Skill packages essential organiclever-www development knowledge for building and deploying the OrganicLever landing and promotional website at www.organiclever.com.
