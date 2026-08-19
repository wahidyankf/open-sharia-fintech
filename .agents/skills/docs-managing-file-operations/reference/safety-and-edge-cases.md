# Safety Guidelines and Edge Cases

## Read Before Edit

**ALWAYS** read files before making changes:

- Read all affected files first
- Verify current state before editing
- Check for existing references before deleting

## Ask Before Large Changes

For operations affecting many files:

1. **Present complete plan** to user
2. **List all affected files** (count them)
3. **Explain impact** (renames, links, indices, deletions)
4. **Get explicit confirmation** before proceeding

## Extra Caution for Deletions

When deleting files:

1. **Always find references first** using Grep
2. **Present deletion plan** to user
3. **Warn about impact** on other files
4. **Get explicit confirmation**
5. **Verify cleanup** after deletion

## Preserve Existing Content

When editing files:

- Only update the links/references (surgical edits)
- Don't change unrelated content
- Preserve formatting and structure
- Don't refactor while managing files

## Verify Before Completing

Before telling user "done":

1. **Use Glob** to verify files exist at new paths (or deleted)
2. **Use Grep** to check for any remaining old references
3. **Spot-check** a few updated links with Read
4. **List any warnings** or edge cases

## Edge Cases and Special Considerations

### README.md Files

README.md files follow a fixed name regardless of directory:

- **Never rename** `README.md` — directory-index files must stay named `README.md`
- **Keep as** `README.md` for GitHub compatibility
- **Update content** but not filename

### Moving Files Out of docs/

If user wants to move files outside `docs/`:

1. **Alert user** that different conventions may apply
2. **Ask for guidance** on naming in new location
3. **Proceed carefully** with user approval

### Circular Link Updates

When operations affect many interconnected files:

1. **Update systematically** (don't miss any)
2. **Use Grep** to find all references
3. **Verify each update** points to correct path
4. **Re-check** after updates to catch any missed

### Managing Recently Created Files

If files were just created and not committed:

1. **Check git status** first
2. **Note to user** that git history won't show operation
3. **Offer to commit** before operation (preserves history)
