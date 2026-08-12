# BeaverNest Flutter Web Visual Assets

These plan-owned high-fidelity references make the three responsive, UI-bearing surfaces concrete
before implementation. Each image is an illustrative Flutter Web layout with Desktop (>=1024 px),
Tablet (768–1023 px), and Mobile (<768 px) artboards; they show responsive reflow, not a native
Android or macOS delivery.

| Surface                   | Candidate A                                                       | Candidate B                                                    | Selected treatment       |
| ------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------ |
| Status workspace          | [Focused Status Dashboard](./status-dashboard.excalidraw.png)     | [Operations Console](./operations-console.excalidraw.png)      | Focused Status Dashboard |
| Diagnostics workspace     | [Compact support snapshot](./diagnostics-screen-a.excalidraw.png) | [Recent-check timeline](./diagnostics-screen-b.excalidraw.png) | Compact support snapshot |
| Browser shortcut guidance | [Contextual help panel](./install-guidance-a.excalidraw.png)      | [Dedicated help card](./install-guidance-b.excalidraw.png)     | Dedicated help card      |

Status candidates annotate loading, unavailable, retry-in-progress, and keyboard focus. Diagnostics
candidate ready cards and unavailable panels are mutually exclusive state examples: an unavailable
response replaces (rather than accompanies) version, uptime, and server-time data. Diagnostics
candidates contain only the contracted safe snapshot fields and an unavailable state without a cause.
Shortcut candidates annotate visible focus, close/Escape behavior, focus return, and a 44 px minimum
interactive target.

The browser chrome is illustrative. It does not promise HTTPS, a PWA, a service worker, offline
operation, immediate automatic updates, native packaging, or a browser action that every user agent
offers. The product requirements are authoritative for those boundaries.
