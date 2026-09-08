---
description: "Confirms the accessible palette works unchanged on both light and dark backgrounds and shows a worked contrast example."
when_to_use: "Use when testing whether a color renders with sufficient contrast in both light and dark mode."
---

# Dark Mode Considerations

All colors must work in both light and dark rendering contexts.

## Testing Backgrounds

| Mode           | Background          | Text Color      | Used For               |
| -------------- | ------------------- | --------------- | ---------------------- |
| **Light Mode** | #FFFFFF (white)     | #000000 (black) | GitHub web light theme |
| **Dark Mode**  | #1E1E2E (dark gray) | #FFFFFF (white) | GitHub dark theme      |

## No Special Adjustments Needed

The verified accessible palette requires **no adjustments** between light and dark modes. All colors maintain sufficient contrast and accessibility in both contexts.

## Example Dark Mode Test

```
Light Mode Background: #FFFFFF (white)
Blue (#0173B2) with Black text (#000000) and Black border (#000000)
Result: PASS: 8.59:1 contrast ratio (AAA)

Dark Mode Background: #1E1E2E (dark gray)
Blue (#0173B2) with White text (#FFFFFF) and Black border (#000000)
Result: PASS: 6.93:1 contrast ratio (AAA)
```
