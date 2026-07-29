// Example 14 showed render-blocking external CSS delays first paint; Example 15 inlines the
// CRITICAL (above-the-fold) CSS so first paint no longer waits on a separate network request for
// it. The non-critical CSS can load asynchronously afterwards. (co-12)

// Each milestone in the rendering timeline (ms from navigation start).
interface Step {
  // => reuse the same timeline shape as Example 14 to make the delta obvious
  event: string;
  time: number;
}

// WITH inlined critical CSS: the CSSOM is ready the instant the HTML is parsed -- no extra wait.
const inlinedCss: Step[] = [
  // => the critical CSS travels INSIDE the HTML, so there is no second network round trip
  { event: "HTML parsed (critical CSS inlined)", time: 50 }, // => DOM + CSSOM ready together
  { event: "first paint", time: 60 }, // => co-12: paint can happen immediately -- no CSSOM wait
];

// firstPaintAfter returns the time of the first paint milestone.
function firstPaintAfter(timeline: Step[]): number {
  // => locate the first-paint entry
  return timeline.find((s) => s.event.includes("first paint"))!.time; // => the measured first paint
}

const firstPaintInlined = firstPaintAfter(inlinedCss); // => 60 ms
const firstPaintExternal = 260; // => Example 14's blocking-external-CSS baseline

console.log("first paint with inlined critical CSS (ms):", firstPaintInlined); // => Output: 60
console.log("saved vs external CSS (ms):", firstPaintExternal - firstPaintInlined); // => Output: 200
