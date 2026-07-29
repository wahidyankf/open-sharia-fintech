// Kata 3 (after): the optimistic add keeps a SNAPSHOT and rolls back to it on failure.
// THE FIX: snapshot the prior state; restore it when the mutation fails.

let list: string[] = ["buy milk"]; // => the confirmed list

function addOptimisticWithRollback(label: string, fails: boolean): void {
  // THE FIX: snapshot the prior state so it can be restored on failure (Example 34)
  const snapshot = [...list]; // => the confirmed state before the optimistic add
  list = [...list, label]; // => optimistic: show immediately
  if (fails) {
    list = snapshot; // => ROLLBACK: restore the prior, confirmed state
  }
}

addOptimisticWithRollback("fly kite", true); // => fails -> rolled back
console.log("after a FAILED add (FIX: rolled back):", list); // => ["buy milk"] -- honest
