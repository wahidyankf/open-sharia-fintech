# Link Update Guidelines and Git Operations Best Practices

## Calculating New Relative Paths

When updating links, calculate the new relative path based on:

1. **Source file location** (where the link is)
2. **Target file new location** (where it's linking to)
3. **Relative path calculation** (how many `../` needed)

## Removing Links to Deleted Files

When deleting files, you may need to:

1. **Remove the entire link** - If the link has no replacement
2. **Replace with alternative** - If there's a newer version
3. **Add deletion note** - If context is important

## Verification Tip

To verify relative path:

1. Start at source file
2. Count each `../` as going up one level
3. Count each `/dirname/` as going down one level
4. Verify you end at target file

## Link Syntax Requirements

All links must follow
[Linking Convention](../../../../repo-governance/conventions/formatting/linking.md):

- Use relative paths (`./` or `../`)
- Include `.md` extension
- Use GitHub-compatible markdown `[Text](path.md)` format
- No wiki-link syntax `[[...]]`

## Always Use git Commands

**NEVER** use regular `mv` or `rm` commands. Always use `git mv` and `git rm`:

```bash
# Good:
git mv old-path.md new-path.md
git rm file-to-delete.md
git rm -r directory-to-delete/

# Bad:
mv old-path.md new-path.md
rm file-to-delete.md
rm -r directory-to-delete/
```

**Why?** `git mv` and `git rm` preserve file history, while regular commands break git tracking.

## Verify Operations Succeed

After each git operation:

```bash
# Check git status to verify operation
git status
```

## Handle Conflicts Carefully

If `git mv` fails (file already exists):

1. Alert user to the conflict
2. Suggest resolution (rename target, or merge files)
3. Do NOT force overwrite

## Batch Operations in Correct Order

When managing multiple files:

1. **Rename directory first** (if applicable)
2. **Rename files inside** (in any order)
3. **Delete files** (after updating references)
4. **Update links** (after all files renamed/moved/deleted)
5. **Update indices** (last)
