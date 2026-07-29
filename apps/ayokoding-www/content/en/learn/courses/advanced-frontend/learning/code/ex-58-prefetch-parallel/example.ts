// Example 58: Prefetching Parallelizes and Cuts Latency. (co-30)
//
// The fix for Example 57's waterfall: start the independent fetches in PARALLEL (Promise.all) so
// they overlap. The total latency is now the MAX of the steps, not the sum -- a big cut when one
// step is slow. Prefetching starts a fetch BEFORE it is needed so the result is ready on demand.

// Each step is a fake fetch that resolves after `latencyMs`.
function fetchAfter(latencyMs: number, value: string): Promise<string> {
  // => same fetch as Example 57; the change is HOW we call them
  return new Promise((resolve) => setTimeout(() => resolve(value), latencyMs)); // => resolve later
}

// parallel starts all three fetches at once (no dependency forces serialization here).
async function parallel(): Promise<{ total: number; steps: string[] }> {
  // => co-30: Promise.all overlaps the fetches -> total = MAX latency, not SUM
  const t0 = Date.now(); // => start the clock
  const [user, account, settings] = await Promise.all([
    // => all three begin in the same tick; they run concurrently
    fetchAfter(80, "user-1"),
    fetchAfter(120, "account-1"), // => no longer waits for `user`
    fetchAfter(100, "settings-1"), // => no longer waits for `account`
  ]);
  return { total: Date.now() - t0, steps: [user, account, settings] }; // => ~120ms total (the max)
}

(async () => {
  const result = await parallel(); // => the parallelized chain
  console.log("steps:", result.steps.join(" -> ")); // => Output: the three resolved values
  console.log("total latency (ms, ~= max 120):", result.total); // => Output: roughly 120ms (vs ~300 serial)
})();
