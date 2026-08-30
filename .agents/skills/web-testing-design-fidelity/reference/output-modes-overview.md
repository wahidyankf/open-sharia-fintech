# Output Modes Overview

## Output Modes (Choose at Invocation)

The **`output-mode`** input selects where findings land. The evaluation methodology, finding anatomy,
and severity/priority scales are identical in every mode — only the **destination** changes.
`output-mode` defaults to `local-tmp`. Creating a plan requires literal `output-mode: plan`.

| `output-mode` | Destination                                                                                                         | Use when                                                                                                                                         |
| ------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `plan`        | A new plan folder under `plans/backlog/` (or `plans/in-progress/` when the caller passes `plan-stage: in-progress`) | The user explicitly authorized a tracked, promotable plan.                                                                                       |
| `delivery`    | Appended as unchecked task-list checkboxes into an **existing** plan's `delivery.md` (requires a `plan-path`)       | The findings belong to a plan already in flight — the mechanism behind the rule-15 near-end three-tester retest, folded back into the host plan. |
| `local-tmp`   | A single `findings.md` (+ an `evidence/` subfolder) under `local-tmp/<slug>/`                                       | The caller will fix the findings immediately in the same session and wants no plan paperwork. Ephemeral and gitignored.                          |

If `output-mode` is omitted, default to `local-tmp`. If `delivery` is selected without a `plan-path`, ask
for it before evaluating — never guess which plan to write into.
