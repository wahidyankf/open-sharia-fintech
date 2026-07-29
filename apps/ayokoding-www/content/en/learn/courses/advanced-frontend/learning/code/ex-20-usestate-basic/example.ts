// Example 20: useState Re-renders on Change. (co-17)
//
// A component holds state in a useState cell; calling the setter changes the state and triggers a
// re-render, so the UI always reflects the current state. The UI is a FUNCTION of state: change
// the state, and the next render derives the new DOM from it.

// A render log records what the UI showed after each render.
const ui: string[] = []; // => each entry is one rendered frame
// => the log proves the UI only changes as a consequence of a state change + re-render

// makeCounter is one component instance with a single state cell.
function makeCounter(): { render: () => void; setCount: (n: number) => void } {
  // => the component's state lives in `count`, closed over by both render and setCount
  let count = 0; // => co-17: the useState cell's current value
  function render(): void {
    // => the UI is derived FROM state; it never holds a value state does not also hold
    ui.push(`count: ${count}`); // => this render's frame
  }
  function setCount(next: number): void {
    // => co-17: setting state schedules a re-render
    count = next; // => state changes first...
    render(); // => ...then the re-render reflects the new state
  }
  return { render, setCount };
}

const counter = makeCounter(); // => one independent component instance
counter.render(); // => initial render
counter.setCount(1); // => state change -> re-render
counter.setCount(2); // => another state change -> another re-render

console.log("rendered frames:", ui); // => Output: rendered frames: [ 'count: 0', 'count: 1', 'count: 2' ]
