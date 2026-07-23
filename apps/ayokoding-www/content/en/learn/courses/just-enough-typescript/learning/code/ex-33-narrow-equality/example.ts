// Example 33: Narrow Equality -- === against a literal narrows a literal union directly.
type Status = "idle" | "loading" | "done";

function report(status: Status): string {
  if (status === "loading") {
    // => this branch's status type narrows to exactly the literal "loading"
    return "please wait";
  }
  return `status: ${status}`; // => here, status is narrowed to "idle" | "done"
}

console.log(report("loading")); // => Output: please wait
console.log(report("done")); // => Output: status: done
