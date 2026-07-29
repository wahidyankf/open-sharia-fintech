// Capstone store: a server-state cache with invalidation, an optimistic add that rolls back on
// failure, and a memoized derived selector for the filtered view. co-15 (client-vs-server-state),
// co-19 (usememo-usecallback / memoized selector).
import type { Row } from "./types";

// The server cache: the canonical row list + a stale flag (TanStack Query-style, Example 31).
interface CacheEntry {
  rows: Row[]; // the confirmed server data
  isStale: boolean; // true => a mutation asked for a refetch
}

// In-memory query cache, keyed by the single query key this dashboard uses.
const cache = new Map<string, CacheEntry>(); // => one entry for "dashboard-rows"

// prime seeds the cache with the initial fetch result (called once after the first load).
export function prime(rows: Row[]): void {
  // populate the cache fresh (not stale) after the initial fetch
  cache.set("dashboard-rows", { rows, isStale: false });
}

// read returns the cached rows (the single source of server state).
export function read(): Row[] {
  // co-15: components read from the cache, not straight from a fetch each time
  return cache.get("dashboard-rows")?.rows ?? [];
}

// invalidate marks the cache stale (a mutation happened); the next observer would refetch.
export function invalidate(): void {
  // co-15: a mutation invalidates; observers refetch (Example 33)
  const entry = cache.get("dashboard-rows");
  if (entry) entry.isStale = true;
}

// optimisticAdd shows the new row immediately and rolls back if the (simulated) mutation fails.
export function optimisticAdd(row: Row, shouldFail: boolean): { rolledBack: boolean; rows: Row[] } {
  // co-15 (Example 34): snapshot, apply optimistically, roll back on failure
  const entry = cache.get("dashboard-rows");
  if (!entry) return { rolledBack: false, rows: [] };
  const snapshot = entry.rows; // => the prior confirmed state, for rollback
  entry.rows = [...snapshot, row]; // => optimistic: the new row appears immediately
  if (shouldFail) {
    entry.rows = snapshot; // => ROLLBACK: restore the prior state on failure
    invalidate(); // => mark stale so a later refetch reconciles
    return { rolledBack: true, rows: snapshot };
  }
  invalidate(); // => success: invalidate so the next observer refetches the confirmed server truth
  return { rolledBack: false, rows: entry.rows };
}

// A memoized derived selector (co-19): the filtered view recomputes only when its inputs change.
let lastRows: Row[] | null = null; // => last input reference (cache key)
let lastQuery = ""; // => last query string (cache key)
let lastFiltered: Row[] = []; // => the cached derived result

// selectFiltered returns the rows matching the query, memoized on (rows reference, query).
export function selectFiltered(rows: Row[], query: string): Row[] {
  // co-19 (Example 36): recompute only when the rows reference or the query changes
  if (rows !== lastRows || query !== lastQuery) {
    lastRows = rows; // => store the new input reference
    lastQuery = query; // => store the new query
    lastFiltered = rows.filter((r) => r.label.toLowerCase().includes(query.toLowerCase())); // => re-derive
  }
  return lastFiltered; // => the memoized (or freshly-computed) filtered view
}

// resetForTests clears the memo + cache so each test starts from a known state.
export function resetForTests(): void {
  cache.clear();
  lastRows = null;
  lastQuery = "";
  lastFiltered = [];
}
