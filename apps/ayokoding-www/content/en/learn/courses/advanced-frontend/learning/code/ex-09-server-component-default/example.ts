// Example 9: A Server Component Ships No Client JS. (co-07)
//
// A server component (the DEFAULT -- no 'use client') renders to HTML on the server and ships NO
// client JavaScript for itself. Its output is plain markup; the browser never receives a JS bundle
// for it. This is the complement of Example 8's client boundary.

// A component is either server (no JS) or client (ships JS).
interface Ship {
  // => the only fact that matters here: how many JS bytes this component adds to the client bundle
  component: string; // => the component's name
  clientJsBytes: number; // => 0 for a server component; >0 for a client component
}

// A server component renders to an HTML string and contributes ZERO client bytes.
function serverComponent(): { html: string; ship: Ship } {
  // => the render runs on the server; nothing about it is sent as executable JS
  return {
    html: `<nav><a href="/">Home</a></nav>`, // => pure markup in the response
    ship: { component: "Nav", clientJsBytes: 0 }, // => co-07: no client JS for a server component
  };
}

const result = serverComponent(); // => the server renders Nav to HTML
// => the browser receives the <nav> markup but no Nav.js bundle -- it is inert, fast, cacheable

console.log("server HTML:", result.html); // => Output: server HTML: <nav><a href="/">Home</a></nav>
console.log("client JS shipped:", result.ship.clientJsBytes, "bytes"); // => Output: client JS shipped: 0 bytes
