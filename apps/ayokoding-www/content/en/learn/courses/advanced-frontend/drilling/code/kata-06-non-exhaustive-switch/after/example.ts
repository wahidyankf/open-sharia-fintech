// Kata 6 (after): the switch handles EVERY variant, and a `never`-assertion makes a future missing
// case a COMPILE error instead of a silent runtime bug.
// THE FIX: add the "stale" case AND a never-assertion so exhaustiveness is enforced (Example 67).

type State =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "success"; data: number[] }
  | { status: "stale" };

function render(state: State): string {
  switch (state.status) {
    case "loading":
      return "Loading...";
    case "error":
      return `Error: ${state.message}`;
    case "success":
      return `OK: ${state.data.join(",")}`;
    case "stale":
      return "Stale -- refetching"; // => THE FIX: the missing case, now handled
    default: {
      // => if every case is handled, `state` is `never` here; an unhandled variant is a type error
      const exhaustive: never = state; // => exhaustiveness check
      return exhaustive;
    }
  }
}

console.log("render stale (FIX: handled):", render({ status: "stale" })); // => "Stale -- refetching"
