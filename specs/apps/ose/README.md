# OSE

Specifications for the OSE product family. Three distinct products share this tree — the OSE
Application (`ose-app-web` + `ose-be`, the AI-assisted GRC platform at `app.oseplatform.com`), OSE
Platform Web (`ose-www`, the marketing and updates site at `oseplatform.com`), and OSE LMS
(`ose-lms-be`, the learning-management backend) — across four logical owners.

## Contents

- [Product overview](./overview.md) — what OSE is for and who it serves.
- [Deployment topology](./deployment.md) — the environments each deployable runs in.

- [OSE App Web](./app-web/README.md) — the specification corpus for `ose-app-web`, the compliance
  gap-analysis client: its architecture and its behaviours.
- [OSE BE](./be/README.md) — the specification corpus for `ose-be`, the gap-analysis API: its
  architecture, its behaviours, and the OpenAPI contract both sides generate from.
- [OSE LMS BE](./lms-be/README.md) — the specification corpus for `ose-lms-be`, the
  learning-management API: its architecture, its behaviours, and the OpenAPI contract the service
  generates its models from.
- [OSE Web](./www/README.md) — the specification corpus for `ose-www`, the platform's public site:
  its architecture and its behaviours.

## Related

- [`apps/ose-app-web/README.md`](../../../apps/ose-app-web/README.md) — the app client.
- [`apps/ose-be/README.md`](../../../apps/ose-be/README.md) — the backend service.
- [`apps/ose-lms-be/README.md`](../../../apps/ose-lms-be/README.md) — the LMS backend service.
- [`apps/ose-www/README.md`](../../../apps/ose-www/README.md) — the public site.
