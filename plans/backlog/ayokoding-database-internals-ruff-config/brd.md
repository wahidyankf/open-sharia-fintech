# Business Requirements — Database Internals Course Ruff Configuration

## Business Goal and Rationale

Keep executable course examples stable when repository formatting runs. Dense explanatory annotations
are part of the learning material; formatting that splits a statement from its annotation degrades
the teaching asset and risks drift from the matching Markdown snippets.

## Business Impact

The maintainer and course-authoring agents can run standard formatting without manual restoration of
the database-internals course corpus. Learners retain code examples whose explanations remain
attached to the relevant line.

## Affected Roles

- The maintainer, who reviews and merges course-content changes.
- Course-authoring and validation agents, which run formatting and content checks.
- Learners, who consume the rendered examples and their annotations.

## Success Measures

- Observable: the course has a root `ruff.toml` and `ruff format --check` exits zero for its Python
  corpus without modifying files.
- Observable: the plan diff is confined to the course-scoped configuration and its companion plan
  records; no manifest or runtime route changes occur.

## Non-Goals

- Reformatting existing Python files.
- Changing course lessons, drills, capstone behavior, or tests.
- Establishing a repository-wide Ruff policy.

## Risks and Mitigations

- A too-small line length could still wrap annotated examples. Measure the corpus before selecting
  the value and use `ruff format --check` as the acceptance test.
- A too-large value could exceed Ruff's supported configuration range. Keep the selected value within
  Ruff's parser limit and verify it with the installed formatter.
- A local configuration could accidentally affect another course. Place it only at the target course
  root and inspect the final diff before committing.
