// Example 39 (invalid): reading .data on the loading variant, which does not have it.
type State =
  | { status: "loading" } // => no extra data while loading
  | { status: "success"; data: string } // => data is only present once successful
  | { status: "error"; msg: string }; // => msg is only present on failure

function render(state: State): string {
  if (state.status === "loading") {
    return state.data; // => TYPE ERROR: Property 'data' does not exist on the loading variant
  }
  return "";
}

console.log(render({ status: "loading" }));
