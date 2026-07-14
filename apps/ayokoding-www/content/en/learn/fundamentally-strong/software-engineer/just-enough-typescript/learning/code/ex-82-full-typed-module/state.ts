// Example 82: state.ts -- a discriminated-union TaskState, tagged by "status".
export type TaskState =
  | { status: "pending" } // => no extra data while pending
  | { status: "done"; result: number } // => result present only once done
  | { status: "failed"; reason: string }; // => reason present only on failure

export function describe(state: TaskState): string {
  switch (state.status) {
    case "pending":
      return "pending"; // => the pending variant carries no extra data to interpolate
    case "done":
      return `done: ${state.result}`; // => narrowed to the done variant -- .result is safe
    case "failed":
      return `failed: ${state.reason}`; // => narrowed to the failed variant -- .reason is safe
  }
}
