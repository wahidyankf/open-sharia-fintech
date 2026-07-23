// Example 82: Full Typed Module -- state.ts + util.ts + an async flow, wired via ESM imports.
import { describe, type TaskState } from "./state"; // => a value import PLUS an inline type-only one
import { firstOf } from "./util"; // => a plain value import -- firstOf is used at runtime, not just for its type

async function runTask(shouldFail: boolean): Promise<TaskState> {
  // => simulates async work -- resolves to one of TaskState's three variants
  if (shouldFail) {
    return { status: "failed", reason: "disk full" };
  }
  return { status: "done", result: 42 };
}

async function main(): Promise<void> {
  const state = await runTask(false); // => state's type is TaskState
  console.log(describe(state)); // => Output: done: 42

  const failedState = await runTask(true); // => same call, different branch -- shouldFail=true now
  console.log(describe(failedState)); // => Output: failed: disk full

  const first = firstOf([10, 20, 30]); // => T is inferred as number
  console.log(first); // => Output: 10
}

main(); // => kicks off the async flow -- both TaskState outcomes plus the generic utility all run in order
