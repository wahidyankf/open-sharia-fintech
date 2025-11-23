---
title: "AI Agents Convention"
description: Standards for creating and managing AI agents in the .claude/agents/ directory
category: explanation
tags:
  - ai-agents
  - conventions
  - claude-code
  - development
  - standards
created: 2025-11-23
updated: 2025-11-23
---

# AI Agents Convention

This document defines the standards for creating, structuring, and managing AI agents in the `.claude/agents/` directory. All agents must follow these conventions to ensure consistency, maintainability, and proper integration with the project.

## Overview

### What are AI Agents?

AI agents in this project are specialized Claude Code assistants defined in the `.claude/agents/` directory. Each agent has:

- **Specific expertise** in a particular domain or task
- **Defined tool permissions** limiting what operations it can perform
- **Clear responsibilities** to avoid overlap with other agents
- **Integration with project conventions** through references to CLAUDE.md and convention documents

### Why We Need Agent Conventions

Without standards, agents can become:

- **Inconsistent** in structure and quality
- **Overlapping** in responsibilities, causing confusion
- **Insecure** through tool permission creep
- **Unmaintainable** as the project grows

This convention ensures all agents are:

- ✅ Well-structured and documented
- ✅ Single-purpose and focused
- ✅ Secure through explicit tool permissions
- ✅ Consistent with project standards

### Scope

This convention applies to:

- All agent files in `.claude/agents/`
- References to agents in `CLAUDE.md`
- Agent validation rules in `repo-rule-checker`

## Agent File Structure

### Required Frontmatter

Every agent file MUST begin with YAML frontmatter containing four required fields:

```yaml
---
name: agent-name
description: Expert in X specializing in Y. Use when Z.
tools: Read, Glob, Grep
model: inherit
---
```

**Field Definitions:**

1. **`name`** (required)
   - Must match the filename (without `.md` extension)
   - Use kebab-case format
   - Should be descriptive and action-oriented
   - Examples: `doc-writer`, `repo-rule-checker`, `api-validator`

2. **`description`** (required)
   - One-line summary of when to use this agent
   - Should complete: "Use this agent when..."
   - Be specific about the agent's expertise
   - Example: `"Expert documentation writer specializing in Obsidian-optimized markdown and Diátaxis framework. Use when creating, editing, or organizing project documentation."`

3. **`tools`** (required)
   - Comma-separated list of allowed tool names
   - Explicit whitelist for security and clarity
   - Only include tools the agent needs
   - Common tools: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`

4. **`model`** (required)
   - Specifies which model to use for this agent
   - Options: `inherit` (default) or specific model name (e.g., `sonnet`)
   - Use `inherit` unless there's a specific need
   - See "Model Selection Guidelines" below for decision criteria

### Document Structure

After frontmatter, agents should follow this structure:

```markdown
# [Agent Name] Agent

[One-paragraph introduction describing the agent's role]

## Core Expertise / Core Responsibility

[Clear statement of the agent's primary purpose and capabilities]

## [Domain-Specific Sections]

[Detailed guidelines, standards, checklists, examples specific to this agent]

## Reference Documentation

[Links to CLAUDE.md, conventions, and related documentation]
```

**Required Sections:**

1. **Title (H1)**: Must follow pattern `# [Name] Agent`
2. **Core Expertise/Responsibility (H2)**: Clear purpose statement
3. **Reference Documentation (H2)**: Links to relevant conventions and guidance

**Optional Sections:**

- Detailed guidelines
- Examples and anti-patterns
- Checklists
- Decision trees
- Troubleshooting

## Agent Naming Conventions

### File Naming

Agent files follow kebab-case naming:

```
✅ Good:
- doc-writer.md
- repo-rule-checker.md
- api-validator.md
- test-runner.md

❌ Bad:
- DocWriter.md (PascalCase)
- doc_writer.md (snake_case)
- documentation-writer-agent.md (redundant suffix)
```

### Naming Guidelines

1. **Be descriptive** - Name should indicate the agent's purpose
2. **Be concise** - Avoid unnecessary words
3. **Be action-oriented** - Use verbs when appropriate (`writer`, `checker`, `validator`)
4. **Avoid redundancy** - Don't add `-agent` suffix (implied by location)
5. **Match frontmatter** - `name` field must match filename

### Agent Name vs Description

- **Name**: Short identifier used in file system and frontmatter
- **Description**: Detailed explanation of when and how to use

Example:

```yaml
name: doc-writer # Short, kebab-case
description: Expert documentation writer specializing in Obsidian-optimized markdown and Diátaxis framework. Use when creating, editing, or organizing project documentation. # Detailed usage guidance
```

## Tool Access Patterns

Tool permissions follow the **principle of least privilege**: agents should only have access to tools they actually need.

### Pattern 1: Read-Only Agents

**Tools**: `Read, Glob, Grep`

**Use for:**

- Validation and checking
- Analysis and reporting
- Consistency verification
- Code review (without modifications)

**Example:**

```yaml
---
name: repo-rule-checker
description: Validates consistency between agents, CLAUDE.md, conventions, and documentation.
tools: Read, Glob, Grep
model: inherit
---
```

**Why read-only?**

- These agents should never modify files
- Read-only access prevents accidental changes
- Security through explicit restriction

### Pattern 2: Documentation Agents

**Tools**: `Read, Write, Edit, Glob, Grep`

**Use for:**

- Creating documentation
- Editing existing docs
- Organizing documentation files
- Managing documentation structure

**Example:**

```yaml
---
name: doc-writer
description: Expert documentation writer specializing in Obsidian-optimized markdown and Diátaxis framework.
tools: Read, Write, Edit, Glob, Grep
model: sonnet
---
```

**Why these tools?**

- `Read`: Understand existing documentation
- `Write`: Create new files
- `Edit`: Modify existing files
- `Glob`/`Grep`: Find and search documentation
- **No Bash**: Documentation doesn't need shell access

### Pattern 3: Development Agents

**Tools**: `Read, Write, Edit, Glob, Grep, Bash`

**Use for:**

- Code generation
- Running tests
- Build processes
- Deployment tasks

**Example:**

```yaml
---
name: test-runner
description: Runs tests, analyzes failures, and suggests fixes.
tools: Read, Write, Edit, Glob, Grep, Bash
model: inherit
---
```

**Why Bash access?**

- Need to execute commands (npm test, etc.)
- Interact with development tools
- Run build and deployment scripts

**⚠️ Warning**: Bash access is powerful. Only grant when absolutely necessary.

### Tool Selection Matrix

| Agent Purpose       | Read | Write | Edit | Glob | Grep | Bash | Rationale                  |
| ------------------- | ---- | ----- | ---- | ---- | ---- | ---- | -------------------------- |
| Validation/Checking | ✅   | ❌    | ❌   | ✅   | ✅   | ❌   | Read-only analysis         |
| Documentation       | ✅   | ✅    | ✅   | ✅   | ✅   | ❌   | File creation/editing only |
| Code Generation     | ✅   | ✅    | ✅   | ✅   | ✅   | ⚠️   | May need compilation       |
| Testing/Deployment  | ✅   | ✅    | ✅   | ✅   | ✅   | ✅   | Requires shell commands    |

## Model Selection Guidelines

### When to Use `inherit`

**Default choice for most agents.**

```yaml
model: inherit
```

**Benefits:**

- Uses the model selected by the user or parent context
- Centralized control over model selection
- Flexibility to change models without modifying agents
- Cost optimization (users can choose lighter models)

**Use `inherit` when:**

- Agent doesn't require specific model capabilities
- General-purpose validation or checking
- Standard code analysis
- File organization tasks

**Examples:**

- `repo-rule-checker` (validation)
- `api-validator` (checking API compliance)
- `test-analyzer` (analyzing test results)

### When to Use Specific Models

**Only when there's a clear need for specific capabilities.**

```yaml
model: sonnet
```

**Use specific model when:**

- Complex writing requiring nuance (e.g., documentation)
- Advanced reasoning tasks
- Creative content generation
- Multi-step planning and strategy

**Examples:**

- `doc-writer` uses `sonnet` (complex technical writing)
- `architect` uses `sonnet` (system design decisions)

### Model Selection Decision Tree

```
Start: Choosing Agent Model
    │
    ├─ Does this agent require specific model capabilities?
    │   │
    │   ├─ No → Use `model: inherit` ✅
    │   │        (Most agents should use inherit)
    │   │
    │   └─ Yes → What specific capability?
    │              │
    │              ├─ Complex writing/documentation → `model: sonnet`
    │              ├─ Advanced reasoning/planning → `model: sonnet`
    │              ├─ Creative content generation → `model: sonnet`
    │              └─ Unsure → Use `model: inherit` ✅
    │                         (Can always change later)
```

**⚠️ Important**: Document your reasoning if using a specific model. Add a comment in the agent explaining why.

## Agent Responsibility Boundaries

### Single Responsibility Principle

Each agent should have **one clear, focused purpose**.

**✅ Good - Single Responsibility:**

```yaml
name: doc-writer
description: Expert documentation writer specializing in Obsidian-optimized markdown and Diátaxis framework. Use when creating, editing, or organizing project documentation.
```

**❌ Bad - Multiple Responsibilities:**

```yaml
name: doc-and-code-helper
description: Writes documentation, generates code, runs tests, and deploys applications.
```

### Avoiding Overlap

Before creating a new agent, check if existing agents already cover the domain:

1. **Review** `.claude/agents/` directory
2. **Check** each agent's `description` field
3. **Consider** if you can extend an existing agent
4. **Create new** only if there's no overlap

**Decision Matrix: New Agent vs Extend Existing**

| Scenario                     | Create New Agent | Extend Existing Agent |
| ---------------------------- | ---------------- | --------------------- |
| Completely different domain  | ✅ Yes           | ❌ No                 |
| Different tool requirements  | ✅ Yes           | ❌ No                 |
| Different model needs        | ✅ Yes           | ❌ No                 |
| Slight variation in workflow | ❌ No            | ✅ Yes                |
| Similar expertise area       | ❌ No            | ✅ Yes                |
| Experimental/temporary       | ⚠️ Maybe         | ✅ Prefer extending   |

### Agent Specialization vs Generalization

**Prefer specialization over generalization.**

**✅ Good - Specialized Agents:**

- `doc-writer` - Documentation only
- `repo-rule-checker` - Consistency validation only
- `test-runner` - Test execution only

**❌ Bad - Over-Generalized:**

- `helper` - Too vague, unclear purpose
- `assistant` - No specific expertise
- `general-agent` - Defeats the purpose of specialization

## Convention Referencing Standards

### Required Section: Reference Documentation

**Every agent MUST include a "Reference Documentation" section** at the end:

```markdown
## Reference Documentation

**Project Guidance:**

- `CLAUDE.md` - Primary guidance for all agents working on this project

**Agent Conventions:**

- `docs/explanation/development/ex-de__ai-agents.md` - AI agents convention (all agents must follow)

**Documentation Conventions (if applicable):**

- `docs/explanation/conventions/README.md` - Index of all conventions
- `docs/explanation/conventions/ex-co__file-naming-convention.md` - How to name files
- `docs/explanation/conventions/ex-co__linking-convention.md` - How to link between files
- `docs/explanation/conventions/ex-co__diataxis-framework.md` - How to organize documentation

**Related Agents:**

- Other agents this one works with or complements
```

### Reference Categories

Organize references into clear categories:

1. **Project Guidance** - Always reference `CLAUDE.md`
2. **Agent Conventions** - Always reference this document (`ex-de__ai-agents.md`)
3. **Domain-Specific Conventions** - Reference relevant conventions
4. **Related Agents** - Cross-reference complementary agents

### Link Format

Use GitHub-compatible markdown with relative paths:

```markdown
✅ Good:

- `docs/explanation/development/ex-de__ai-agents.md` - AI agents convention

❌ Bad:

- [[ex-de__ai-agents]] - Obsidian wiki link (not GitHub compatible)
- `/docs/explanation/development/ex-de__ai-agents.md` - Absolute path
- `docs/explanation/development/ex-de__ai-agents` - Missing .md extension
```

See [Linking Convention](../conventions/ex-co__linking-convention.md) for details.

## Agent Documentation Standards

### Required Elements

Every agent must include:

1. ✅ **Clear purpose statement** - What does this agent do?
2. ✅ **Core expertise/responsibility** - What is it an expert in?
3. ✅ **Usage guidelines** - When should you use this agent?
4. ✅ **Reference documentation** - Links to conventions and related docs

### Recommended Elements

Depending on complexity, consider adding:

- **Examples** - Show the agent in action
- **Anti-patterns** - What NOT to do
- **Checklists** - Step-by-step verification
- **Decision trees** - Help users make decisions
- **Troubleshooting** - Common issues and solutions

### Writing Style

Follow these guidelines when writing agent documentation:

1. **Use imperative, direct language**
   - ✅ "Use this agent when creating documentation"
   - ❌ "This agent could potentially be used for documentation tasks"

2. **Be action-oriented**
   - ✅ "Validates consistency between files"
   - ❌ "Performs validation activities"

3. **Provide concrete examples**
   - Include code snippets, file examples, command outputs
   - Show both good (✅) and bad (❌) examples

4. **Use checklists where applicable**
   - Break complex tasks into verifiable steps
   - Use `- [ ]` format for actionable items

5. **Be specific, not vague**
   - ✅ "Checks file naming against ex-co\_\_file-naming-convention.md"
   - ❌ "Validates files"

## Information Accuracy and Verification

### Core Principle: Verify, Never Assume

**All agents must prioritize factual accuracy over assumptions.** When dealing with information that can be verified, agents MUST verify it rather than relying on assumptions or general knowledge.

### Verification Requirements

#### 1. Code-Related Information

When discussing code, libraries, APIs, or technical implementations:

**✅ REQUIRED: Read the Actual Code**

```markdown
❌ Bad (Assumption):
"This function probably uses async/await based on common patterns."

✅ Good (Verified):
"This function uses async/await (confirmed by reading src/utils/api.ts:42-58)."
```

**How to verify:**

- Use `Read` tool to examine actual source files
- Use `Grep` to search for specific patterns
- Use `Glob` to find related files
- Quote exact line numbers when referencing code

**Example verification process:**

```markdown
1. User asks: "How does authentication work in this project?"
2. ❌ DON'T: Assume common auth patterns and describe generic implementation
3. ✅ DO:
   - Search for auth-related files: Grep for "auth", "login", "token"
   - Read actual implementation files
   - Trace the authentication flow through the code
   - Report findings with specific file paths and line numbers
```

#### 2. Documentation and Convention Claims

When referencing project conventions, documentation, or standards:

**✅ REQUIRED: Read the Actual Documents**

```markdown
❌ Bad (Assumption):
"Files should probably follow kebab-case naming."

✅ Good (Verified):
"Files must follow the pattern [prefix]**[content-identifier].[extension]
per docs/explanation/conventions/ex-co**file-naming-convention.md:44-48"
```

**How to verify:**

- Read convention documents before referencing them
- Quote exact sections when making claims
- Link to specific files and line numbers
- Never paraphrase without verification

#### 3. External Libraries and Technologies

When discussing external libraries, frameworks, or technologies:

**✅ REQUIRED: Use Web Search and Fetch**

```markdown
❌ Bad (Outdated Knowledge):
"React Router v6 uses <Switch> component for routing."

✅ Good (Verified):
"React Router v6 uses <Routes> component (verified via official docs at
reactrouter.com/docs - accessed 2025-11-23). The <Switch> component
was replaced in v6."
```

**How to verify:**

- Use `WebSearch` to find official documentation
- Use `WebFetch` to read official docs directly
- Cite sources with URLs and access dates
- Prefer official documentation over blog posts
- Cross-reference multiple sources for controversial topics

**When to use web verification:**

- Library versions and compatibility
- API changes and deprecations
- Best practices and recommendations
- Framework-specific conventions
- Security advisories
- Current state of external projects

#### 4. File and Directory Structure

When making claims about project structure:

**✅ REQUIRED: Verify with Actual File System**

```markdown
❌ Bad (Assumption):
"The tests are probably in a **tests** directory."

✅ Good (Verified):
"Tests are located in src/**tests**/ (confirmed via Glob: 'src/\*_/_.test.ts'
found 15 files in src/**tests**/)"
```

**How to verify:**

- Use `Glob` to search for files and directories
- Use `Bash` (if permitted) to list directory contents
- Use `Read` to verify file contents
- Report exact paths found

### Verification Tools Matrix

| Information Type    | Primary Tool | Secondary Tool   | Required?      |
| ------------------- | ------------ | ---------------- | -------------- |
| Code implementation | Read         | Grep, Glob       | ✅ Required    |
| Project conventions | Read         | Grep             | ✅ Required    |
| File structure      | Glob         | Bash             | ✅ Required    |
| External libraries  | WebSearch    | WebFetch         | ✅ Required    |
| Official docs       | WebFetch     | WebSearch        | ✅ Required    |
| Best practices      | WebSearch    | WebFetch         | ⚠️ Recommended |
| Historical context  | WebSearch    | Read (changelog) | ⚠️ Recommended |

### When Verification is NOT Possible

If information cannot be verified through available tools:

1. **State the limitation explicitly**

   ```markdown
   ⚠️ "I cannot verify this without access to [X]. Based on general knowledge,
   [Y], but this should be confirmed by [how to verify]."
   ```

2. **Provide verification steps for the user**

   ```markdown
   "To verify this, please:

   1. Check [specific location]
   2. Run [specific command]
   3. Confirm [expected outcome]"
   ```

3. **Never present unverified information as fact**
   ```markdown
   ❌ "The API uses JWT tokens."
   ✅ "The API likely uses JWT tokens (common pattern for REST APIs),
   but I cannot verify without reading the actual implementation."
   ```

### Verification Best Practices

#### Before Making Claims

1. **Ask yourself**: "Can I verify this?"
2. **If yes**: Use appropriate tools to verify
3. **If no**: State the limitation clearly
4. **Always**: Provide sources and evidence

#### When Reading Code

```markdown
✅ Good verification pattern:

1. Read the file: Read("src/auth/login.ts")
2. Quote specific lines: "Lines 42-58 show the login implementation"
3. Explain what you found: "Uses bcrypt for password hashing"
4. Provide context: "This aligns with security best practices"
```

#### When Using Web Search

```markdown
✅ Good verification pattern:

1. Search for official docs: WebSearch("React 18 official documentation")
2. Fetch the actual page: WebFetch(official_url, "What are the new features?")
3. Quote the source: "According to reactjs.org/blog/2022/03/29/..."
4. Include access date: "(accessed 2025-11-23)"
```

#### When Uncertain

```markdown
✅ Good uncertainty handling:
"I searched for [X] using [tool] but found [Y]. This suggests [Z],
however I recommend verifying by [verification method]."

❌ Bad uncertainty handling:
"I'm not sure, but it's probably [guess]."
```

### Agent-Specific Verification Requirements

Different agents have different verification needs:

#### Documentation Agents (doc-writer)

- ✅ Must verify all code examples by reading actual code
- ✅ Must verify all file paths exist using Glob
- ✅ Must verify all claims about project structure
- ✅ Must cross-reference convention documents
- ✅ Must use WebSearch for external library documentation

#### Validation Agents (repo-rule-checker)

- ✅ Must read all files before validating
- ✅ Must never assume compliance without checking
- ✅ Must provide specific line numbers for issues
- ✅ Must verify links point to existing files
- ✅ Must check actual frontmatter, not assumed format

#### Development Agents (test-runner, etc.)

- ✅ Must read actual test files to understand setup
- ✅ Must verify command output by actually running commands
- ✅ Must check actual error messages, not assumed messages
- ✅ Must verify tool availability before suggesting commands

### Verification Anti-Patterns

#### ❌ Making Assumptions

**Bad:**

```markdown
"Most Node.js projects use npm, so this project probably uses npm."
```

**Good:**

```markdown
"Checking package.json... (Read tool) Confirmed: project uses npm 11.6.2
as specified in package.json:5 under volta.npm field."
```

#### ❌ Outdated General Knowledge

**Bad:**

```markdown
"Vue 3 uses the Options API by default."
```

**Good:**

```markdown
"Checking Vue 3 documentation... (WebFetch) Vue 3 documentation recommends
Composition API for new projects (vuejs.org/guide/introduction.html,
accessed 2025-11-23)."
```

#### ❌ Vague References

**Bad:**

```markdown
"According to the documentation, files should be named a certain way."
```

**Good:**

```markdown
"According to docs/explanation/conventions/ex-co**file-naming-convention.md:44-48,
files must follow the pattern: [prefix]**[content-identifier].[extension]"
```

#### ❌ Unverified File Paths

**Bad:**

```markdown
"The configuration is in config/app.js"
```

**Good:**

```markdown
"Searching for config files... (Glob: 'config/\*_/_.js')
Found: config/app.js, config/database.js, config/auth.js
The app configuration is in config/app.js (verified)"
```

### Verification Checklist for Agents

Before providing information, verify:

- [ ] Have I read the actual files being discussed?
- [ ] Have I verified file paths exist?
- [ ] Have I checked the actual code implementation?
- [ ] Have I consulted official documentation for external libraries?
- [ ] Have I provided specific line numbers and file paths?
- [ ] Have I stated clearly what I verified vs. what I assumed?
- [ ] Have I used appropriate tools (Read, Grep, Glob, WebSearch, WebFetch)?
- [ ] Have I cited sources with URLs and access dates?
- [ ] If I cannot verify, have I stated this limitation clearly?
- [ ] Have I provided steps for the user to verify themselves?

### When to Ask for Clarification

If verification reveals uncertainty or contradictions:

```markdown
"I found two different implementations:

1. src/auth/jwt.ts uses JWT tokens
2. src/auth/session.ts uses session cookies

Both are active. Could you clarify which authentication method
is currently in use, or if both are supported?"
```

This is better than:

- Assuming one is correct
- Presenting both without clarification
- Guessing based on "best practices"

## Creating New Agents

### When to Create a New Agent

Create a new agent when:

1. ✅ **New domain or expertise** not covered by existing agents
2. ✅ **Different tool requirements** than existing agents
3. ✅ **Distinct user need** that would benefit from specialization
4. ✅ **Clear, single responsibility** that doesn't overlap

Don't create a new agent when:

1. ❌ **Existing agent can be extended** with minor modifications
2. ❌ **Responsibilities overlap** significantly with existing agents
3. ❌ **Purpose is too vague** or general
4. ❌ **Temporary or experimental** need (extend existing instead)

### Agent Creation Checklist

Before submitting a new agent, verify:

#### Frontmatter Complete

- [ ] `name` matches filename (kebab-case, no `.md`)
- [ ] `description` clearly states when to use this agent
- [ ] `tools` explicitly lists required tools only (least privilege)
- [ ] `model` set to `inherit` (or justified if specific)

#### Document Structure

- [ ] H1 title follows pattern: `# [Name] Agent`
- [ ] Core responsibility/expertise clearly stated
- [ ] Detailed guidelines provided
- [ ] Reference documentation section included

#### Content Quality

- [ ] Purpose is clear and specific
- [ ] No significant overlap with existing agents
- [ ] Examples provided for usage
- [ ] Anti-patterns documented (what NOT to do)

#### Convention Compliance

- [ ] References `CLAUDE.md`
- [ ] References AI agents convention (`ex-de__ai-agents.md`)
- [ ] References relevant domain conventions
- [ ] Links use correct GitHub-compatible format

#### Information Accuracy

- [ ] Agent includes verification requirements for its domain
- [ ] Agent specifies when to use Read/Grep/Glob for verification
- [ ] Agent specifies when to use WebSearch/WebFetch for verification
- [ ] Agent emphasizes verification over assumptions
- [ ] Agent provides examples of good vs bad verification practices

#### Testing

- [ ] Manually tested agent invocation
- [ ] Verified tool permissions are sufficient
- [ ] Confirmed no tool permission creep
- [ ] Verified model selection is appropriate

### Agent Template

Use this template when creating new agents:

```markdown
---
name: agent-name
description: Expert in [domain] specializing in [specific area]. Use when [specific scenario].
tools: Read, Glob, Grep
model: inherit
---

# Agent Name Agent

You are an expert [role/domain] specializing in [specific expertise].

## Core Responsibility

Your primary job is to [clear, specific purpose statement].

## [Domain-Specific Guidelines]

[Detailed guidelines, standards, examples specific to this agent's domain]

### [Subsection as needed]

[More specific guidance]

## [Additional Sections as Needed]

- Examples
- Checklists
- Decision trees
- Anti-patterns
- Troubleshooting

## Reference Documentation

**Project Guidance:**

- `CLAUDE.md` - Primary guidance for all agents working on this project

**Agent Conventions:**

- `docs/explanation/development/ex-de__ai-agents.md` - AI agents convention (all agents must follow)

**[Domain-Specific Conventions]:**

- Relevant conventions for this agent's domain

**Related Agents:**

- Other complementary agents (if applicable)
```

## Relationship to CLAUDE.md

### Division of Responsibilities

**CLAUDE.md provides:**

- ✅ Project-wide guidance for ALL agents
- ✅ Project overview and context
- ✅ Environment setup (Volta, Node.js, npm)
- ✅ Git hooks and commit conventions
- ✅ High-level documentation organization
- ✅ Reference to this AI agents convention

**Individual agents provide:**

- ✅ Specialized domain expertise
- ✅ Specific task instructions
- ✅ Detailed guidelines for their area
- ✅ Examples and checklists for their domain

**This convention (ex-de\_\_ai-agents.md) provides:**

- ✅ Standards for how agents are structured
- ✅ Agent creation guidelines
- ✅ Tool and model selection criteria
- ✅ Convention referencing requirements

### Inheritance Pattern

```
CLAUDE.md (Project-wide guidance)
    ↓ (inherited by all agents)
Individual Agents (Specialized capabilities)
    ↓ (follow standards from)
ex-de__ai-agents.md (Agent structure standards)
```

**Rules:**

1. **Don't duplicate** - Agents should reference CLAUDE.md, not repeat its content
2. **Do specialize** - Agents add domain expertise on top of project guidance
3. **Follow conventions** - All agents must comply with this convention

### What Belongs Where

| Content Type      | CLAUDE.md | Individual Agent | This Convention |
| ----------------- | --------- | ---------------- | --------------- |
| Project overview  | ✅        | ❌               | ❌              |
| Environment setup | ✅        | ❌               | ❌              |
| Git/commit rules  | ✅        | ❌               | ❌              |
| Documentation org | ✅        | ❌               | ❌              |
| Agent structure   | ❌        | ❌               | ✅              |
| Agent creation    | ❌        | ❌               | ✅              |
| Domain expertise  | ❌        | ✅               | ❌              |
| Specific tasks    | ❌        | ✅               | ❌              |

## Special Cases

### Agent Directory Structure

The `.claude/agents/` directory:

- **Does NOT need** a `README.md` file (agents are self-documenting)
- **Contains only** agent definition files (`.md` files)
- **Follows** flat structure (no subdirectories)

### Agent Versioning

Currently, we don't version agents. If significant changes are needed:

1. **Update in place** for minor improvements
2. **Document changes** in the agent file (update metadata comment)
3. **Consider** creating a new agent if the purpose changes significantly

### Deprecating Agents

If an agent is no longer needed:

1. **Don't delete immediately** - may be referenced
2. **Add deprecation notice** at the top of the agent file
3. **Point to replacement** agent (if applicable)
4. **Remove after** confirming no references exist

## Anti-Patterns

### ❌ Vague Descriptions

**Bad:**

```yaml
description: Helper agent for various tasks
```

**Good:**

```yaml
description: Expert documentation writer specializing in Obsidian-optimized markdown and Diátaxis framework. Use when creating, editing, or organizing project documentation.
```

### ❌ Tool Permission Creep

**Bad:**

```yaml
name: doc-validator
tools: Read, Write, Edit, Glob, Grep, Bash # Too many tools for validation!
```

**Good:**

```yaml
name: doc-validator
tools: Read, Glob, Grep # Read-only for validation
```

### ❌ Model Specification Without Justification

**Bad:**

```yaml
model: sonnet # No explanation why
```

**Good:**

```yaml
model: sonnet # Complex technical writing requires advanced language capabilities
```

Or better:

```yaml
model: inherit # Use default unless there's a specific need
```

### ❌ Duplicating CLAUDE.md

**Bad:**

```markdown
## Project Setup

This project uses Volta for Node.js version management...
[Repeats entire CLAUDE.md section]
```

**Good:**

```markdown
## Reference Documentation

**Project Guidance:**

- `CLAUDE.md` - Primary guidance including environment setup
```

### ❌ Missing Reference Section

**Bad:**

```markdown
# My Agent

Does stuff.

[No references to conventions or CLAUDE.md]
```

**Good:**

```markdown
# My Agent

Does stuff.

## Reference Documentation

**Project Guidance:**

- `CLAUDE.md` - Primary guidance for all agents

**Agent Conventions:**

- `docs/explanation/development/ex-de__ai-agents.md` - AI agents convention
```

### ❌ Overlapping Responsibilities

**Bad:**

```yaml
name: doc-writer-and-validator
description: Writes documentation and validates it
```

**Good:**
Create two separate agents:

```yaml
name: doc-writer
description: Expert documentation writer...
```

```yaml
name: doc-validator
description: Validates documentation consistency...
```

## Validation and Compliance

### Repo-Rule-Checker Integration

The `repo-rule-checker` agent validates all agents against this convention.

**Checks performed:**

1. ✅ Frontmatter has all required fields
2. ✅ Agent `name` matches filename
3. ✅ Agent `description` provides clear usage guidance
4. ✅ Agent `tools` field lists tools explicitly
5. ✅ Agent `model` field is present and valid
6. ✅ Document structure follows standard pattern
7. ✅ Reference documentation section exists
8. ✅ References to CLAUDE.md and this convention present
9. ✅ Links use GitHub-compatible format

### Manual Verification

Before committing a new agent:

1. **Read this entire convention** - Understand all requirements
2. **Use the agent creation checklist** - Verify all items
3. **Test the agent** - Invoke it and verify behavior
4. **Review existing agents** - Ensure consistency
5. **Run repo-rule-checker** - Validate compliance

## Related Documentation

- [Development Index](./README.md) - Overview of development conventions
- [Conventions Index](../conventions/README.md) - Documentation conventions
- [File Naming Convention](../conventions/ex-co__file-naming-convention.md) - How to name files
- [Linking Convention](../conventions/ex-co__linking-convention.md) - How to link between files
- [Diátaxis Framework](../conventions/ex-co__diataxis-framework.md) - Documentation organization

---

**Last Updated**: November 23, 2025
