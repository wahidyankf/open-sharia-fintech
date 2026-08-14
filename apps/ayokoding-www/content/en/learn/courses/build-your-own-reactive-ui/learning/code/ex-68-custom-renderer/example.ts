// custom-renderer: independently runnable, strict TypeScript demonstration.
// => Run with npx tsx example.ts; every assertion is part of the example.

function assert(condition: boolean, message: string): void {
  // => A failed runtime contract must stop the lesson, not merely log a warning.
  if (!condition) throw new Error(message);
  // => PASS: the invariant remains true and execution continues.
}

const queued = new Set<() => void>();
// => A set batches duplicate invalidations into one future flush.
function schedule(job: () => void): void {
  queued.add(job);
}
// => Scheduling records work without running it mid-update.
function flush(): void {
  for (const job of queued) job();
  queued.clear();
}
// => A deterministic flush gives a small topological/batching boundary.
const source = { count: 0 };
// => This plain object is the source state a Proxy or compiler could observe.
let work = 0;
// => Work counters reveal whether unrelated computations ran.
const renderCounter = (): void => {
  source.count;
  work += 1;
};
// => This direct update represents compiled, fine-grained DOM work.
schedule(renderCounter);
schedule(renderCounter);
// => Two synchronous invalidations still enqueue one job.
flush();
// => The batch publishes a stable result once, avoiding intermediate glitches.
assert(work === 1, "batched work should run once");
// => PASS: deduplication is the scheduling invariant used by advanced runtimes.
const staticParts = ["<p>", "</p>"] as const;
// => Tagged templates preserve immutable static sections around dynamic holes.
const rendered = staticParts[0] + String(source.count) + staticParts[1];
// => A renderer updates the dynamic hole without changing the static strings.
assert(rendered === "<p>0</p>", "template result should contain the dynamic value");
// => Host configs, fibers, and delegation all use the same scheduled-work principle.
console.log("PASS: custom-renderer");
// => Output: PASS: custom-renderer
