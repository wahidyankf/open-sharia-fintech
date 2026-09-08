# Islamic

Specifications for the Islamic tools product family. The family ships one logical owner today —
`islamic-be`, a Sharia-compliance API that any consumer can call, independent of the OSE
Application's GRC surface.

## Contents

- [Product overview](./overview.md) — what the family is for and who it serves.

- [Islamic BE](./be/README.md) — the specification corpus for `islamic-be`, the Sharia-compliance
  API: its architecture, its behaviours, and the OpenAPI contract its clients generate from.

## Related

- `apps/islamic-be` — the implementing project. DU3 creates it and adds the link back from here;
  a link added now would point at nothing and fail the `md-links` gate.
