// Example 6: A Hydration Mismatch Warns and Recovers. (co-05)
//
// A hydration mismatch happens when the server and the client render DIFFERENT content for the
// same node. React warns (it cannot safely reconcile the difference) and then recovers by
// re-rendering the client tree. The classic cause: reading something client-only (e.g. the current
// time, or `window`) during render.

// The collected console warnings -- a real React build would log these to the browser console.
const warnings: string[] = []; // => stands in for the dev-console warning sink
// => pushing a string here models React's "Warning: Text content did not match" output

// The server renders a fixed value; the client reads a different (client-only) value.
const serverText = "count: 0"; // => the server's deterministic render
// => the server has no access to client-only state, so it renders a fixed value

// During hydration the client renders based on client-only state -> a different value.
function clientRender(): string {
  // => reading `Math.random()` / `Date.now()` / `window` here is the classic mismatch cause
  const clientOnlyState = 1; // => a value the server could NOT have known
  return `count: ${clientOnlyState}`; // => differs from serverText -> mismatch
}

// hydrateRoot compares server vs client text; a difference is reported then recovered.
function hydrateRoot(serverValue: string, clientValue: string): string {
  // => co-05: React compares the existing server HTML against the client's first render
  if (serverValue !== clientValue) {
    // => the mismatch is a bug to fix, not a crash: warn, then discard the server HTML
    warnings.push(`Warning: Text content did not match. Server: "${serverValue}" Client: "${clientValue}"`);
  }
  return clientValue; // => recovery: React re-renders from the client tree
}

const rendered = hydrateRoot(serverText, clientRender()); // => mismatch detected
// => the warning fires AND the client value wins -- both happen on the same hydration pass

console.log("warnings:", warnings); // => Output: the mismatch warning string
console.log("recovered DOM:", rendered); // => Output: recovered DOM: count: 1
