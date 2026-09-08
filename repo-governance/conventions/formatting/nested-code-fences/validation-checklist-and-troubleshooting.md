---
description: The pre-commit checklist for nested fences, plus symptom-diagnosis-solution troubleshooting for three common rendering failures.
when_to_use: Use when a nested code fence example renders incorrectly and you need to diagnose and fix the symptom.
---

# Validation Checklist and Troubleshooting

## Validation Checklist

Before committing markdown with nested fences:

- [ ] **Outer fence uses 4 backticks** - When documenting markdown structure
- [ ] **Inner fences use 3 backticks** - For code blocks within the example
- [ ] **Every opening fence has matching closing fence** - Count pairs
- [ ] **No orphaned fences** - No extra ``` after proper closure
- [ ] **Fence pairs use same depth** - Opening and closing match (3-3, 4-4)
- [ ] **Content renders correctly** - Test in preview or GitHub
- [ ] **Bold/italic formatting works** - Verify markdown not shown as literals

## Troubleshooting Rendering Issues

### Symptom: Bold/Italic Shows as Literals

**Issue**: Content like `**bold**` displays as literal `**bold**` instead of **bold**.

**Diagnosis**: Orphaned closing fence is treating remaining content as code.

**Solution**:

1. Search for all ``` in the file
2. Count opening and closing fences
3. Remove any orphaned closing fences
4. Verify every opening fence has exactly one matching closing fence

### Symptom: Unexpected Code Block Rendering

**Issue**: Content that should be formatted markdown displays as monospace code.

**Diagnosis**: Fence depth mismatch or unclosed fence pair.

**Solution**:

1. Verify outer fence uses 4 backticks
2. Verify inner fences use 3 backticks
3. Check every opening fence has a closing fence at same depth
4. Test rendering in preview

### Symptom: Fence Markers Visible in Output

**Issue**: Backtick markers (``` or ````) show in rendered output.

**Diagnosis**: Fence pairs are broken or nested incorrectly.

**Solution**:

1. Use 4 backticks for outer fence (not 3)
2. Ensure inner fences use 3 backticks
3. Remove any stray backtick groups
4. Verify proper nesting structure
