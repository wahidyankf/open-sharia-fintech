# web-ui Specs

Gherkin behavioral specifications for [web-ui](../../../libs/web-ui/README.md), the shared React
component library.

## Purpose

These specs define the **observable behavior** of every `web-ui` component: what a user sees and
can do, and what accessibility contract each component honors. They are the shared contract
between design, development, and QA.

## Structure

```
specs/libs/web-ui/
├── README.md
├── product/               # C4 L1 product framing
├── system-context/        # C4 L1 actors and consumers
├── containers/            # C4 L2 deployable units
├── components/            # C4 L3 component catalogue
└── behavior/
    └── gherkin/           # Gherkin feature files organized by component
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
        ├── sheet/
        ├── side-nav/
        ├── stat-card/
        ├── tab-bar/
        ├── textarea/
        └── toggle/
```

## Running the Tests

```bash
nx run web-ui:test:unit
```

Every scenario is consumed at the unit level via the matching `*.steps.tsx` file co-located with
each component under `libs/web-ui/src/components/`.

- [Behavior — web-ui](./behavior/README.md)
- [Components — web-ui](./components/README.md)
- [Containers — web-ui](./containers/README.md)
- [Product — web-ui](./product/README.md)
- [System Context — web-ui](./system-context/README.md)
