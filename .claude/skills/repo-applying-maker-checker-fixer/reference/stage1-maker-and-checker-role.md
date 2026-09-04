# Maker-Checker-Fixer — Stage 1: Maker and Stage 2 Checker Role

## Stage 1: Maker (Content Creation & Updates)

**Role**: Creates NEW content and updates EXISTING content with all dependencies

**Characteristics**:

- User-driven operation (responds to "create" or "update" requests)
- Comprehensive scope (creates target content AND updates related files)
- Cascading changes (adjusts indices, cross-references, dependencies)
- Proactive management (anticipates what needs updating)

**Tool Pattern**: `Write`, `Edit` (content modification)

**Color**: Blue (writer agents) or Yellow (special case: repo-rules-maker uses bash)

**When to Use Maker**:

- User explicitly requests content creation or updates
- Creating NEW content from scratch
- Making significant changes to EXISTING content
- Need comprehensive dependency management
- User-driven workflow (user says "create" or "update")

**Example Workflow**:

```markdown
User: "Create new TypeScript generics tutorial"

Maker:

1. Creates main content file
2. Creates bilingual version (if applicable)
3. Updates navigation files
4. Ensures overview/index links correct
5. Follows weight ordering convention
6. Uses accessible colors in diagrams
7. Validates all internal links
8. Delivers complete, ready-to-publish content
```

## Stage 2: Checker (Validation) — Role and Characteristics

**Role**: Validates content against conventions and generates audit reports

**Characteristics**:

- Validation-driven (analyzes existing content)
- Non-destructive (does NOT modify files being checked)
- Comprehensive reporting (generates detailed audit in `local-tmp/<agent-family>/`)
- Evidence-based (re-validation in fixer prevents false positives)

**Tool Pattern**: `Read`, `Glob`, `Grep`, `Write`, `Bash` (read-only + report generation)

- `Write` needed for audit report files
- `Bash` needed for UTC+7 timestamps

**Color**: Green (checker agents)

**When to Use Checker**:

- ✅ REQUIRED: New content created from scratch
- ✅ REQUIRED: Major refactoring or updates
- ✅ REQUIRED: Before publishing to production
- ✅ REQUIRED: Complex content (tutorials, web platforms)
- ✅ REQUIRED: Critical files (AGENTS.md, conventions)
- ⚠️ OPTIONAL: Small updates to high-quality content

**Criticality Categorization**:

Checkers categorize findings by importance/urgency:

- 🔴 **CRITICAL** - Breaks functionality, blocks users (must fix before publication)
- 🟠 **HIGH** - Significant quality degradation, convention violations (should fix)
- 🟡 **MEDIUM** - Minor quality issues, style inconsistencies (fix when convenient)
- 🟢 **LOW** - Suggestions, optional improvements (consider for future)

**Report Format**: Findings grouped by criticality with emoji indicators
