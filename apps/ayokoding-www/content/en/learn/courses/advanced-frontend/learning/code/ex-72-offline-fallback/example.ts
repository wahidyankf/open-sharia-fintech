// Example 72: An Offline Fallback Page Serves When the Network Is Down. (co-34)
//
// When the network is down and the requested page is NOT cached, the service worker serves a
// pre-cached OFFLINE FALLBACK page instead of a browser error. This keeps the app usable (a branded
// "you are offline" page) rather than showing a dead tab.

// The cache holds the fallback page plus any previously-visited pages.
const cache: Map<string, string> = new Map(); // => keyed by URL
let networkOnline = true; // => flip to model going offline

// installFallback pre-caches the offline fallback page (and the app shell).
function installFallback(): void {
  // => co-34: the fallback must be cached AHEAD of time, while online
  cache.set("/offline.html", "<main>You are offline.</main>"); // => the branded fallback
  cache.set("/", "<main>Home</main>"); // => a previously-visited page (cached)
}

// fetchWithFallback tries cache -> network -> offline fallback (the standard offline strategy).
function fetchWithFallback(url: string): { body: string; source: string } {
  // => co-34: cache-first, then network, then the offline fallback -- never a dead error
  const cached = cache.get(url); // => is this URL cached?
  if (cached) return { body: cached, source: "cache" }; // => serve cached
  if (networkOnline) return { body: `<fresh ${url}>`, source: "network" }; // => online miss -> network
  return { body: cache.get("/offline.html")!, source: "offline-fallback" }; // => offline + uncached -> fallback
}

installFallback(); // => cache the fallback and the home page
networkOnline = false; // => go offline
const uncachedOffline = fetchWithFallback("/dashboard"); // => offline + not cached -> fallback
const cachedOffline = fetchWithFallback("/"); // => offline but cached -> served from cache

console.log("uncached while offline:", uncachedOffline.source, "->", uncachedOffline.body); // => Output: offline-fallback -> <main>You are offline.</main>
console.log("cached while offline:", cachedOffline.source); // => Output: cached while offline: cache
