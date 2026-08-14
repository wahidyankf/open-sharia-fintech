# Testing Methodology — Session-Based Exploratory Testing

Structure the work as one or more **time-boxed charters** (Session-Based Test Management). Each
charter is a focused mission; opportunistic findings outside the charter are still recorded.

## 1. Frame charters

Use Elisabeth Hendrickson's template:

```
Explore <target / area / feature / risk>
With   <tools / data / viewports / locales / restrictions>
To discover <information / risk class / quality attribute>
```

Derive charters from the goal. Example for "verify the salary calculator":

- `Explore the calculator's city/role filters with each filter level independently to discover
scope-handling defects.`
- `Explore the calculator at 320/375/768/1024/1280 px in en + id to discover responsive and design
parity defects against the assets/ mockups.`

## 2. Apply tours to vary the angle of attack

Pick tours that fit the goal (James Whittaker's taxonomy):

- **Money / Landmark tour** — the marketed, primary flows in varying order.
- **FedEx tour** — data lifecycle: create → modify → store → display.
- **Antisocial / Intellectual tour** — invalid, out-of-order, boundary, and complex inputs.
- **Supermodel tour** — appearance, layout, design parity, responsive behaviour.
- **Obsessive-Compulsive tour** — repeat the same action to surface state bugs.
- **Back Alley tour** — least-used features and edge interactions.

## 3. Cover the product surface with SFDIPOT

Sweep the "San Francisco Depot" heuristic so coverage is not accidental:

- **S**tructure — pages, routes, components, assets that render.
- **F**unction — what each feature does; outputs; computed values.
- **D**ata — inputs/outputs: boundaries, nulls, special chars, Unicode/emoji, large values, encodings.
- **I**nterfaces — links, forms, third-party widgets, API calls visible in the network panel.
- **P**latform — browser engine, viewport, device, locale/timezone.
- **O**perations — real user journeys, error recovery, back/refresh behaviour.
- **T**ime — session expiry, ordering, debounce/race, date/time edge cases, perceived performance.

## 4. Judge against quality criteria (CRUSSPIC STMPL)

Probe Capability, Reliability, Usability, Security, Scalability, Performance, Installability,
Compatibility — and Supportability, Testability, Maintainability, Portability, Localizability where
observable. Most web charters lean on Capability, Usability, Performance, Compatibility, and
Localizability.
