// Capstone server layer: a streaming-SSR renderer, the data fetch, and a Lighthouse-style Core
// Web Vitals measurement. co-04 (streaming-ssr), co-08 (core-web-vitals), co-30 (data fetching).
import type { CoreWebVitals, LoadState, Page, Row } from "./types";

// The seed rows the "server" owns; pagination slices this list by cursor.
const SEED: Row[] = [
  { id: "1", label: "buy bread" },
  { id: "2", label: "buy milk" },
  { id: "3", label: "sell car" },
  { id: "4", label: "buy eggs" },
  { id: "5", label: "walk dog" },
  { id: "6", label: "sell bike" },
];

// PAGE_SIZE rows per page (co-30 pagination).
const PAGE_SIZE = 3;

// fetchPage simulates a server fetch of one page starting at `cursor`.
export function fetchPage(cursor: number | null): Promise<Page<Row>> {
  // cursor=null starts at index 0; otherwise resume from the cursor (keyset position).
  const start = cursor ?? 0; // => the keyset position to resume from
  const items = SEED.slice(start, start + PAGE_SIZE); // => the PAGE_SIZE rows on this page
  const nextCursor = start + PAGE_SIZE < SEED.length ? start + PAGE_SIZE : null; // => null = last page
  return Promise.resolve({ items, nextCursor }); // => resolves synchronously here (no real network)
}

// renderToStream models streaming SSR (co-04): the shell + fallback stream first, then the rows.
export function renderToStream(state: LoadState, query: string): string[] {
  // the chunks stream in arrival order: shell, fallback, then resolved content
  const chunks: string[] = ["<!-- shell -->"]; // => the static shell streams first
  if (state.status === "loading") {
    chunks.push('<p role="status">Loading dashboard...</p>'); // => co-04: the Suspense fallback
    return chunks; // => the fallback paints before the data resolves
  }
  if (state.status === "error") {
    chunks.push(`<p role="alert">${state.message}</p>`); // => the error state
    return chunks;
  }
  // loaded: filter by the query (the derived selector in store.ts does this for the live DOM;
  // here the SSR string mirrors it).
  const matches = state.rows.filter((r) => r.label.includes(query));
  chunks.push(`<ul>${matches.map((r) => `<li>${r.label}</li>`).join("")}</ul>`); // => resolved content
  return chunks;
}

// measureCwv is a deterministic Lighthouse stand-in: it derives the triad from a paint latency and
// a hasReservedSpace flag, so the baseline (slow, no reserved space) and the improved version
// (fast, reserved) produce different, comparable numbers. co-08 / co-11 / co-31.
export function measureCwv(paintMs: number, hasReservedSpace: boolean): CoreWebVitals {
  // LCP tracks the paint latency; INP tracks a proportional responsiveness; CLS is 0 only when
  // the image/row boxes had reserved dimensions (co-11/co-31).
  return {
    lcp: paintMs, // => LCP ~= first meaningful paint
    inp: Math.round(paintMs * 0.05) + 80, // => a responsiveness proxy (worse when paint is slow)
    cls: hasReservedSpace ? 0.05 : 0.3, // => reserved boxes => stable layout
  };
}

// rating bands the CWV the way web.dev / Example 13 does.
export function rate(v: CoreWebVitals): "good" | "poor" {
  // all three must meet "good" for the page to be rated good (the capstone's improvement bar)
  if (v.lcp <= 2500 && v.inp <= 200 && v.cls <= 0.1) return "good";
  return "poor";
}
