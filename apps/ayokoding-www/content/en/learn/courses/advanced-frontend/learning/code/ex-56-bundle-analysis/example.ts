// Example 56: Bundle Analysis Flags an Oversized Dependency. (co-27)
//
// When a bundle blows past its budget (Example 55), bundle analysis breaks the total down by
// dependency so you can see WHICH one is oversized. The analysis turns "the bundle is too big" into
// "moment.js is 70KB" -- an actionable diagnosis.

// Each dependency and the bytes it contributed to the bundle.
interface BundlePart {
  // => the per-dependency breakdown that makes an oversized bundle actionable
  dependency: string; // => the package name
  bytes: number; // => gzipped bytes it added
}

// The analyzed bundle: a list of dependency -> bytes.
const analysis: BundlePart[] = [
  // => one dependency dominates the total -- analysis identifies it by name
  { dependency: "react", bytes: 45000 },
  { dependency: "lodash", bytes: 80000 }, // => the oversized culprit (imported in full)
  { dependency: "app", bytes: 30000 },
];

// totalBytes sums every part; largestPart finds the single biggest contributor.
const totalBytes = analysis.reduce((sum, p) => sum + p.bytes, 0); // => the whole bundle
function largestPart(parts: BundlePart[]): BundlePart {
  // => co-27: the analysis ranks dependencies so the oversized one is obvious
  return parts.reduce((big, p) => (p.bytes > big.bytes ? p : big)); // => the biggest contributor
}

const culprit = largestPart(analysis); // => lodash, the oversized dependency
const pctOfTotal = Math.round((culprit.bytes / totalBytes) * 100); // => how much of the bundle it owns

console.log("bundle total (KB):", Math.round(totalBytes / 1024)); // => Output: bundle total (KB): 151
console.log("largest dependency:", culprit.dependency); // => Output: largest dependency: lodash
console.log("share of bundle:", pctOfTotal + "%"); // => Output: share of bundle: 53%
