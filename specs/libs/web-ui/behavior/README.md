# Behavior — web-ui

Gherkin behavioral specifications for [web-ui](../../../../libs/web-ui/README.md), the shared
React component library.

## Structure

Feature files live under `behavior/gherkin/<component>/`, one folder per component:

```
specs/libs/web-ui/
├── README.md
├── product/           # C4 L1 product framing
├── system-context/     # C4 L1 actors and consumers
├── containers/         # C4 L2 deployable units
├── components/         # C4 L3 component catalogue
└── behavior/
    └── gherkin/         # Gherkin feature files organized by component
        ├── alert/
        ├── app-header/
        ├── badge/
        ├── button/
        ├── card/
        ├── dialog/
        ├── hue-picker/
        ├── icon/
        ├── info-tip/
        ├── input/
        ├── label/
        ├── progress-ring/
        ├── resizable-panel/
        ├── sheet/
        ├── side-nav/
        ├── stat-card/
        ├── tab-bar/
        ├── textarea/
        └── toggle/
```

## Running the tests

```bash
nx run web-ui:test:unit
```

Every scenario is consumed at the unit level via the matching `*.steps.tsx` file co-located with
each component under `libs/web-ui/src/components/`. `libs/web-ui/src/primitives/` MAY also carry
Gherkin coverage the same way — `resizable-panel` (`libs/web-ui/src/primitives/resizable-panel/resizable-panel.steps.tsx`)
is the first primitive to do so; the remaining `primitives/` folders have none.
