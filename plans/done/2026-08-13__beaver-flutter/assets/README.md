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

## Selected-Visual Verification

The selected references below retain their two finalist alternatives and make the required behavior
reviewable before Flutter implementation. The status reference follows the legacy shell's
readiness-first card, labelled icons, polite state change, and Refresh status action. The new Flutter
widgets are visual equivalents, not React component reuse.

| Selected visual                                                   | Responsive behavior                                                                                                 | Focus and error behavior                                                                                                                                                                                                  | Web-only safe-data boundary                                                                                                                                                                 |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Focused Status Dashboard](./status-dashboard.excalidraw.png)     | All three artboards are retained: a desktop rail, a tablet status grid, and a stacked mobile status flow.           | The Refresh status control has a visible focus outline. Loading, unavailable, and retry-in-progress swatches show recoverable state without a page reload.                                                                | Displays only application, database, schema, and refresh status; it makes no endpoint, native, offline, or installation claim.                                                              |
| [Compact support snapshot](./diagnostics-screen-a.excalidraw.png) | All three artboards are retained: desktop cards with a rail, tablet two-column grouping, and a stacked mobile view. | Retry diagnostics has a visible focus outline. Diagnostics unavailable is a no-cause error treatment; its ready fields and unavailable panel are alternative states, never one response.                                  | Shows only contracted version, uptime, server UTC time, and readiness components; it excludes paths, hosts, exceptions, SQL, migrations, and causal detail.                                 |
| [Dedicated help card](./install-guidance-b.excalidraw.png)        | All three artboards are retained: desktop, tablet, and mobile card layouts preserve the same reading order.         | Close has a visible focus outline; Escape closes the card and returns focus to Help. Because the card performs no install operation, browser unavailability is stated as a caveat, not invented as an installation error. | It says an add-to-home-screen shortcut is browser-dependent and requires an internet connection; it promises no PWA, service worker, offline mode, HTTPS, auto-update, or native packaging. |

The browser chrome is illustrative. It does not promise HTTPS, a PWA, a service worker, offline
operation, immediate automatic updates, native packaging, or a browser action that every user agent
offers. The product requirements are authoritative for those boundaries.
