// Capstone: state.ts -- a discriminated-union JobState, tagged by its own "status" field.
export type JobState =
  | { status: "queued"; id: number } // => waiting to start -- no result yet
  | { status: "running"; id: number } // => in progress -- still no result
  | { status: "success"; id: number; result: number } // => finished -- result is safe to read
  | { status: "failed"; id: number; reason: string }; // => finished badly -- reason is safe to read

export function describeJob(job: JobState): string {
  // => switch narrows job's type inside each case, exactly like Example 37/38
  switch (job.status) {
    case "queued":
      return `job ${job.id}: queued`;
    case "running":
      return `job ${job.id}: running`;
    case "success":
      return `job ${job.id}: succeeded with ${job.result}`; // => .result is safe here
    case "failed":
      return `job ${job.id}: failed (${job.reason})`; // => .reason is safe here
    default: {
      // => exhaustiveness check, exactly like Example 38 -- catches an unhandled variant
      const _exhaustive: never = job;
      return _exhaustive;
    }
  }
}

// => a user-defined type guard, exactly like Example 34/81 -- narrows JobState to its success variant
export function isSuccess(job: JobState): job is { status: "success"; id: number; result: number } {
  return job.status === "success";
}
