# Claude Code skills

Skills are short, reusable guides that give an AI agent the right context at
the right moment. Think of them as a practical field guide: an agent can load
the relevant skill instead of carrying every repository convention into every
task. 🧭

If you are new here, begin with [AGENTS.md](../../AGENTS.md). Then use this
directory when you want to understand the guidance behind a task or add a new
skill.

## Find the right skill

| Your goal                                   | Look in                     |
| ------------------------------------------- | --------------------------- |
| Create, organize, or validate documentation | `docs-*` and `readme-*`     |
| Shape or check a delivery plan              | `plan-*` and `grill-me`     |
| Build or test an application                | `swe-*`                     |
| Work with a site’s content                  | `apps-*-developing-content` |
| Work on repository, CI, or agent practices  | `repo-*` and `ci-standards` |

Directory names are the live catalog. This guide intentionally avoids a copied
list of every skill, so a newly added skill is discoverable without leaving a
stale index behind.

## Read a skill before using it

Each skill has a `SKILL.md` file. Read it in full before acting on its
instructions; it may point to a small reference or a supplied script that is
part of the workflow. A typical package looks like this:

```text
skill-name/
├── SKILL.md       # required entry point
├── reference/     # optional focused detail
├── scripts/       # optional task helpers
└── assets/        # optional reusable material
```

Skills use progressive disclosure: their names help you locate the right
subject, while the full `SKILL.md` supplies the working rules only when that
subject is in scope.

## Source and platform behavior

`.claude/skills/` is the hand-authored source for these skill packages.
OpenCode reads compatible skills from this location; it does not need a copied
skill directory. Do not create or hand-edit `.opencode/skills/` mirrors.

When a skill changes, follow the source skill’s instructions and verify the
repository state with `npm run validate:sync`. See
[Platform bindings](../../docs/reference/platform-bindings.md) for the
cross-tool model.

## Keep a new skill useful

- Give it one clear job and a reader-friendly description.
- Put the essential procedure in `SKILL.md`; link to deeper material instead
  of repeating it.
- Prefer supplied scripts and templates over retyping large, fragile commands.
- State boundaries, especially around generated files, credentials, and
  destructive actions.

For the repository’s full expectations, see
[AI agents](../../repo-governance/development/agents/ai-agents.md) and the
[agent-development skill](agent-developing-agents/SKILL.md).
