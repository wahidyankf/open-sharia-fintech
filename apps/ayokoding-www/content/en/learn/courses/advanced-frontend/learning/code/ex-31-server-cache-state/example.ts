// Example 31: A Server Cache Skips the Network on a Cached Read. (co-15)
//
// A server-state cache (TanStack Query-style) stores the result of a fetch keyed by a query key.
// A second read of the same key within the cache window serves the stored data WITHOUT hitting the
// network -- the defining benefit of separating server cache state from component state.

// Counters track how many real network fetches happened vs. how many reads were served.
let networkFetches = 0; // => increments only on a genuine network round trip
// => reads - networkFetches = cache hits (the proof the cache worked)

// A query cache: query key -> cached data (+ its freshness).
const cache: Map<string, { data: string }> = new Map(); // => keyed by the query key string
// => a Map models the in-memory query cache TanStack Query keeps per key

// fetchUser is the "network" function -- expensive, and what the cache exists to avoid repeating.
function fetchUser(id: string): string {
  // => stands in for an HTTP GET /users/{id}
  networkFetches += 1; // => record a real network call
  return `user-${id}`; // => the fetched data
}

// readQuery returns cached data if present, otherwise fetches and caches (the staleWhileCached rule).
function readQuery(key: string): string {
  // => co-15: a cached key skips the network; a miss populates the cache
  const cached = cache.get(key); // => is this key already in the cache?
  if (cached) return cached.data; // => cache hit -> serve without the network
  const data = fetchUser(key); // => cache miss -> fetch and store
  cache.set(key, { data }); // => populate for next time
  return data; // => the freshly-fetched data
}

readQuery("42"); // => miss -> network fetch (#1)
readQuery("42"); // => HIT -> no network
readQuery("42"); // => HIT -> no network

console.log("reads: 3, network fetches:", networkFetches); // => Output: reads: 3, network fetches: 1
