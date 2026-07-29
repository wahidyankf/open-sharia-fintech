// Example 57: A Serial Fetch Waterfall. (co-30)
//
// A request waterfall is when each fetch only starts AFTER the previous one finishes, because each
// depends on the last's result. The total latency is the SUM of every step -- the slowest possible
// shape. This example measures that sum so Example 58 can cut it.

// Each step is a fake fetch that resolves after `latencyMs` with a value.
function fetchAfter(latencyMs: number, value: string): Promise<string> {
  // => stands in for a network/API call; the latency is the point, not the payload
  return new Promise((resolve) => setTimeout(() => resolve(value), latencyMs)); // => resolve later
}

// A waterfall: fetch the user, THEN their account, THEN their settings -- each needs the prior id.
async function waterfall(): Promise<{ total: number; steps: string[] }> {
  // => co-30: each await blocks the next from even starting -> total = sum of all latencies
  const t0 = Date.now(); // => start the clock
  const user = await fetchAfter(80, "user-1"); // => step 1 (waits 80ms)
  const account = await fetchAfter(120, `account-for-${user}`); // => step 2 (waits 120ms, needs user)
  const settings = await fetchAfter(100, `settings-for-${account}`); // => step 3 (waits 100ms, needs account)
  return { total: Date.now() - t0, steps: [user, account, settings] }; // => ~300ms total (sum)
}

// Run via an async IIFE (tsx supports top-level await, but an IIFE is universally clear).
(async () => {
  const result = await waterfall(); // => the serial chain
  console.log("steps:", result.steps.join(" -> ")); // => Output: the three resolved values
  console.log("total latency (ms, ~= sum 300):", result.total); // => Output: roughly 300ms
})();
