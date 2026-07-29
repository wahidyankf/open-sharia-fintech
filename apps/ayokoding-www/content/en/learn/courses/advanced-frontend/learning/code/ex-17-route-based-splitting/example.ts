// Example 17: Route Based Code Splitting. (co-13)
//
// Split bundles per ROUTE: each route's components live in their own chunk, loaded only when the
// user navigates to that route. A visitor on the home page never downloads the dashboard's code,
// and vice versa. This is Example 16's lazy-load idea applied at the route level.

// Each route maps to the chunk that owns its components.
const routeChunks: Record<string, string> = {
  // => a record keyed by path; the value is the chunk name that route needs
  "/": "home.chunk", // => the home route's code
  "/dashboard": "dashboard.chunk", // => the dashboard route's code (heavy, charts)
  "/settings": "settings.chunk", // => the settings route's code
};

// loaded tracks which chunks have actually been fetched (a Set of chunk names).
const loaded = new Set<string>(); // => starts empty; nothing is loaded until a route is visited
// => a Set models "the browser's cache of already-fetched chunks"

// navigateTo models a route change: the route's chunk is fetched on first visit.
function navigateTo(path: string): string {
  // => co-13: the route's chunk loads on demand, the first time the route is entered
  const chunk = routeChunks[path]; // => the chunk this route owns
  if (!loaded.has(chunk)) loaded.add(chunk); // => first visit -> fetch the chunk
  return chunk; // => the chunk now resident for this route
}

// A user session: home -> dashboard -> settings -> dashboard again.
navigateTo("/"); // => loads home.chunk
navigateTo("/dashboard"); // => loads dashboard.chunk (heavy charts)
navigateTo("/settings"); // => loads settings.chunk
navigateTo("/dashboard"); // => already loaded -- no second fetch

console.log("chunks loaded after the session:", Array.from(loaded)); // => three chunks, dashboard not re-fetched
console.log("dashboard chunk in cache:", loaded.has("dashboard.chunk")); // => Output: dashboard chunk in cache: true
