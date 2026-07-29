// Example 47: An aria-live Region Announces Updates. (co-23)
//
// An aria-live region is how a screen reader announces a dynamic update without moving focus.
// Setting aria-live="polite" on a region and then changing its text causes the reader to announce
// the new text -- the mechanism behind "X results found", "item added to cart", and live scores.

// A live region: its polite/rude setting and its current text.
interface LiveRegion {
  // => the politeness setting controls WHEN the reader interrupts
  politeness: "polite" | "assertive" | "off"; // => aria-live value
  text: string; // => the announced content
}

// The reader's announcement queue (what a screen reader would speak).
const announced: string[] = []; // => stands in for the assistive-tech speech queue
// => an "assertive" region interrupts; a "polite" one waits for a pause

// update writes new text into a live region, triggering an announcement (unless it is "off").
function announce(region: LiveRegion, next: string): void {
  // => co-23: changing the text of an aria-live region is what triggers the announcement
  region.text = next; // => update the region's content
  if (region.politeness !== "off") announced.push(next); // => the reader speaks the new text
}

const statusRegion: LiveRegion = { politeness: "polite", text: "" }; // => aria-live="polite"
announce(statusRegion, "Loading results..."); // => first announcement
announce(statusRegion, "3 results found"); // => second announcement, same region

console.log("announcements:", announced); // => Output: announcements: [ 'Loading results...', '3 results found' ]
console.log("region text now:", statusRegion.text); // => Output: region text now: 3 results found
