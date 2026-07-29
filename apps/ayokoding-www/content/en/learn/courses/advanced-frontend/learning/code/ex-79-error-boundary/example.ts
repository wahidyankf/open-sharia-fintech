// Example 79: An Error Boundary Catches a Render Error. (co-37)
//
// A render error in a child normally crashes the WHOLE app. An error boundary (a component using
// getDerivedStateFromError / componentDidCatch) catches a render error in its subtree and shows a
// fallback INSTEAD of unmounting everything. This example models that catch-and-fallback.

// A component can either render successfully or THROW during render.
function riskyChild(shouldThrow: boolean): string {
  // => a child whose render may throw (e.g. reading a property of undefined)
  if (shouldThrow) throw new Error("render exploded"); // => the render error
  return "<p>child ok</p>"; // => the normal output
}

// An error boundary wraps a render and catches a throw, falling back instead of crashing.
function errorBoundary(render: () => string): { output: string; caught: boolean } {
  // => co-37: try the child's render; on throw, show a fallback (do not propagate the crash)
  try {
    return { output: render(), caught: false }; // => normal render, no error
  } catch (e) {
    // => the boundary CATCHES the render error; the rest of the app keeps running
    return { output: `<p role="alert">Something went wrong: ${(e as Error).message}</p>`, caught: true };
  }
}

const ok = errorBoundary(() => riskyChild(false)); // => child renders fine
const caught = errorBoundary(() => riskyChild(true)); // => child throws -> fallback shown

console.log("no error:", ok.output, "| caught:", ok.caught); // => Output: no error: <p>child ok</p> | caught: false
console.log("on error:", caught.output); // => Output: on error: <p role="alert">Something went wrong: render exploded</p>
console.log("app still alive (error caught):", caught.caught); // => Output: app still alive (error caught): true
