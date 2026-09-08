---
description: How to verify LaTeX renders correctly on GitHub, and the common rendering issues (delimiter, missing signs, spacing) with fixes.
when_to_use: Use when a LaTeX formula is not rendering correctly and you need to diagnose why.
---

# Testing LaTeX Rendering

## On GitHub

1. **View any markdown file** on GitHub web interface
2. **LaTeX renders automatically** - no special configuration needed
3. **Works on mobile** - GitHub mobile app also supports LaTeX rendering

**Verification**: View this convention document on GitHub. All formulas should render properly in the web interface.

## Common Rendering Issues

**Problem**: LaTeX displays as raw text instead of rendering

**Cause**: Single `$` delimiter used for display math

**Example of broken code:**

```markdown
$
WACC = \frac{E}{V} \times r_e
$
```

**Solution**: Use double `$$` for display math:

```markdown
$$
WACC = \frac{E}{V} \times r_e
$$
```

**Applies to:**

- Any equation on its own line
- All `\begin{align}` blocks
- Display-level formulas

---

**Problem**: Formula doesn't render (shows raw LaTeX code)

**Causes**:

- Missing dollar signs (`$` or `$$`)
- Unescaped backslashes in markdown preview
- Unsupported LaTeX commands (rare, most standard commands work)

**Solution**: Check syntax, ensure proper dollar sign placement, verify no typos in command names.

**Problem**: Spacing looks wrong

**Causes**:

- Using `*` instead of `\times` for multiplication
- Missing braces around multi-character subscripts/superscripts

**Solution**: Use `\times` or `\cdot` for multiplication, add braces: `$r_{free}^{adjusted}$`
