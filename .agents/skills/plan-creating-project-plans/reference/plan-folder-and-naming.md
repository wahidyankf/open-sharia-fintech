# Plans Folder Structure and Naming Convention

## Plans Folder Structure

```
plans/
├── ideas/                                # Two-pager idea briefs (one file per idea)
├── backlog/                              # Future work
│   └── project-name/                   # Planned but not started (no date prefix)
├── in-progress/                          # Active work
│   └── project-name/                    # Currently executing (no date prefix)
└── done/                                 # Completed work
    └── YYYY-MM-DD__project-name/        # Archived (completion date prefix)
```

## Plan Naming Convention

Naming is **stage-aware** — each lifecycle stage has its own rule:

| Stage          | Format                            | Date meaning    |
| -------------- | --------------------------------- | --------------- |
| `backlog/`     | `project-identifier/`             | No date prefix  |
| `in-progress/` | `project-identifier/`             | No date prefix  |
| `done/`        | `YYYY-MM-DD__project-identifier/` | Completion date |

**Rules** (identifier part, all stages):

- Separator between the completion date and identifier (`done/` only): Double underscore (`__`)
- Identifier: Lowercase, hyphen-separated, descriptive
- Trailing slash indicates directory
- Moving from `backlog/` → `in-progress/` is a pure move (neither carries a date prefix)
- Add the completion date prefix when moving from `in-progress/` → `done/`
