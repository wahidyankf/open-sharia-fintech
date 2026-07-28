import { describe, expect, it } from "vitest";
import { DEFAULT_STATE, PARAM_KEYS, decodeState, encodeState, sanitizeState } from "./url-state";
import type { FilterState } from "./filter";

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
    expect(sanitizeState({ harness: "cursor", class: "light" })).toEqual({ harness: "cursor", class: "light" });
  });

  it("sanitizeState is idempotent", () => {
    const s: FilterState = { harness: "cursor", class: "opus" };
    expect(sanitizeState(sanitizeState(s))).toEqual(s);
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
    { name: "class light", query: "class=light" },
    { name: "class unrated", query: "class=unrated" },
    { name: "both filters", query: "harness=cursor&class=sonnet" },
    { name: "both filters (other harness)", query: "harness=opencode-zen&class=light" },
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
    expect(decoded).toEqual({ harness: "cursor", class: "opus" });
    expect(encodeState(decoded).toString()).toBe("harness=cursor&class=opus");
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
