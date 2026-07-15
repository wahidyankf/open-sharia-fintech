// Example 68: Discriminated Union Exhaustive -- adding a new state variant without
// updating the switch is a COMPILE error here, not a silent runtime bug.
type UiState = // => the same four-variant union Examples 65-67 model at runtime, now typed
  | { status: "loading" } // => Example 65's variant
  | { status: "error"; message: string } // => Example 66's variant; message is unique to it
  | { status: "empty" } // => Example 67's variant
  | { status: "loaded"; items: string[] } // => Example 71's variant; items is unique to it
  | { status: "stale" }; // => a NEW variant, added but deliberately left unhandled below

function render(state: UiState): string {
  // => same shape as Examples 65-67's render(), but typed and returning a string
  switch (state.status) {
    // => the tag being switched on is the SAME discriminant field, now type-checked
    case "loading":
      return "Loading..."; // => co-27: one branch per union member
    case "error":
      return state.message; // => narrowed: only this branch has .message
    case "empty":
      return "No results"; // => co-27: the dedicated empty-state branch, same as Example 67
    case "loaded":
      return state.items.join(", "); // => narrowed: only this branch has .items
    default: {
      // exhaustiveCheck: never accepts ONLY a value tsc has narrowed to the empty
      // set -- since "stale" reaches here unhandled, tsc reports a real type error
      const exhaustiveCheck: never = state; // => TYPE ERROR: "stale" is not assignable to `never`
      // => if a case for "stale" existed above, state here WOULD be narrowed to never
      return exhaustiveCheck; // => never actually runs; tsc rejects this file before it can
    } // => end of the default/exhaustiveness-check branch
  } // => end of the switch
} // => end of render; every reachable branch above returns a string
