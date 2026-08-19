# Index File Updates and Validation Checklist

## When to Update README.md

Update index files when:

- Directory name changes (link to directory changes)
- File name changes (link to file changes)
- File moved between directories (remove from old index, add to new index)
- File deleted (remove from index)
- New subdirectory created (add to parent index)

## How to Update

1. **Read the index file** completely
2. **Identify the entry** to update/remove
3. **Use Edit tool** to make surgical update
4. **Preserve formatting** and ordering
5. **Verify link syntax** is correct

## Validation Checklist

Before marking an operation complete, verify:

### File Operations

- [ ] All files renamed/moved with `git mv` (not regular `mv`)
- [ ] All files deleted with `git rm` (not regular `rm`)
- [ ] All new file names follow kebab-case naming convention
- [ ] No naming conflicts or overwrites
- [ ] Files exist at new paths (or deleted as intended)

### Link Updates

- [ ] All internal links updated to new paths
- [ ] All links to deleted files removed or updated
- [ ] All relative paths correctly calculated
- [ ] All links include `.md` extension
- [ ] Link text preserved (only path changed)
- [ ] No broken links remain

### Index Updates

- [ ] All affected README.md files updated
- [ ] Directory renames reflected in parent indices
- [ ] File moves reflected in both source and dest indices
- [ ] Deleted files removed from indices
- [ ] Links in indices point to correct paths
- [ ] Formatting and ordering preserved

### Convention Compliance

- [ ] File naming convention followed (lowercase kebab-case)
- [ ] Linking convention followed
- [ ] README.md files at directory roots (exempt from kebab-case rule)

### Deletion Safety (if applicable)

- [ ] All references to deleted files found
- [ ] All references removed or updated
- [ ] No broken links to deleted files remain
- [ ] Index entries for deleted files removed

### Validation Recommendations

- [ ] Suggested running `docs-link-checker` to verify all links
- [ ] Suggested reviewing `git diff` before committing
- [ ] Noted any edge cases or manual checks needed
