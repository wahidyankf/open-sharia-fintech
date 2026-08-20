# Checker Implementation Patterns

## Checker Implementation Patterns

## Link Validation Workflow

Standard 5-step checker workflow:

Step 0: Initialize Report
Step 1: Discover Files (glob for \*.md)
Step 2: Extract Links (parse markdown, categorize)
Step 3: Validate Internal Links (file exists, format correct)
Step 4: Validate External Links (HTTP request, cache results)
Step 5: Finalize Report (summary, grouped by criticality)

## Progressive Writing Requirement

**CRITICAL**: Write findings to report file immediately after discovery (don't buffer in memory)

**Why**: Context compaction can lose buffered findings during long validation runs

## Tool Requirements for Link Checkers

**Required tools**:

- Read: Read markdown files to extract links
- Glob: Find all markdown files in scope
- Grep: Extract link patterns
- Bash: File existence checks, path resolution, HTTP requests
- Write: Initialize and update report file

## Categorization by Criticality

**CRITICAL** (Must fix before publication):

- Broken internal links (404, file not found)
- Wiki-link syntax (GitHub does not render `[[...]]` links)

**HIGH** (Should fix before publication):

- Missing .md extension in docs/ links
- Broken external links (404, 410)
- Filename as link text (poor accessibility)

**MEDIUM** (Fix when convenient):

- External link redirects (works but suboptimal)
- External link timeouts (may be temporary)
- Suboptimal link text (not descriptive enough)

**LOW** (Optional improvements):

- Consider updating redirect to final URL
- Suggest alternative link text

## Dual-Label Pattern for Link Checkers

Link checkers use both verification status AND criticality:

Finding: [BROKEN] - Internal Link to Non-Existent File

**Verification**: [BROKEN] - Target file does not exist
**Criticality**: CRITICAL - Breaks user navigation

**Verification labels**:

- [OK] - Link is valid
- [BROKEN] - Link target doesn't exist (404)
- [REDIRECT] - External link redirects (informational)
- [FORMAT_ERROR] - Wrong format (missing .md, etc.)

**Why dual labels?**

- Verification describes FACTUAL STATE
- Criticality describes URGENCY/IMPORTANCE
- Complementary information for fixer decision-making
