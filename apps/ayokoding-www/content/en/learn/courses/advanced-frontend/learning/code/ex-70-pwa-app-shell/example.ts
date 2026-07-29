// Example 70: An App Shell Cached by a Service Worker. (co-34)
//
// The PWA app-shell model: the service worker pre-caches the minimal shell (the HTML, CSS, core JS)
// at install, so a REPEAT visit loads the shell instantly from cache while fresh content fills in.
// The shell is the unchanging chrome; only the data is fetched live.

// The service worker's cache, populated at install.
const shellCache: Map<string, string> = new Map(); // => the app shell's cached assets
let networkHits = 0; // => counts live network loads of the shell

// install caches the shell assets once (runs at service-worker registration).
function installShell(assets: string[]): void {
  // => co-34: the shell is pre-cached so repeat visits do not re-fetch it
  for (const a of assets) shellCache.set(a, `<shell:${a}>`); // => prime the cache
}

// loadShell serves the cached shell on a repeat visit (instant, no network).
function loadShell(): { source: "cache" | "network"; latencyMs: number } {
  // => first visit: miss -> network (slow); repeat visit: hit -> cache (instant)
  const cached = shellCache.get("/shell.html"); // => is the shell cached?
  if (cached) return { source: "cache", latencyMs: 5 }; // => co-34: instant repeat visit
  networkHits += 1; // => first visit had to load it from the network
  return { source: "network", latencyMs: 400 }; // => the slow first load
}

installShell(["/shell.html", "/app.css", "/app.js"]); // => cache the shell
loadShell(); // => first visit was the network load that primed the cache
const repeat = loadShell(); // => repeat visit -> instant from cache

console.log("repeat-visit source:", repeat.source); // => Output: repeat-visit source: cache
console.log("repeat-visit latency (ms):", repeat.latencyMs); // => Output: repeat-visit latency (ms): 5
