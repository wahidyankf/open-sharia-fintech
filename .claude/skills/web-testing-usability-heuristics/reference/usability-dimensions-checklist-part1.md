# Usability Dimensions Checklist (Part 1 of 2): Predictability Through Cognitive Load

Apply the dimensions relevant to the goal; record which were covered and which were not. Each bullet
names the principle a violation cites.

- **Predictability & conformity to expectations** — the UI behaves the way its context and
  conventions imply; no surprising context changes on focus or input (ISO 9241-110 §3 _conformity
  with user expectations_; WCAG 3.2.1 On Focus, 3.2.2 On Input). The interface is
  **self-descriptive** — it explains its own capabilities (ISO 9241-110 §2).
- **Consistency — internal & external** — identical elements look and behave identically across the
  page and sibling pages (internal); navigation, icons, form patterns, and terminology match what
  users know from other sites (external; Jakob's Law; WCAG 3.2.3 Consistent Navigation, 3.2.4
  Consistent Identification). Heuristic 4.
- **Information scent & wayfinding** — labels and links predict their destinations; nav,
  breadcrumbs, and active-state cues tell the user where they are and where a click leads (Pirolli &
  Card; Heuristic 6).
- **Information flow & visual hierarchy** — content is scannable; the most important thing is the
  most prominent thing; related items are grouped (Law of Proximity); reading order matches
  importance; the page chunks information into digestible groups rather than a wall (Miller's Law;
  Krug).
- **Recognition over recall** — the user is not forced to remember data, codes, or earlier choices
  across steps; options and previously-entered context stay visible (Heuristic 6; WCAG 3.3.7
  Redundant Entry).
- **Feedback & system status** — every action produces visible, timely feedback; loading/empty/
  success/error states exist and read clearly; perceived response stays snappy (Heuristic 1; Doherty
  Threshold — interactions over ~400 ms need a progress indicator to bridge the wait).
- **Edge & boundary UX states (always probe — find at least one, or state explicitly that a genuine
  attempt surfaced none)** — judge the states a happy-path demo skips: the **empty / zero-result /
  no-data** state (does the page explain there is nothing yet and what to do next?), the **loading**
  state (timely progress feedback?), the **error** state (plain-language and recoverable?), the
  **first-visit vs. returning** experience, and the response to **extreme or very long content** and
  **slow / offline** conditions. Each is judged for predictability, clarity, and recoverability
  against the cited principle (Heuristics 1, 5, 9; WCAG 3.3). A confusing or missing edge state is a
  finding; a sensible behaviour a first-timer would expect but the page lacks becomes a
  `spec-suggestions.md` entry.
- **Error prevention & humane recovery** — risky actions are guarded (confirmation, constraints,
  sensible defaults); when errors occur, messages are plain-language, specific, and suggest a fix,
  identified in text not colour alone (Heuristics 5 & 9; WCAG 3.3.1 Error Identification, 3.3.2
  Labels or Instructions, 3.3.3 Error Suggestion).
- **Cognitive load & decision cost** — the number and complexity of choices at each step is
  manageable; menus/option-sets are chunked rather than overwhelming (Hick's Law, Miller's Law); the
  design is minimalist, free of clutter that competes with the primary task (Heuristic 8).
