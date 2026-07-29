// Kata 2 (before): an effect logs the current filter, but the filter is captured STALE because it
// is missing from the dependency array. The log always shows the value from the FIRST render.
// THE BUG: `[].length === 0` deps -> the effect never re-runs, so it closes over the initial filter.

let loggedFilters: string[] = []; // => what the effect printed across renders

// runEffect simulates a useEffect with a deps array; it re-runs only when deps changed (Example 23).
function runEffect(setup: () => void, prevDeps: string[] | null, deps: string[]): string[] | null {
  // Object.is-per-element comparison gates the re-run (co-18)
  const changed = prevDeps === null || deps.some((d, i) => !Object.is(d, prevDeps[i]));
  if (changed) setup();
  return deps; // => carry forward for the next comparison
}

function renderWithBug(): void {
  let prevDeps: string[] | null = null;
  for (const filter of ["a", "ab", "abc"]) {
    // THE BUG: deps = [] -> after the first render, prevDeps=[] matches [] -> effect never re-runs
    prevDeps = runEffect(() => loggedFilters.push(filter), prevDeps, []); // => empty deps (stale)
  }
}

renderWithBug();
console.log("effect logged (BUG: only first render):", loggedFilters); // => ["a"] -- stale forever
