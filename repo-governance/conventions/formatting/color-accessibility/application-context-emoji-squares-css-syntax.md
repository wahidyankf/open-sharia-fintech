---
description: "Covers accessible-palette guidance for colored square emoji plus future CSS custom properties and syntax-highlighting themes."
when_to_use: "Use when implementing CSS theme colors or syntax-highlighting palettes that must stay color-blind accessible."
---

# Application Contexts: Emoji Squares, CSS, and Syntax Highlighting

## Emoji Colored Squares

The colored square emojis (🟦🟩🟨🟪) use the verified accessible color palette:

- 🟦 Blue (#0173B2) - Safe for all color blindness types
- 🟩 Teal (#029E73) - Safe for all color blindness types (GitHub renders as green, but actual color is from teal palette)
- 🟨 Yellow (#F1C40F) - Accessible with shape differentiation and text labels
- 🟪 Purple (#CC78BC) - Safe for all color blindness types

**Important note**: GitHub emoji rendering may vary slightly from the specified hex codes, but the semantic colors used are from the verified palette and are tested to work for all users.

## CSS/Styling (Future)

When CSS styling is implemented:

1. **Use CSS custom properties** (variables) with descriptive names:

   ```css
   --color-primary: #0173b2; /* Blue for main elements */
   --color-secondary: #de8f05; /* Orange for secondary */
   --color-success: #029e73; /* Teal for success states */
   --color-warning: #ca9161; /* Brown for warnings */
   --color-text-dark: #000000; /* Black for dark text */
   --color-text-light: #ffffff; /* White for light text */
   ```

2. **Document theme colors** in project CSS documentation

3. **Test light mode and dark mode separately** to ensure sufficient contrast

4. **Never use color names**: Always use hex codes for consistency
   - FAIL: `color: red`
   - PASS: `color: #0173B2`

5. **Include border/outline properties** for visual definition

## Syntax Highlighting (Future)

When syntax highlighting themes are implemented:

1. **Use accessible palette colors** for code highlighting
2. **Avoid red-green combinations** in error/success states
3. **Use blue for keywords** and orange for strings
4. **Use teal for comments** and purple for identifiers
5. **Maintain 3:1 minimum contrast** between text and background
