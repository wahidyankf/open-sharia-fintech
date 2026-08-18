---
title: "Frontmatter Requirements and Quality Checklist"
description: "Specifies the required frontmatter fields for overview and level pages, plus the start of the pre-publish quality checklist covering coverage, self-containment, and code quality."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - education
  - code-first
created: 2025-12-25
when_to_use: "Read before publishing by-example content, to confirm frontmatter is complete and every quality checklist item is satisfied."
---

# Frontmatter Requirements and Quality Checklist

## Frontmatter Requirements

### Overview Page

```yaml
---
title: "Overview"
date: YYYY-MM-DDTHH:MM:SS+07:00
weight: 10000000
description: "Learn {Language/Framework} through {N}+ annotated code examples covering 95% of the language - ideal for experienced developers"
tags: ["language-tag", "tutorial", "by-example", "examples", "code-first"]
---
```

### Tutorial Level Pages

```yaml
---
title: "Beginner" | "Intermediate" | "Advanced"
date: YYYY-MM-DDTHH:MM:SS+07:00
weight: 10000001 | 10000002 | 10000003
description: "Examples {range}: {Topic summary} ({coverage}% coverage)"
tags: ["language-tag", "tutorial", "by-example", "level-tag", "topic-tags"]
---
```

## Quality Checklist

Before publishing by-example content, verify:

### Coverage

- [ ] 75-85 total examples across three levels
- [ ] Beginner: 27-30 examples (0-40% coverage)
- [ ] Intermediate: 20-30 examples (40-75% coverage, varies by language)
- [ ] Advanced: 25-28 examples (75-95% coverage)
- [ ] 95% coverage of language/framework achieved
- [ ] Coverage gaps documented and justified

### Self-Containment

- [ ] Every beginner example is fully standalone
- [ ] Every intermediate example runs without external references
- [ ] Every advanced example is copy-paste-runnable
- [ ] All imports and helper code included

### Code Quality

- [ ] Every significant line has inline comment
- [ ] Annotation density meets target PER EXAMPLE (1.0-2.25 comment lines per code line, reduce if >2.5, enhance if <1.0)
- [ ] Annotations explain WHY (not just WHAT)
- [ ] Pattern matching branches documented (which matched, why)
- [ ] Execution flow decisions shown (if/case branches, timing)
- [ ] Best practices indicated (PASS: GOOD vs FAIL: BAD where relevant)
- [ ] `// =>` or `# =>` notation shows outputs and states
- [ ] Variable states documented at each step
- [ ] Code is formatted with standard tools
- [ ] Examples compile/run successfully
