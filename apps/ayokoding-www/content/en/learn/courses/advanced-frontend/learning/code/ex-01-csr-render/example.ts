// Example 1: Client Side Rendering Boots an Empty Shell. (co-01)
//
// CSR: the server ships an EMPTY shell and the browser boots a JS bundle that fills it.
// This is the opposite of SSR (Example 2): before JS runs there is NOTHING to read, so the
// pre-JS DOM is blank -- a crawler or a no-JS user sees an empty page.

// The "server" ships this exact HTML body: a root div with no children at all.
const SHELL_HTML = `<div id="root"></div>`; // => co-01: the empty shell, pre-JS
// => SHELL_HTML contains zero text content; only the JS bundle can ever fill it

// A minimal DOM model -- enough to represent "a node that may or may not exist yet".
interface DomNode {
  // => a real DOM element has many fields; this model keeps only what proves the point
  tag: string; // => the element type (h1, p, ...)
  text: string; // => the rendered text content
}

// readDom reports a node's text, or "<empty>" when nothing has rendered yet.
function readDom(node: DomNode | null): string {
  // => the union `DomNode | null` is exactly "a node that may not exist yet"
  return node ? node.text : "<empty>"; // => null -> the blank shell
}

// A client renderer boots the bundle and produces the first real content.
function clientRender(): DomNode {
  // => stands in for React mounting <h1>Hello, CSR</h1> into #root
  return { tag: "h1", text: "Hello, CSR" }; // => content exists ONLY after this runs
}

// --- The CSR lifecycle, in order ---
const shell = null; // => before JS: the root has no DOM node -- the blank shell
console.log("pre-JS DOM:", readDom(shell)); // => Output: pre-JS DOM: <empty>
const mounted = clientRender(); // => JS boots; the bundle fills the shell
console.log("post-render DOM:", readDom(mounted)); // => Output: post-render DOM: Hello, CSR
