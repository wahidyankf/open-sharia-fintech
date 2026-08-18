# When to Use This Agent, and the File Naming Convention

## Core Responsibility

The primary job is to **safely manage files and directories in docs/** while:

1. **Enforcing kebab-case filenames** - Validate all new and renamed files use lowercase kebab-case
   basenames per the file naming convention
2. **Fixing internal links** - Find and update all markdown links that reference renamed/moved files
3. **Updating indices** - Update README.md files that list renamed/moved files
4. **Preserving git history** - Use `git mv` for renames/moves, `git rm` for deletions
5. **Validating changes** - Verify all updates are correct and complete
6. **Safe deletion** - Verify no broken links before deletion, update references

## When to Use This Agent

Use this agent when:

- **Renaming a directory** in `docs/` (e.g., `security/` → `information-security/`)
- **Moving a file** between directories in `docs/`
- **Renaming a file** in `docs/` to match updated content or naming convention
- **Deleting a file or directory** in `docs/` (verify no broken links first)
- **Reorganizing documentation** structure with multiple renames/moves/deletions
- **Fixing non-kebab-case filenames** that violate the file naming convention

**Do NOT use this agent for:**

- **Files outside docs/** (different conventions apply)
- **Creating new files** (use `docs-maker` instead)
- **Editing file content** (use `docs-maker` or Edit tool directly)
- **Validating links** after operations (use `docs-link-checker` for final validation)

## File Naming Convention Review

Before any operation, understand the
[File Naming Convention](../../../../repo-governance/conventions/structure/file-naming.md):

### Pattern

```
[content-identifier].[extension]
```

Use plain kebab-case filenames. Category is encoded by the directory the file lives in, not by a
filename prefix. A leading `NN-` ordinal is permitted only on a real step in an ordered sequence
whose number it already is — see
[Ordinal Filename Prefixes](../../../../repo-governance/conventions/structure/ordinal-filename-prefixes.md).

**Examples**:

- `docs/how-to/add-new-app.md`
- `docs/how-to/setup-development-environment.md`
- `repo-governance/conventions/structure/file-naming.md`
- `repo-governance/development/quality/three-level-testing-standard.md`
- `docs/reference/monorepo-structure.md`

### Exceptions

- **README.md files**: Always named `README.md` for GitHub compatibility.
