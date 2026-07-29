// Kata 2 (after): the effect lists `filter` in its dependency array, so it re-runs (and logs the
// CURRENT filter) whenever the filter changes.
// THE FIX: deps = [filter] -> the effect re-runs when filter changes, closing over the fresh value.

let loggedFilters: string[] = []; // => what the effect printed across renders

function runEffect(setup: () => void, prevDeps: string[] | null, deps: string[]): string[] | null {
  const changed = prevDeps === null || deps.some((d, i) => !Object.is(d, prevDeps[i]));
  if (changed) setup();
  return deps;
}

function renderFixed(): void {
  let prevDeps: string[] | null = null;
  for (const filter of ["a", "ab", "abc"]) {
    // THE FIX: deps = [filter] -> the effect re-runs whenever filter changes
    prevDeps = runEffect(() => loggedFilters.push(filter), prevDeps, [filter]); // => current filter
  }
}

renderFixed();
console.log("effect logged (FIX: every change):", loggedFilters); // => ["a","ab","abc"] -- always fresh
