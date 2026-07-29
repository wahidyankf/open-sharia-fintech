// Example 4: Streaming SSR Sends a Suspense Fallback First. (co-04)
//
// Streaming SSR sends HTML in CHUNKS: a <Suspense> fallback goes out immediately, then the real
// content streams in once the async work resolves. The browser can paint the fallback before the
// slow data is ready -- the opposite of waiting for the whole page to finish server-side.

// Each chunk the server flushes down the wire, in arrival order.
const wire: string[] = []; // => the byte stream the browser receives, chunk by chunk
// => pushing in order models TCP streaming: the browser renders each chunk as it arrives

// A Suspense boundary ships its fallback IMMEDIATELY, then its children once they resolve.
function renderStreaming(fallback: string, slow: () => string): void {
  wire.push(`<!-- shell -->`); // => the page shell streams first
  wire.push(fallback); // => co-04: the fallback goes out before the slow data is ready
  // => the browser can paint the fallback now; it does NOT block on `slow()`
  wire.push(slow()); // => the resolved real content streams in later, replacing the fallback
}

// slowData models an async data fetch that is not ready for a while.
function slowData(): string {
  // => standing in for a database/API call; the point is it is NOT available up front
  return `<p>real content</p>`; // => the eventual payload
}

renderStreaming(`<p>loading...</p>`, slowData); // => fallback then content

// The wire shows the fallback BEFORE the resolved content -- the whole point of streaming.
console.log("chunks in arrival order:"); // => Output header
wire.forEach((chunk, i) => console.log(`  [${i}] ${chunk}`)); // => one line per chunk, in order
