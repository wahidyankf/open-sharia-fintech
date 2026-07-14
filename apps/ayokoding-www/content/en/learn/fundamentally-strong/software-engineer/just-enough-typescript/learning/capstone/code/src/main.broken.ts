// Capstone (broken): reads .result on the raw, un-narrowed union -- not every variant has it.
import { describeJob, type JobState } from "./state";

async function runJob(id: number, shouldFail: boolean): Promise<JobState> {
  console.log(describeJob({ status: "queued", id }));
  console.log(describeJob({ status: "running", id }));
  if (shouldFail) {
    return { status: "failed", id, reason: "simulated failure" };
  }
  return { status: "success", id, result: id * 10 };
}

async function main(): Promise<void> {
  const results: JobState[] = [];
  results.push(await runJob(1, false));

  // => TYPE ERROR: 'result' does not exist on every JobState variant -- only "success" has it
  const total = results.reduce((sum, job) => sum + job.result, 0);
  console.log("total result:", total);
}

main();
