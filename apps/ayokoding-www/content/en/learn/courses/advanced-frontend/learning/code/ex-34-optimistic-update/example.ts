// Example 34: An Optimistic Update Rolls Back on Failure. (co-15)
//
// An optimistic update shows the EXPECTED result immediately (before the server confirms), so the
// UI feels instant. If the mutation then FAILS, the update rolls back to the prior state. The
// rollback is what makes optimism safe -- the user is never left with a lie.

// A todo list with a function to attempt a server mutation.
interface State {
  // => the list is the canonical server state; optimisticState is the maybe-a-lie UI view
  todos: string[]; // => the confirmed list
}

let state: State = { todos: ["buy milk"] }; // => the initial confirmed state

// commitTodo attempts the mutation; it FAILS when shouldFail is true.
function commitTodo(title: string, shouldFail: boolean): { ok: boolean } {
  // => the real mutation is async and may reject; here it is a synchronous boolean
  if (shouldFail) return { ok: false }; // => simulate a server rejection
  state.todos = [...state.todos, title]; // => confirm the new todo
  return { ok: true }; // => success
}

// optimisticAdd shows the todo immediately, then rolls back if the commit fails.
function optimisticAdd(title: string, shouldFail: boolean): string[] {
  // => co-15: show the expected result first, keep a snapshot to restore on failure
  const snapshot = [...state.todos]; // => the prior confirmed state, for rollback
  const optimisticView = [...snapshot, title]; // => the optimistic UI the user sees NOW
  const result = commitTodo(title, shouldFail); // => attempt the real mutation
  if (!result.ok) state.todos = snapshot; // => ROLLBACK: restore the prior state on failure
  return result.ok ? state.todos : optimisticView; // => report the final confirmed/optimistic view
}

const ok = optimisticAdd("walk dog", false); // => succeeds -> confirmed
const failed = optimisticAdd("fly kite", true); // => fails -> rolled back, not in confirmed list

console.log("after success:", ok); // => Output: after success: [ 'buy milk', 'walk dog' ]
console.log("after failure (rolled back):", state.todos); // => Output: after failure (rolled back): [ 'buy milk', 'walk dog' ]
