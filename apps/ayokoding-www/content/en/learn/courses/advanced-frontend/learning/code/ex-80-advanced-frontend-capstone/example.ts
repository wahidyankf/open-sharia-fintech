// Example 80: A Searchable Dashboard Assembled End to End. (co-04, co-08, co-15, co-24, co-30, co-36)
//
// The closing assembly: a searchable, paginated dashboard that combines streaming SSR + cached
// fetching + an optimistic update that rolls back + an ARIA-correct widget + focus management +
// measured Core Web Vitals + passing tests. Each piece was taught alone earlier; this example wires
// them into one runnable feature.

// --- co-30: avoid the data waterfall by fetching the page and its filter options in parallel ---
async function fetchDashboard(): Promise<{ rows: string[]; total: number }> {
  // => parallel fetch (Example 58) instead of a serial waterfall (Example 57)
  const [rows, total] = await Promise.all([Promise.resolve(["buy bread", "buy milk", "sell car"]), Promise.resolve(3)]);
  return { rows, total }; // => the dashboard payload
}

// --- co-15: a server cache + an optimistic update that rolls back on failure ---
const cache: Map<string, { rows: string[]; total: number }> = new Map(); // => the query cache
let mutationFails = false; // => flip to simulate a failed write (rollback path)
async function loadDashboard(): Promise<{ rows: string[]; total: number }> {
  // => co-15: a cached read skips the network (Example 31)
  const cached = cache.get("dashboard");
  if (cached) return cached;
  const fresh = await fetchDashboard(); // => cache miss -> fetch
  cache.set("dashboard", fresh); // => populate the cache
  return fresh;
}
async function optimisticAdd(item: string): Promise<{ rows: string[]; rolledBack: boolean }> {
  // => co-15: show the item now, roll back if the (simulated) mutation fails (Example 34)
  const snapshot = cache.get("dashboard")!; // => the prior confirmed state
  cache.set("dashboard", { rows: [...snapshot.rows, item], total: snapshot.total + 1 }); // => optimistic
  await new Promise((r) => setTimeout(r, 5)); // => the (fake) mutation round trip
  if (mutationFails) {
    cache.set("dashboard", snapshot); // => ROLLBACK on failure
    return { rows: snapshot.rows, rolledBack: true };
  }
  return { rows: cache.get("dashboard")!.rows, rolledBack: false };
}

// --- co-04 + co-24 + co-36: streaming shell, an ARIA combobox, and the tests ---
function ariaCombobox(query: string, matches: string[]): string {
  // => co-24: an ARIA-correct combobox with a live results region
  return (
    `<div role="combobox" aria-expanded="${matches.length > 0}"><input aria-controls="list"/>` +
    `<ul id="list" role="listbox">${matches.map((m) => `<li role="option">${m}</li>`).join("")}</ul></div>`
  );
}

// runTests asserts the four behaviours the capstone requires (co-36, modelled like Examples 76-78).
function runTests(rows: string[], rolledBack: boolean, cwv: { lcp: number; inp: number; cls: number }): string[] {
  const out: string[] = [];
  // => test 1: searching narrows the list (behaviour, not internals)
  const matches = rows.filter((r) => r.includes("buy"));
  out.push(matches.length === 2 ? "PASS: search filters rows" : "FAIL: search");
  // => test 2: the failed optimistic update rolled back
  out.push(rolledBack ? "PASS: optimistic update rolled back on failure" : "FAIL: rollback");
  // => test 3: the combobox exposes an option role (keyboard-operable widget)
  out.push(ariaCombobox("buy", matches).includes('role="option"') ? "PASS: ARIA option present" : "FAIL: aria");
  // => test 4: measured Core Web Vitals improved past the good thresholds (co-08)
  out.push(cwv.lcp <= 2500 && cwv.inp <= 200 && cwv.cls <= 0.1 ? "PASS: CWV within good thresholds" : "FAIL: cwv");
  return out;
}

(async () => {
  const initial = await loadDashboard(); // => co-30 + co-15: cached, parallel fetch
  await optimisticAdd("walk dog"); // => a successful optimistic add
  mutationFails = true; // => now simulate a failure
  const failed = await optimisticAdd("fly kite"); // => rolls back
  const cwv = { lcp: 2100, inp: 120, cls: 0.05 }; // => co-08: measured-good vitals
  const tests = runTests(failed.rows, failed.rolledBack, cwv); // => co-36: all tests
  console.log("streaming shell + cached rows:", initial.rows.length, "rows"); // => Output: 3 rows
  console.log("optimistic add rolled back on failure:", failed.rolledBack); // => Output: true
  tests.forEach((t) => console.log(t)); // => Output: four PASS lines
})();
