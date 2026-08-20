# Test Dimensions Checklist (Part 2 of 2): Responsive Through Security

- **Responsive / breakpoints** — at each viewport: nav collapse/hamburger, text overflow, image
  scaling, modal/overlay sizing, form layout, table overflow, touch targets (≥ 24×24 CSS px per WCAG
  2.5.8; ≥ 44×44 px preferred). Compare against `*-mobile`/`*-tablet`/`*-desktop` mockups when
  provided.
- **Accessibility (WCAG 2.2 AA)** — the POUR-organized, agent-observable criteria:
  - Perceivable: alt text (1.1.1), semantic structure (1.3.1), text contrast ≥ 4.5:1 / large ≥ 3:1
    (1.4.3), non-text contrast ≥ 3:1 (1.4.11), reflow at 320 px (1.4.10), resize to 200% (1.4.4).
  - Operable: full keyboard operability (2.1.1), no keyboard trap (2.1.2), skip link (2.4.1), logical
    focus order (2.4.3), visible focus (2.4.7), focus not obscured (2.4.11), target size (2.5.8).
  - Understandable: `html lang` set (3.1.1), no context change on focus/input (3.2.1/3.2.2),
    consistent nav (3.2.3), error identification in text not color alone (3.3.1),
    labels/instructions (3.3.2), error suggestions (3.3.3).
  - Robust: valid markup / no duplicate IDs, name-role-value exposed (4.1.2), status messages
    announced via `aria-live`/`role="status"` (4.1.3).
  - Note: automated scanning catches ~30-57% of issues — keyboard and screen-reader observation are
    required for the rest.
- **Performance (Core Web Vitals)** — LCP < 2.5s (good) / > 4s (poor); INP < 200ms / > 500ms;
  CLS < 0.1 / > 0.25. Capture via Lighthouse/PageSpeed when feasible; otherwise observe load and
  interaction latency qualitatively and flag the worst offenders.
- **Cross-browser** — when the goal calls for it, note rendering/behaviour differences across
  Chrome/Safari/Firefox/Edge for the features used.
- **Safe security surface (passive, per OWASP WSTG)** — HTTP→HTTPS redirect and no mixed content;
  valid TLS; presence of `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`/CSP
  `frame-ancestors`, `Strict-Transport-Security`, `Referrer-Policy`; session-cookie
  `Secure`/`HttpOnly`/`SameSite`; no version-string over-disclosure (`Server`, `X-Powered-By`); error
  pages on bad paths do not leak stack traces/paths/queries; `robots.txt` does not advertise
  sensitive paths. Observation only — never exploit.
