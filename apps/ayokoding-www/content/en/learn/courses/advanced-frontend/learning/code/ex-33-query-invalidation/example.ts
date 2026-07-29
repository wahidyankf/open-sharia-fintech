// Example 33: Invalidation Triggers a Stale Query to Refetch. (co-15)
//
// After a mutation, you invalidate the affected query key. The cache marks that key STALE, and the
// next time it is observed it refetches -- so the UI converges on the new server truth without
// manual refetch wiring everywhere.

// The cache stores data plus a stale flag per query key.
interface CacheEntry {
  // => the stale flag is what invalidation flips to force a refetch
  data: string; // => the cached value
  isStale: boolean; // => true => a refetch is needed next time this key is observed
}

let networkFetches = 0; // => counts real fetches triggered by invalidation
const cache: Map<string, CacheEntry> = new Map(); // => the query cache, keyed by query key

// primeCache stands in for an initial successful fetch.
cache.set("todos", { data: "[]", isStale: false }); // => fresh after the first fetch
networkFetches = 1; // => that initial fetch

// invalidate marks a key stale WITHOUT fetching -- the refetch happens on next observation.
function invalidate(key: string): void {
  // => co-15: invalidation marks stale; the observer refetches, not the mutator
  const entry = cache.get(key); // => locate the affected key
  if (entry) entry.isStale = true; // => flip stale -- the data is now suspect
}

// observe reads the key, refetching IF it is stale (the convergence mechanism).
function observe(key: string): string {
  // => a stale key refetches on observation; a fresh key serves from cache
  const entry = cache.get(key)!;
  if (entry.isStale) {
    networkFetches += 1; // => the refetch invalidation asked for
    entry.data = '["new-todo"]'; // => the refreshed server data
    entry.isStale = false; // => fresh again
  }
  return entry.data; // => the data the UI now shows
}

observe("todos"); // => fresh -> no refetch
invalidate("todos"); // => a mutation happened -> mark stale
observe("todos"); // => stale -> refetch (#2), UI converges on the new data

console.log("network fetches:", networkFetches); // => Output: network fetches: 2
console.log("todos after invalidation:", observe("todos")); // => Output: todos after invalidation: ["new-todo"]
