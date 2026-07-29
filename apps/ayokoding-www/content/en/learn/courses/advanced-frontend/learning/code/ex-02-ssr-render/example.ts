// Example 2: Server Side Rendering Returns Complete HTML. (co-02)
//
// SSR: the server returns FULLY-FORMED HTML per request -- the content exists before any JS
// runs. Contrast Example 1's empty shell: here the response body already contains the content,
// so the page is readable (and indexes) immediately.

// The smallest component model: a tag plus the text it wraps.
interface Component {
  // => only the two fields the HTML-string claim actually depends on
  tag: string; // => the element type
  text: string; // => the wrapped text content
}

// renderToString turns a component into its HTML string WITH content baked in.
function renderToString(c: Component): string {
  // => the server-side equivalent of React's renderToString -- markup, not a data object
  return `<${c.tag}>${c.text}</${c.tag}>`; // => angle brackets => a real HTML string
}

// Each request calls renderToString and gets COMPLETE HTML back.
const first = renderToString({ tag: "h1", text: "Hello, SSR" }); // => request 1's body
const second = renderToString({ tag: "h1", text: "Hello, SSR" }); // => request 2's body
// => SSR produces the identical complete HTML on every request -- it is not cached at build (that is Example 3)

// Pre-JS, the content is ALREADY present in the string -- the key difference from CSR.
console.log("SSR HTML (pre-JS):", first); // => Output: SSR HTML (pre-JS): <h1>Hello, SSR</h1>
console.log("identical per request:", first === second); // => Output: identical per request: true
