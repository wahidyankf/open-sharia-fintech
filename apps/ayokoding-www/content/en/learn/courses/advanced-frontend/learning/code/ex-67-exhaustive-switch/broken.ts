// broken.ts: a NEW union member ("timeout") is added but NOT handled in the switch.
// The never-assertion now FAILS to compile, because "timeout" reaches the default branch and is
// not assignable to `never`. This is exactly the compile-time guarantee exhaustiveness gives you.
type State =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "success"; data: number[] }
  | { status: "stale" }
  | { status: "timeout" }; // => newly added -- but no case handles it below

function render(state: State): string {
  switch (state.status) {
    case "loading":
      return "Loading...";
    case "error":
      return `Error: ${state.message}`;
    case "success":
      return `OK: ${state.data.join(",")}`;
    case "stale":
      return "Stale -- refetching";
    default: {
      // => TYPE ERROR: "timeout" reaches here, so `state` is NOT `never`
      const exhaustive: never = state; // => error TS2322: ... is not assignable to type 'never'
      return exhaustive;
    }
  }
}

console.log(render({ status: "timeout" }));
