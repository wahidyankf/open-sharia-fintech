# Behaviors — web-ui

Gherkin feature files for [web-ui](../../../../libs/web-ui/README.md), one folder per component.

```
specs/libs/web-ui/behaviors/
├── alert/
├── app-header/
├── badge/
├── button/
├── card/
├── code-block/
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

## Consumption

`nx run web-ui:test:unit` consumes every scenario here through the matching `*.steps.tsx` file
co-located with its component under `libs/web-ui/src/components/`. A primitive MAY carry Gherkin
coverage the same way: `code-block` and `resizable-panel` under `libs/web-ui/src/primitives/` do,
and the remaining primitives have none.
