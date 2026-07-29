// Kata 6 (before): a switch over the state union is MISSING a case for one variant. The unhandled
// variant falls through and returns a WRONG default (an empty string), a silent runtime bug.
// THE BUG: no "stale" case, and no exhaustiveness check, so the missing case is never surfaced.

type State =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "success"; data: number[] }
  | { status: "stale" }; // => this variant exists in the union...

function render(state: State): string {
  switch (state.status) {
    case "loading":
      return "Loading...";
    case "error":
      return `Error: ${state.message}`;
    case "success":
      return `OK: ${state.data.join(",")}`;
    // THE BUG: no case for "stale" -- it falls through and returns "" below
  }
  return ""; // => the silent wrong default for the unhandled "stale" state
}

console.log("render stale (BUG: empty):", JSON.stringify(render({ status: "stale" }))); // => "" -- wrong
