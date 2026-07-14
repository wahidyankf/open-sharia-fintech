// Example 39: State Machine Union -- three variants tagged by their own "status" field.
type State =
  | { status: "loading" } // => no extra data while loading
  | { status: "success"; data: string } // => data is only present once successful
  | { status: "error"; msg: string }; // => msg is only present on failure

function render(state: State): string {
  if (state.status === "success") {
    return `data: ${state.data}`; // => narrowed to the success variant -- .data is safe
  }
  return `status: ${state.status}`; // => loading or error -- neither has .data
}

console.log(render({ status: "loading" })); // => Output: status: loading
console.log(render({ status: "success", data: "42" })); // => Output: data: 42
