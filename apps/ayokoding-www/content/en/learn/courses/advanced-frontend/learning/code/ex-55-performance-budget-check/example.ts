// Example 55: A Bundle Size Budget Fails a CI Check. (co-27)
//
// A performance budget turns "keep the bundle small" into a CHECKABLE gate. The build measures the
// output; if it exceeds the budget, the check FAILS (non-zero exit) -- blocking the regression the
// way a failing test would. The budget is what makes size a first-class CI concern, not a wish.

// A budget rule: which artifact, its limit in KB, and the measured size.
interface Budget {
  // => the limit is the gate; the measured size is what the build produced
  artifact: string; // => what is being measured (e.g. the main bundle)
  limitKb: number; // => the threshold the CI check enforces
  measuredKb: number; // => the actual size this build produced
}

// checkBudget returns the exit code a CI step would use (0 pass, 1 fail).
function checkBudget(b: Budget): { exitCode: number; verdict: string } {
  // => co-27: exceeding the limit is a CI failure, not a warning
  if (b.measuredKb > b.limitKb) {
    // => over budget -> fail the build, exactly like a failing test
    return { exitCode: 1, verdict: `FAIL: ${b.artifact} ${b.measuredKb}KB > ${b.limitKb}KB limit` };
  }
  return { exitCode: 0, verdict: `pass: ${b.artifact} ${b.measuredKb}KB <= ${b.limitKb}KB` }; // => within budget
}

// A regression: someone added a heavy dependency, pushing the main bundle over budget.
const mainBundle: Budget = { artifact: "main.js", limitKb: 200, measuredKb: 240 }; // => 240 > 200
const result = checkBudget(mainBundle); // => the CI step's outcome

console.log("CI exit code:", result.exitCode); // => Output: CI exit code: 1
console.log("verdict:", result.verdict); // => Output: verdict: FAIL: main.js 240KB > 200KB limit
