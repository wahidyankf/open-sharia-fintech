// Example 3: Static Site Generation Pre-renders at Build Time. (co-03)
//
// SSG: pages are pre-rendered to static HTML at BUILD time, then served as plain files. Unlike
// SSR (Example 2, per-request) this HTML is identical for every visitor because it was baked once.

// A build step writes each page's HTML to a file once, ahead of any request.
const builtFiles: Map<string, string> = new Map(); // => the "build output" directory
// => a Map models the dist/ folder: filename -> static HTML contents

// buildPage renders one page to a static file at build time (runs ONCE, not per request).
function buildPage(path: string, content: string): void {
  // => at build time the content is fixed; the file will never change until the next build
  builtFiles.set(path, `<main>${content}</main>`); // => co-03: static HTML, baked once
}

buildPage("/about", "About us"); // => baked into /about.html at build time
// => every future request for /about serves the SAME bytes -- no rendering happens per request

// Two "requests" at runtime both read the identical pre-built file.
const requestA = builtFiles.get("/about"); // => runtime: just a file read
const requestB = builtFiles.get("/about"); // => runtime: the same file read

console.log("served HTML:", requestA); // => Output: served HTML: <main>About us</main>
console.log("static (byte-identical):", requestA === requestB); // => Output: static (byte-identical): true
