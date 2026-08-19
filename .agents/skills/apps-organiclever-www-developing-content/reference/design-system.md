# organiclever-www — Design System

`organiclever-www` uses the OrganicLever warm OKLCH design system. All visual tokens come
from `@open-sharia-enterprise/web-ui-token`, and all UI components from
`@open-sharia-enterprise/web-ui`.

## Token Import Chain

```css
/* apps/organiclever-www/src/app/globals.css */
@import "tailwindcss";
@source "../../../../libs/web-ui/src/**/*.{ts,tsx}";
@import "@open-sharia-enterprise/web-ui-token/src/tokens.css"; /* shared neutral baseline */
@import "@open-sharia-enterprise/web-ui-token/src/organiclever.css"; /* OL warm OKLCH palette */

@theme {
  --font-sans: var(--font-nunito), ui-sans-serif, system-ui, sans-serif;
  --font-mono: var(--font-jetbrains-mono), ui-monospace, monospace;
}
```

## Fonts

Nunito (body) and JetBrains Mono (numerics) are self-hosted via `next/font/google` in
`src/app/layout.tsx`. They generate CSS variables `--font-nunito` and
`--font-jetbrains-mono` applied to `<html>` className, then consumed by `@theme` above.

## Dark Mode Activation

```ts
// JavaScript — preferred (works with data-theme="dark" selector)
document.documentElement.setAttribute("data-theme", "dark");
document.documentElement.removeAttribute("data-theme");

// Tailwind class — also supported (legacy .dark selector)
document.documentElement.classList.add("dark");
```

Both selectors activate the same warm-dark palette in `organiclever.css`.

## Key Tokens

```css
var(--hue-teal)        /* Interactive elements, focus rings */
var(--hue-sage)        /* Primary brand, success, main CTA */
var(--hue-teal-wash)   /* Active tab backgrounds */
var(--hue-sage-wash)   /* Success alert backgrounds */
var(--warm-0)          /* Page background (warm near-white) */
var(--warm-900)        /* Body text (warm near-black) */
var(--color-primary)   /* Maps to --hue-sage */
var(--color-ring)      /* Maps to --hue-teal */
```

## web-ui Component Usage

Use components from `@open-sharia-enterprise/web-ui` — NOT from `@/components/ui/`. The
shared `web-ui` library owns the canonical component implementations.

```tsx
import {
  Button, Alert, Input, Icon, Toggle, ProgressRing,
  Sheet, AppHeader, StatCard, InfoTip, HuePicker, TabBar, SideNav,
} from "@open-sharia-enterprise/web-ui";

// Brand variants
<Button variant="teal">Primary action</Button>
<Button variant="sage" size="xl">Hero CTA</Button>
<Alert variant="success">Workout logged!</Alert>
<Alert variant="warning">Rest day recommended</Alert>

// OL-specific components
<Icon name="dumbbell" size={24} />
<Toggle value={isDark} onChange={setIsDark} label="Dark mode" />
<StatCard label="Streak" value={7} unit="days" hue="terracotta" icon="flame" />
<TabBar tabs={tabs} current={route} onChange={navigate} />
<SideNav brand={{ name: "OrganicLever", icon: "dumbbell", hue: "teal" }}
         tabs={tabs} current={route} onChange={navigate} />
```

## Dynamic Hue Backgrounds

When hue is a runtime variable, use inline style — Tailwind cannot detect template
literal class names at build time:

```tsx
/* Correct */
<div style={{ backgroundColor: `var(--hue-${hue})` }} />

/* Wrong — Tailwind strips this at build */
<div className={`bg-[var(--hue-${hue})]`} />
```

## Storybook

`libs/web-ui/.storybook/preview.ts` imports `organiclever.css` so all web-ui stories
render with the warm OL palette. Dark mode toggle uses `.dark` class (Storybook
`addon-themes` with `withThemeByClassName({ dark: 'dark' })`).
