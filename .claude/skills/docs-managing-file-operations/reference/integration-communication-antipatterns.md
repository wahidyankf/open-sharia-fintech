# Integration with Other Agents, Communication, and Anti-Patterns

## Integration with Other Agents

### After File Operations: Run docs-link-checker

**Always recommend** running `docs-link-checker` after file management:

```
All files managed and links updated!

Next steps:
1. Review changes: git diff
2. Validate links: Use docs-link-checker to verify all links
3. Commit changes: git commit -m "refactor(docs): reorganize documentation structure"
```

### Before Large Reorganizations: Consider rules-checker

For large reorganizations, consider running `rules-checker` before and after:

- Before: Check current state compliance
- After: Verify no new inconsistencies introduced

### Use docs-maker for New Files

If operations require creating new README.md files:

1. Complete the file management operation
2. Suggest user invoke `docs-maker` to create proper index files
3. Or create minimal index and suggest enhancement via `docs-maker`

## Communication Best Practices

### Clear Summaries

After completing file management operation:

```markdown
## File Management Complete

### Operations Performed

- Renamed 8 files in repo-governance/conventions/ (kebab-case compliance)
- Deleted 2 deprecated files
- Moved 1 file to new location

### Links Updated

- Updated 23 links across 12 files
- Removed 3 links to deleted files

### Indices Updated

- Updated docs/explanation/README.md
- Updated repo-governance/conventions/README.md
- Removed entries for deleted files

### Git Operations

- All operations performed with git mv/git rm (history preserved)

### Next Steps

1. Review: git diff --stat
2. Validate: Use docs-link-checker agent
3. Commit: git commit -m "refactor(docs): reorganize documentation structure"
```

### Warning About Uncommitted Changes

If `git status` shows other uncommitted changes:

```
[Warning] You have other uncommitted changes in your working directory.

I recommend committing or stashing those changes before proceeding with this operation to avoid
confusion in git history.

Proceed anyway? (Please confirm)
```

## Anti-Patterns

| Anti-Pattern                   | Bad                                 | Good                                              |
| ------------------------------ | ----------------------------------- | ------------------------------------------------- |
| **Using mv/rm instead of git** | `mv old.md new.md`, `rm file.md`    | `git mv old.md new.md`, `git rm file.md`          |
| **Non-kebab-case filenames**   | `MyFile.md`, `my_file.md`           | `my-file.md` (lowercase kebab-case)               |
| **Broken links**               | Delete files without updating links | Find and update/remove ALL links to deleted files |
| **Skipping indices**           | Delete files but not README.md      | Update all affected README.md files               |
| **No user confirmation**       | Delete 50 files without asking      | Present plan and get confirmation                 |
| **Missing validation**         | Assume links are correct            | Verify with Glob/Grep, suggest docs-link-checker  |
| **Unsafe deletion**            | Delete without checking references  | Find all references first, plan cleanup           |
| **Orphaned links**             | Delete files, leave broken links    | Remove or update all references to deleted files  |
