# Systematic File Management Process: Execution and Validation

Follow this process for ALL file management operations (Phases 3-4 of 4).

## Phase 3: Execution (ONLY AFTER USER APPROVAL)

1. **Execute git operations**
   - Use `git mv old-path new-path` for renames/moves
   - Use `git rm file-path` for deletions
   - NEVER use regular `mv` or `rm` commands
   - Verify each operation succeeded

2. **Update internal links**
   - Use Edit to update markdown links in all referencing files
   - Update relative paths to point to new locations (rename/move)
   - Remove links to deleted files (delete)
   - Ensure all links include `.md` extension
   - Verify link syntax is correct

3. **Update index files**
   - Update README.md files with new file names/paths
   - Remove entries for deleted files
   - Maintain alphabetical or logical ordering
   - Update descriptions if needed

## Phase 4: Validation

1. **Verify changes**
   - Use Glob to verify renamed/moved files exist at new paths
   - Use Glob to verify deleted files no longer exist
   - Use Grep to check for any remaining old references
   - Use Grep to verify no broken links to deleted files
   - Use Read to spot-check updated links
   - Verify no broken references remain

2. **Recommend final validation**
   - Suggest running `docs-link-checker` to verify all links
   - Suggest reviewing git diff before committing
   - Note any edge cases or manual checks needed
