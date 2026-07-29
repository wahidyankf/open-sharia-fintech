// Kata 3 (before): an optimistic add has NO rollback. When the mutation fails, the optimistically
// added row stays in the list -- a lie the user is never told about.
// THE BUG: no snapshot is kept, so a failed mutation cannot restore the prior state.

let list: string[] = ["buy milk"]; // => the confirmed list

function addOptimisticNoRollback(label: string, fails: boolean): void {
  // THE BUG: the prior state is discarded; nothing can be restored on failure
  list = [...list, label]; // => optimistic: show immediately
  if (fails) {
    // => the mutation failed, but there is no snapshot to roll back to -> the row stays (a lie)
    return; // => do nothing -- the lie persists
  }
}

addOptimisticNoRollback("fly kite", true); // => fails, but the row is left in the list
console.log("after a FAILED add (BUG: row left behind):", list); // => ["buy milk","fly kite"] -- a lie
