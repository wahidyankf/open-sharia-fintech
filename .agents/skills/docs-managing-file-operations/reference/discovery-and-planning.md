# Systematic File Management Process: Discovery and Planning

Follow this process for ALL file management operations (Phases 1-2 of 4).

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
