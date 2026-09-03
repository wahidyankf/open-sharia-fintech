import { describe, expect, it } from "vitest";
import {
  DEFAULT_SORT_STATE,
  DEFAULT_STATE,
  PARAM_KEYS,
  decodeState,
  encodeState,
  sanitizeState,
} from "../../../../../src/features/ai-benchmark/core/url-state";
import type { FilterState } from "../../../../../src/features/ai-benchmark/core/filter";

// Pure-function tests for URL state encode/decode/sanitize (Phase 4 steps F-3..F-9), mirroring the
// calculator's proven contract: the URL is the single source of truth, defaults are OMITTED from
// the query string, and unknown values sanitize to the default rather than throwing. See prd.md
// AC-22/AC-26/AC-27.

// ─── F-3 / F-4 — decode defaults + encode omits defaults ───────────────────────

describe("decodeState — empty query yields the default unfiltered state", () => {
  it("an empty query string decodes to all-undefined (unfiltered)", () => {
    expect(decodeState(new URLSearchParams(""))).toEqual(DEFAULT_STATE);
  });

  it("DEFAULT_STATE has no filter set", () => {
    expect(DEFAULT_STATE.harness).toBeUndefined();
    expect(DEFAULT_STATE.class).toBeUndefined();
  });
});

describe("encodeState — defaults are omitted from the query string", () => {
  it("the default state encodes to an empty query string", () => {
    expect(encodeState(DEFAULT_STATE).toString()).toBe("");
  });

  it("a harness filter is encoded under its param key, class omitted when default", () => {
    const q = encodeState({ harness: "cursor" });
    expect(q.get(PARAM_KEYS.harness)).toBe("cursor");
    expect(q.has(PARAM_KEYS.class)).toBe(false);
    expect(q.toString()).toBe("harness=cursor");
  });

  it("a class filter is encoded under its param key, harness omitted when default", () => {
    const q = encodeState({ class: "opus" });
    expect(q.get(PARAM_KEYS.class)).toBe("opus");
    expect(q.has(PARAM_KEYS.harness)).toBe(false);
    expect(q.toString()).toBe("class=opus");
  });

  it("both filters are encoded when both are set", () => {
    const q = encodeState({ harness: "cursor", class: "sonnet" });
    expect(q.get(PARAM_KEYS.harness)).toBe("cursor");
    expect(q.get(PARAM_KEYS.class)).toBe("sonnet");
  });
});

// ─── F-5 / F-6 — unknown values sanitize to default (no throw) ─────────────────

describe("decodeState / sanitizeState — unknown values fall back to unfiltered, never throw", () => {
  it("an unknown harness value decodes to undefined (unfiltered)", () => {
    const s = decodeState(new URLSearchParams("harness=not-a-real-harness"));
    expect(s.harness).toBeUndefined();
    expect(s.class).toBeUndefined();
  });

  it("an unknown class value decodes to undefined (unfiltered)", () => {
    const s = decodeState(new URLSearchParams("class=ultra"));
    expect(s.class).toBeUndefined();
    expect(s.harness).toBeUndefined();
  });

  it("sanitizeState drops unknown values without throwing", () => {
    const sanitized = sanitizeState({
      harness: "bogus" as unknown as FilterState["harness"],
      class: "nope" as unknown as FilterState["class"],
    });
    expect(sanitized).toEqual(DEFAULT_STATE);
  });

  it("a known harness and known class survive sanitizeState", () => {
    expect(sanitizeState({ harness: "cursor", class: "haiku" })).toEqual({
      harness: "cursor",
      class: "haiku",
      ...DEFAULT_SORT_STATE,
    });
  });

  it("sanitizeState is idempotent", () => {
    const s: FilterState = { harness: "cursor", class: "opus" };
    expect(sanitizeState(sanitizeState(s))).toEqual({ ...s, ...DEFAULT_SORT_STATE });
  });
});

// ─── F-7 / F-8 — round-trip every valid query string ───────────────────────────

describe("encodeState ∘ decodeState — round-trips for every valid query string", () => {
  const cases: Array<{ name: string; query: string }> = [
    { name: "empty", query: "" },
    { name: "harness only", query: "harness=claude-code" },
    { name: "harness cursor", query: "harness=cursor" },
    { name: "harness opencode-go", query: "harness=opencode-go" },
    { name: "class opus", query: "class=opus" },
    { name: "class sonnet", query: "class=sonnet" },
    { name: "class haiku", query: "class=haiku" },
    { name: "class unrated", query: "class=unrated" },
    { name: "both filters", query: "harness=cursor&class=sonnet" },
    { name: "both filters (other harness)", query: "harness=opencode-zen&class=haiku" },
  ];

  it.each(cases)("round-trips: $name — encodeState(decodeState($query)) is stable", ({ query }) => {
    const decoded = decodeState(new URLSearchParams(query));
    const reEncoded = encodeState(decoded).toString();
    // The round-trip must reach a fixed point: encoding the decoded state reproduces a canonical
    // query equal to the input after default-omission normalization.
    expect(reEncoded).toBe(query);
  });

  it("a query with extra unknown params decodes (ignoring them) and round-trips cleanly", () => {
    const decoded = decodeState(new URLSearchParams("harness=cursor&garbage=x&class=opus"));
    expect(decoded).toEqual({ harness: "cursor", class: "opus", ...DEFAULT_SORT_STATE });
    expect(encodeState(decoded).toString()).toBe("harness=cursor&class=opus");
  });

  // AC-67 (cycle 3.3): the retired "class=light" value is no longer a known band, so it must
  // sanitize to the default unfiltered state, exactly like any other unrecognized class value.
  it("a retired class=light value decodes to the default unfiltered state (class: undefined)", () => {
    const decoded = decodeState(new URLSearchParams("class=light"));
    expect(decoded.class).toBeUndefined();
    expect(decoded).toEqual(DEFAULT_STATE);
  });
});

// ─── Sort params (Phase 1) — round-trip the four per-band sort choices ─────────

describe("encodeState / decodeState — round-trip the four per-band sort params", () => {
  it("round-trips a non-default sort mode for each of the three rated bands", () => {
    const state = {
      harness: undefined,
      class: undefined,
      opus: "price-asc" as const,
      sonnet: "price-desc" as const,
      haiku: "price-asc" as const,
    };
    const encoded = encodeState(state);
    expect(encoded.get("sort-opus")).toBe("price-asc");
    expect(encoded.get("sort-sonnet")).toBe("price-desc");
    expect(encoded.get("sort-haiku")).toBe("price-asc");
    expect(decodeState(encoded)).toEqual(state);
  });

  // AC-67 (cycle 3.3): a full query string using the renamed `class`/`sort-haiku` wire values
  // round-trips to itself exactly — the identifier and its URL-parameter wire format move
  // together, with NO legacy alias for the retired per-band sort key (DD-35 — no-alias by design).
  // Rule-15 UWT-015 fix: `sortHaiku` (camelCase) renamed to `sort-haiku` (kebab-case), matching
  // every VALUE on this page already being kebab-case — same no-legacy-alias precedent.
  it("round-trips a full query string using the renamed class=haiku and sort-haiku parameters", () => {
    const query = "class=haiku&sort-haiku=price-asc";
    const decoded = decodeState(new URLSearchParams(query));
    const reEncoded = encodeState(decoded).toString();
    expect(reEncoded).toBe(query);
  });

  // Regression (pr-review-synthesis-maker MEDIUM finding): a `sortUnrated` param used to exist and
  // fully round-trip here despite having zero rendering effect — the `unrated` band is never
  // sorted (`benchmark-chart.tsx`'s `RATED_BANDS` excludes it) and never had a dropdown. Removed
  // rather than wired up (see `SORT_PARAM_KEYS`'s docstring); this asserts the URL no longer
  // recognizes it at all, so a stale bookmarked `sortUnrated=...` link is silently ignored, never
  // resurrected.
  it("ignores an unrecognized sortUnrated query param entirely — it is not a known param key", () => {
    const decoded = decodeState(new URLSearchParams("sortUnrated=price-desc"));
    expect(decoded).toEqual(DEFAULT_STATE);
    expect(encodeState(decoded).toString()).toBe("");
  });

  it("an unrecognized sort-sonnet value in the URL sanitizes to the default (capability), never throwing", () => {
    expect(() => decodeState(new URLSearchParams("sort-sonnet=not-a-real-value"))).not.toThrow();
    const decoded = decodeState(new URLSearchParams("sort-sonnet=not-a-real-value"));
    expect(decoded.sonnet).toBe("capability");
    // The other two bands are unaffected by the one unrecognized value.
    expect(decoded.opus).toBe("capability");
    expect(decoded.haiku).toBe("capability");
  });
});

// ─── decodeState → FilterState is usable by filterModels (contract) ────────────

describe("decodeState output — feeds filterModels directly", () => {
  it("decodes a known harness to the typed HarnessId", () => {
    expect(decodeState(new URLSearchParams("harness=codex-cli")).harness).toBe("codex-cli");
  });
  it("decodes a known class to the typed Band", () => {
    expect(decodeState(new URLSearchParams("class=unrated")).class).toBe("unrated");
  });
});
