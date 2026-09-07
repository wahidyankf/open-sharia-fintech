---
description: "The three artifacts requiring sync: C4 diagrams, Gherkin feature files, and specs/ README files."
when_to_use: "Use when deciding which spec artifact a code change must also update."
---

# What Must Stay in Sync

## C4 Diagrams

Each owner's `specs/apps/<product>/<owner>/architecture.md` documents that surface at the context, container, and component levels — the three C4 zoom levels are sections of one document, not three folders. It must reflect the actual system at all times.

**Update an owner's `architecture.md` when:**

- Adding or removing an application (`apps/`) or library (`libs/`)
- Changing the runtime technology of an existing app (e.g., Astro → Next.js, Go/Gin → Go/Fiber)
- Introducing a new data store (PostgreSQL database, Redis cache, S3 bucket)
- Adding or removing a new external integration (third-party API, authentication provider, CDN)
- Changing how containers communicate (new HTTP boundary, new message queue, new tRPC procedure that crosses a container boundary)
- Changing the deployment target in a way that creates a new runtime boundary (e.g., a serverless function split off from a monolith)

**C4 scope per level:**

- **Context diagram**: Update when adding/removing actors, external systems, or top-level system boundaries
- **Container diagram**: Update when adding/removing deployable units, data stores, or major technology changes
- **Component diagram**: Update when adding/removing tRPC routers, REST resource groups, major page groups, or significant internal subsystems

## Gherkin Feature Files

Gherkin feature files define the observable behaviour of the system from a stakeholder perspective. They must describe what the system actually does.

**Update Gherkin specs when:**

- Adding a new REST endpoint or tRPC procedure — add a scenario describing its behaviour
- Removing an endpoint or procedure — remove or archive the corresponding scenario
- Changing the HTTP method, path, request shape, or response shape of an existing endpoint
- Changing authentication or authorization requirements for an endpoint
- Changing validation rules that affect the observable API contract (e.g., a field becomes required, a maximum length changes)
- Adding or removing a major UI page or flow that has acceptance criteria

**Do not add Gherkin scenarios for:**

- Internal implementation details (private functions, internal state machines)
- Framework-level behaviour that is not part of the application's acceptance criteria

## specs/ README Files

README files inside `specs/apps/*/` and `specs/libs/*/` describe project structure, BDD framework in use, and how feature files are organized. They must reflect current reality.

**Update specs README files when:**

- Renaming an app or lib — rename the corresponding `specs/` folder and update its README
- Removing an app or lib — remove the corresponding `specs/` folder
- Changing the BDD framework for a project (e.g., Godog → Cucumber)
- Reorganizing feature files within a spec folder (new domain groupings, renamed subdirectories)

## specs/README.md

The root `specs/README.md` lists all projects with specs. Update it when:

- Adding a new project that requires specs
- Removing a project
- Renaming a project
