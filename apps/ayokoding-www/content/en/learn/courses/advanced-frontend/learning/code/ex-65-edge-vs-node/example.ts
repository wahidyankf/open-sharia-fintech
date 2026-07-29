// Example 65: The Edge Runtime Web API Subset Rejects a Node API. (co-32)
//
// The edge runtime is a SUBSET of Web APIs in a V8 isolate -- it deliberately omits Node-only
// modules like `node:fs`, `node:path`, and the `Buffer`/`process` Node globals. Using one is a
// build-time error: the edge runtime simply does not provide it.

// The APIs each runtime exposes.
const RUNTIME_APIS: Record<"nodejs" | "edge", Set<string>> = {
  // => nodejs has the full Node stdlib; edge has only the Web subset
  nodejs: new Set(["fetch", "Request", "Response", "node:fs", "node:path", "Buffer", "process"]),
  edge: new Set(["fetch", "Request", "Response"]), // => co-32: Web APIs only -- no node:*, no Buffer
};

// canUse returns whether `api` is available in the chosen runtime.
function canUse(runtime: "nodejs" | "edge", api: string): boolean {
  // => co-32: a Node-only API is simply absent from the edge runtime's API set
  return RUNTIME_APIS[runtime].has(api); // => false for node:fs on edge
}

// A route that imports node:fs compiled for the edge -> rejected.
const edgeChecks = ["fetch", "node:fs", "Buffer"].map((api) => ({
  api, // => the import the handler tried to use
  available: canUse("edge", api), // => whether the edge runtime provides it
}));

edgeChecks.forEach((c) => console.log(`edge runtime has ${c.api}: ${c.available}`)); // => Output: three lines
console.log("node:fs usable on edge:", canUse("edge", "node:fs")); // => Output: node:fs usable on edge: false
