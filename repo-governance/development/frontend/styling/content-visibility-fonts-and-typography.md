---
description: Never hide content on mobile (adapt the layout instead), use next/font for all font loading, and use clamp() or Tailwind responsive utilities for text that scales between breakpoints
when_to_use: Use when a component might hide content on small screens, when adding a font, or when sizing text that must scale across breakpoints.
---

# Content Visibility, Font Loading, and Fluid Typography

## No Content Hiding

Content must be accessible at all viewports. Never use `hidden` or `sr-only` to remove content on mobile — adapt the layout instead.

```tsx
/* Wrong — content removed on mobile */
<aside className="hidden md:block">
  <Navigation />
</aside>

/* Correct — layout adapts; content always present */
<aside className="w-full md:w-64">
  <Navigation />
</aside>
```

If a full sidebar cannot fit on mobile, move it into a slide-over drawer or an accordion — do not amputate it.

## Font Loading

Use `next/font` for all font loading. Do not declare `font-family` in CSS files.

```tsx
/* Correct — next/font in layout.tsx */
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

```css
/* Wrong — font-family in globals.css */
@layer utilities {
  body {
    font-family: Arial, Helvetica, sans-serif;
  }
}
```

**Known violation**: `organiclever-www/src/app/globals.css` declares `font-family: Arial, Helvetica, sans-serif` inside `@layer utilities`. This is scheduled for removal in favour of a `next/font` declaration in the app's root layout.

## Fluid Typography

Use `clamp()` or Tailwind responsive font-size utilities for text that must scale between breakpoints.

```tsx
/* Tailwind responsive utilities — simple and sufficient for most cases */
<h1 className="text-2xl md:text-4xl lg:text-5xl font-bold">

/* clamp() — for smooth scaling without breakpoint jumps */
<h1 style={{ fontSize: "clamp(1.5rem, 4vw, 3rem)" }}>
```

Prefer Tailwind responsive utilities for headings and body text. Reserve `clamp()` for display text or hero headings where smooth scaling matters.
