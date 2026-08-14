# Factual Validation — Update Frequency Rules and Metadata Storage

## When to Re-validate Content

**MANDATORY re-validation triggers**:

- **6 months since last validation** - Standard refresh cycle
- **Major version release** of referenced software/library
- **Breaking change announced** in official release notes
- **User reports error** in documentation
- **Deprecation notice** for used API/method

**OPTIONAL re-validation triggers**:

- Minor version updates (if content specific to that version)
- Patch releases (usually safe to skip)
- Community feedback about potential issues
- Regular documentation review cycles

## Validation Metadata Storage

**Location**: `docs/metadata/external-links-status.yaml`

**Format**:

```yaml
factual-validations:
  - file: "docs/tutorials/quick-start.md"
    claim: "npm install --save-dev prettier"
    verification-status: "[Verified]"
    last-checked: "2025-12-27T10:00:00+07:00"
    source: "https://docs.npmjs.com/cli/v9/commands/npm-install"
    expires: "2026-06-27T10:00:00+07:00" # 6 months later
```
