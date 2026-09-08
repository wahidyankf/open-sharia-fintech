---
description: "Option C (extract shared pattern) and Option D (add to development conventions)."
when_to_use: "Use when extracting a shared pattern or adding to development conventions."
---

# Four Offload Options (C-D)

## Option C: Extract Common Pattern to Shared Convention

**When to use:** Multiple agents share the same detailed content (cross-file duplication).

**Process:**

1. Identify files with overlapping content (>50% similarity)
2. Determine if pattern represents a convention or standard
3. Create new convention doc OR expand existing one
4. Move shared pattern to convention (single source of truth)
5. Update all affected files with summary + link
6. Update convention index
7. Verify zero content loss

**Example - Content Format Standard:**

- **Before:** Diagram standards duplicated in `docs-maker.md`, `plan-maker.md`
- **After:**
  - New file: `repo-governance/conventions/formatting/diagrams.md` (comprehensive)
  - All agents: "Use Mermaid diagrams. See [Diagram Convention](../../../conventions/formatting/diagrams.md)" (2 lines each)
  - Savings: Eliminated duplication
- **Why Conventions Folder:** Diagrams are a content format standard, not development process

**Example - Development Process Standard:**

- **Before:** Testing strategy duplicated across multiple agents
- **After:**
  - New file: `repo-governance/development/quality/testing-strategy.md` (comprehensive)
  - All agents: "See `testing-strategy.md` for comprehensive testing guidelines" (2 lines each)
  - Savings: Eliminated duplication
- **Why Development Folder:** Testing is a development process, not content format

## Option D: Add to Development Conventions

**When to use:** Content relates to development processes, workflows, or team practices.

**Destination:** `repo-governance/development/`

**Examples of development content:**

- Code review checklists → `quality/code-review.md`
- Testing strategies → `quality/testing-strategy.md`
- Release process → `workflow/release-process.md`
- CI/CD workflows → `infra/cicd-workflow.md`
- Git workflows → `workflow/trunk-based-development.md`
- Commit conventions → `workflow/commit-messages.md`
- Agent standards → `agents/ai-agents.md`

**Existing development docs:**

- `agents/ai-agents.md` (AI agent standards)
- `workflow/commit-messages.md` (commit conventions)
- `workflow/trunk-based-development.md` (git workflow)

**Process:**

1. Determine if it's a development practice (git, commits, CI/CD, testing, code review, etc.)
2. Create new doc OR expand existing in `repo-governance/development/`
3. Use lowercase kebab-case filenames; place in the appropriate subdirectory so the hierarchy encodes the category
4. Move content to development convention (comprehensive detail)
5. Replace original with 2-5 line summary + link
6. Update development index (`repo-governance/development/README.md`)
7. Verify all cross-references work

**Example** (historical — `plan-executor.md` was later removed when plan execution moved into the plan-execution workflow orchestrated by the calling context):

- **Before:** Commit granularity examples in `plan-executor.md`
- **After:**
  - Updated: `repo-governance/development/workflow/commit-messages.md` (comprehensive)
  - `plan-executor.md`: "Split commits logically. See [Commit Messages Convention](../../workflow/commit-messages.md)" (2 lines)
  - Savings: 100+ lines
