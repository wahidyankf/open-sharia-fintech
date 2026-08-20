# Deletion Operations

## Safe Deletion Process

Deleting files requires extra care to avoid broken links:

1. **Find all references**:

   ```bash
   # Use Grep to find all links to the file
   grep -r "path/to/file.md" docs/
   ```

2. **Categorize references**:
   - **Index files**: Remove entries from README.md
   - **Content links**: Either remove or update to point elsewhere
   - **Backlinks**: Identify what needs updating

3. **Verify deletion safety**:
   - List all files that link to the target
   - Confirm user wants to proceed
   - Plan how each reference will be handled

4. **Execute deletion**:

   ```bash
   # Use git rm (NOT regular rm)
   git rm docs/path/to/file.md
   ```

5. **Clean up references**:
   - Update all files that linked to deleted file
   - Remove from index files
   - Verify no broken links remain

## Deleting Directories

When deleting an entire directory:

1. **Find all files inside**:

   ```bash
   # Use Glob to find all files
   docs/path/to/directory/**/*.md
   ```

2. **Find all references to any file in directory**:

   ```bash
   # Use Grep to find links
   grep -r "path/to/directory" docs/
   ```

3. **Verify deletion safety**:
   - List all affected files
   - List all incoming links
   - Confirm user wants to proceed

4. **Execute deletion**:

   ```bash
   # Use git rm -r (NOT regular rm -r)
   git rm -r docs/path/to/directory
   ```

5. **Clean up**:
   - Update parent README.md
   - Remove all references to deleted directory
   - Verify no broken links

## Deletion Safety Checklist

Before deleting any file or directory:

- [ ] Found all references using Grep
- [ ] Identified what needs updating
- [ ] Got user confirmation
- [ ] Planned cleanup for all references
- [ ] Using `git rm` (not regular `rm`)
