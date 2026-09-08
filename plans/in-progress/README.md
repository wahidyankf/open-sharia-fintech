# In-Progress Plans

Active project plans currently being worked on.

## Choose the right route 🧭

Use this index to understand delivery work that is underway. For the product story or a first local
run, start with the [repository README](../../README.md) and [documentation hub](../../docs/README.md)
instead. Each plan README explains its outcome and boundaries; its `delivery.md` is the detailed
execution checklist.

## Active Plans

- **[lms-init](./lms-init/README.md)** — Initialize `ose-lms-be`, a Java 25 + Spring Boot REST
  backend for the OSE Learning Management System, with a hello-world and a health endpoint. Teaches
  the repository to build, format, test, and gate Java at all, and refactors the `rhino-cli` doctor
  tool inventory to be config-driven across `ose-public` and `ose-private`.
- **[islamic-be-init](./islamic-be-init/README.md)** — Stand up `islamic-be`, a Go 1.26 + Gin REST
  service for generic Islamic tools with a health endpoint, and its `islamic-be-e2e` Playwright-BDD
  suite. Adds the Go language lane on top of the shared surfaces `lms-init` generalizes; depends on
  that plan's DU1 and DU2.

## Instructions

**Idea Capture**: For ideas not ready for formal planning, write a two-pager in `../ideas/`.

**Naming**: Plans in `in-progress/` use NO date prefix — just the slug (e.g., `organiclever-web-responsive-breakpoints/`). `backlog/` also uses no date prefix, so moving from `backlog/` is a pure move.

When starting work on a plan:

1. Move the plan folder: `git mv backlog/[identifier]/ in-progress/[identifier]/` (no rename — neither stage carries a date prefix)
2. Update the plan's README.md status to "In Progress"
3. Add the plan to this list

When completing a plan:

1. Rename and move: `git mv in-progress/[identifier]/ done/YYYY-MM-DD__[identifier]/` using today's completion date
2. Update this list
