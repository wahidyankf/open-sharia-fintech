// Example 25: useCallback Returns a Stable Function Reference. (co-19)
//
// `useCallback` is the function-specialized form of useMemo: it returns the SAME function reference
// across renders when its deps are unchanged. This matters when the function is passed to a child
// that is memoized -- a new reference each render would defeat the child's memo and force a
// re-render.

// Counters for renders of the parent and the (memoized) child.
let parentRenders = 0; // => the parent re-renders whenever its state changes
let childRenders = 0; // => the child should NOT re-render if its props (the callback) are stable
// => if the callback were recreated each render, childRenders would track parentRenders

// useCallback returns a stable reference when deps are unchanged (Object.is per element).
function useCallback<T extends (...args: never[]) => unknown>(
  fn: T,
  deps: unknown[],
  prev: { deps: unknown[]; fn: T } | null,
): T {
  // => co-19: the function is the cached value; reuse it when deps are Object.is-equal
  const changed = prev === null || deps.some((d, i) => !Object.is(d, prev.deps[i]));
  return changed ? fn : prev!.fn; // => same reference on a cache hit
}

let stable: { deps: unknown[]; fn: () => void } | null = null;
const childCallbackRefs: (() => void)[] = []; // => the callback reference passed to the child each render

function parentRender(filterValue: string): void {
  // => the parent re-renders on every state change (here: filterValue)
  parentRenders += 1; // => count this parent render
  const handler = useCallback(() => console.log(filterValue), [filterValue], stable); // => deps=[filter]
  stable = { deps: [filterValue], fn: handler }; // => store for next comparison
  // => a memoized child only re-renders if the callback REFERENCE changed
  const last = childCallbackRefs[childCallbackRefs.length - 1];
  if (last !== handler) {
    // => new reference -> child must re-render (the only reason it ever would here)
    childRenders += 1;
    childCallbackRefs.push(handler);
  }
}

parentRender("a"); // => mount: new ref -> child renders
parentRender("a"); // => dep unchanged -> SAME ref -> child does NOT re-render
parentRender("a"); // => still unchanged -> child still skipped
parentRender("b"); // => dep changed -> new ref -> child renders again

console.log("parent renders:", parentRenders, "| child renders:", childRenders); // => Output: parent: 4 | child: 2
