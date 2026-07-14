// Example 69: Async Discriminated State -- an async fetch producing loading->success/error states.
type FetchState =
  | { status: "loading" } // => no extra data while loading
  | { status: "success"; data: number } // => data present only once successful
  | { status: "error"; msg: string }; // => msg present only on failure

async function fetchData(shouldFail: boolean): Promise<FetchState> {
  // => simulates a network call -- resolves to either the success or error variant
  if (shouldFail) {
    return { status: "error", msg: "network down" }; // => shouldFail=true takes this branch
  }
  return { status: "success", data: 42 }; // => shouldFail=false takes this branch
}

function render(state: FetchState): string {
  if (state.status === "success") {
    return `data: ${state.data}`; // => narrowed to success here -- .data is safe
  }
  if (state.status === "error") {
    return `error: ${state.msg}`; // => narrowed to error here -- .msg is safe
  }
  return "loading"; // => the one remaining variant
}

async function run(): Promise<void> {
  console.log(render(await fetchData(false))); // => Output: data: 42
  console.log(render(await fetchData(true))); // => Output: error: network down
}

run(); // => prints both outcomes: a successful fetch, then a failing one
