// Capstone: main.ts -- runs a small batch of jobs end to end, printing every state transition.
import { describeJob, isSuccess, type JobState } from "./state"; // => value + type-only, combined
import { pluck } from "./util";

async function runJob(id: number, shouldFail: boolean): Promise<JobState> {
  // => simulates an async job -- prints its own loading transitions along the way
  console.log(describeJob({ status: "queued", id }));
  console.log(describeJob({ status: "running", id }));
  if (shouldFail) {
    return { status: "failed", id, reason: "simulated failure" };
  }
  return { status: "success", id, result: id * 10 };
}

async function main(): Promise<void> {
  const results: JobState[] = []; // => collects every job's FINAL state
  results.push(await runJob(1, false)); // => job 1 succeeds
  results.push(await runJob(2, true)); // => job 2 fails, deliberately
  results.push(await runJob(3, false)); // => job 3 succeeds

  for (const job of results) {
    console.log(describeJob(job)); // => one summary line per finished job
  }

  const ids = pluck(results, "id"); // => the generic utility, applied to JobState[]
  console.log("processed ids:", ids); // => Output: processed ids: [ 1, 2, 3 ]

  const succeeded = results.filter(isSuccess); // => narrowed to ONLY the success variant
  const totalResult = succeeded.reduce((sum, job) => sum + job.result, 0);
  // => .result is safe inside reduce -- succeeded's element type is the success variant
  console.log("total result:", totalResult); // => Output: total result: 40 (10 + 30)
}

main();
