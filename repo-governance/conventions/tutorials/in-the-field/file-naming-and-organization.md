---
description: The directory structure, file naming pattern, and topic-weight numbering scheme for In-the-Field guide files.
when_to_use: Use when creating or naming a new In-the-Field guide file and assigning it a topic weight.
---

# File Naming and Organization

## Directory Structure

```
content/
└── en/
    └── learn/
        └── software-engineering/
            └── programming-language/
                └── {language}/
                    └── in-the-field/
                        ├── _index.md              # Landing page
                        ├── overview.md            # What is in-the-field
                        ├── test-driven-development.md
                        ├── behaviour-driven-development.md
                        ├── build-tools.md
                        ├── ci-cd.md
                        ├── docker-and-kubernetes.md
                        ├── authentication.md
                        ├── security-practices.md
                        └── [topic].md             # 20-40 guides
```

## File Naming Pattern

- Topic-based naming: `[topic-kebab-case].md`
- Examples: `test-driven-development.md`, `docker-and-kubernetes.md`, `sql-database.md`
- NO numbering (guides are independent, not sequential)

## Topic Weights

**Weight assignment** (controls navigation order):

```yaml
overview.md:  weight: 10000000  # Always first (what is in-the-field)
topic-1.md:   weight: 10000001  # First topic in pedagogical progression
topic-2.md:   weight: 10000002  # Second topic
# ... rest of topics following pedagogical progression
```

**Universal Pedagogical Ordering Principles**:

Apply these principles to determine optimal topic progression for ANY domain (programming languages, DevOps, cloud platforms, databases, frameworks, etc.):
