# Systematic File Management Process

Follow this process for ALL file management operations:

## Phase 1: Discovery & Analysis

1. **Understand the request**
   - What operation is being requested? (rename, move, or delete?)
   - What is the target? (file or directory?)
   - What is the old path? What is the new path (if applicable)?
   - Does the directory exist? Do conflicts exist?

2. **Read current state**
   - Use Glob to find all affected files
   - Use Read to verify current kebab-case compliance
   - Use Grep to find all links referencing the files
   - List all files that will be affected

3. **Calculate impact**
   - How many files need renaming/moving/deleting?
   - How many files have links that need updating?
   - Which README.md files need updating?

## Phase 2: Planning

1. **Validate new filenames** (for rename/move operations)
   - Confirm new basenames are lowercase kebab-case
   - Confirm filenames do not contain underscores, uppercase, or spaces
   - List old path → new path mapping

2. **Verify deletion safety** (for delete operations)
   - Find all links pointing to files being deleted
   - Verify these links will be removed or updated
   - Check if files are referenced in indices
   - Confirm no orphaned links will remain

3. **Plan git operations**
   - List all `git mv` commands needed (rename/move)
   - List all `git rm` commands needed (delete)
   - Ensure operations are in correct order
   - Check for naming conflicts

4. **Plan link updates**
   - Identify all files with links to affected files
   - Calculate new relative paths for each link (rename/move)
   - Identify links to remove (delete)
   - Plan Edit operations needed

5. **Plan index updates**
   - Identify which README.md files need updates
   - Plan what changes are needed in each

6. **Get user confirmation**
   - Present complete plan to user
   - List all files that will be affected
   - Warn about any potential issues
   - Ask user to confirm before proceeding

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
