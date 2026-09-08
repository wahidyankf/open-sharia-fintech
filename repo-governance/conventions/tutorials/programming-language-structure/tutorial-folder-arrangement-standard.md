---
description: The manual, non-pedagogical weight-ordered arrangement standard for tutorial folders (overview, setup, quick-start, by-example, by-concept) across all content types.
when_to_use: Use when arranging or validating tutorial folder order and weights for any content type (languages, infrastructure tools, data tools, platforms).
---

# Tutorial Folder Arrangement Standard

**CRITICAL**: All topics with by-example tutorials MUST follow this specific arrangement order:

1. **overview** (weight: 100000)
2. **initial-setup** (weight: 100001)
3. **quick-start** (weight: 100002)
4. **by-example** (weight: 100003)
5. **by-concept** (weight: 100004) - OPTIONAL (only for topics that originally had it)

**Key Rules**:

- **Manual arrangement**: Tutorial structure is arranged MANUALLY by content creators, NOT automatically by agents
- **NO automatic "by pedagogical" ordering**: Agents should NOT enforce automatic ordering patterns beyond this standard arrangement
- **by-concept is optional**: Not all topics require by-concept path (some may have only by-example)
- **Consistent weight values**: Use the exact weight values shown above for predictable navigation ordering

**Rationale**:

- **Learner-first ordering**: Overview → Setup → Quick touchpoints → Example-driven learning → Narrative-driven learning
- **Progressive complexity**: Foundational setup before learning paths, code examples before deep explanations
- **Flexibility**: by-concept optional allows topics to provide by-example-only when appropriate
- **Explicit control**: Content creators manually arrange structure based on pedagogical goals

**Examples Across Content Types**:

**Programming Languages** (Java, Golang, Elixir):

```
tutorials/
├── _index.md                # weight: 100002
├── overview.md              # weight: 100000
├── initial-setup.md         # weight: 100001
├── quick-start.md           # weight: 100002
├── by-example/              # weight: 100003
└── by-concept/              # weight: 100004
```

**Infrastructure Tools** (Ansible, Terraform):

```
tutorials/
├── _index.md                # weight: 100002
├── overview.md              # weight: 100000
├── initial-setup.md         # weight: 100001
├── quick-start.md           # weight: 100002
├── by-example/              # weight: 100003
└── by-concept/              # weight: 100004 (OPTIONAL)
```

**Data Tools** (PostgreSQL, Redis):

```
tutorials/
├── _index.md                # weight: 100002
├── overview.md              # weight: 100000
├── initial-setup.md         # weight: 100001
├── quick-start.md           # weight: 100002
├── by-example/              # weight: 100003
└── by-concept/              # weight: 100004 (OPTIONAL)
```

**Platforms** (AWS, Google Cloud):

```
tutorials/
├── _index.md                # weight: 100002
├── overview.md              # weight: 100000
├── initial-setup.md         # weight: 100001
├── quick-start.md           # weight: 100002
├── by-example/              # weight: 100003
└── by-concept/              # weight: 100004 (OPTIONAL)
```

**Agent Responsibilities**:

- **Validation**: Agents SHOULD validate that tutorial folders follow this standard arrangement
- **NO automatic reordering**: Agents MUST NOT automatically reorder tutorials into "pedagogical" patterns
- **Respect manual arrangement**: Content creators control the structure intentionally
