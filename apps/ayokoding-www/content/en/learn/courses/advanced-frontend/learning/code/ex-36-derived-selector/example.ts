// Example 36: A Memoized Derived Selector Recomputes on Input Change Only. (co-19)
//
// A memoized selector derives a value from state and caches it, recomputing only when its INPUT
// slice changes. Components reading a selector that did not change do not re-render -- the whole
// point of memoized selectors in a global store.

let computeCalls = 0; // => counts real recomputations (proof the memo worked)
// => computeCalls staying low while reads repeat is the memoization paying off

// selectVisible derives the count of done items from the todos slice.
function selectVisibleCount(todos: { done: boolean }[]): number {
  // => the derive itself; memoized means this body runs only when todos changes
  computeCalls += 1; // => record a real recomputation
  return todos.filter((t) => t.done).length; // => the derived count
}

// memoize returns a selector that recomputes only when its single argument changes (by reference).
function memoize<I, O>(projector: (input: I) => O): (input: I) => O {
  // => co-19: cache keyed on the last input reference; same reference => same cached output
  let lastInput: I | undefined; // => the previous input reference
  let lastOutput: O | undefined; // => the previous result
  return (input: I) => {
    if (input !== lastInput) {
      // => reference changed -> recompute; same reference -> cache hit
      lastInput = input; // => store the new reference
      lastOutput = projector(input); // => recompute and cache
    }
    return lastOutput as O; // => the cached or freshly-computed result
  };
}

const select = memoize(selectVisibleCount); // => the memoized selector

const todosA = [{ done: true }, { done: false }]; // => reference A
select(todosA); // => compute (#1)
select(todosA); // => SAME reference -> cache hit (#1 still)
select(todosA); // => still same -> cache hit (#1 still)
const todosB = [{ done: true }, { done: true }]; // => a NEW reference (and new values)
select(todosB); // => new reference -> recompute (#2)

console.log("reads: 4, real computations:", computeCalls); // => Output: reads: 4, real computations: 2
console.log("visible count (todosB):", select(todosB)); // => Output: visible count (todosB): 2
