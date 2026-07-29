// Example 63: Width and Height Reserve Space and Prevent CLS. (co-31, co-11)
//
// Without explicit width/height, an image has height 0 until it loads, then snaps to full size --
// shoving everything below it (a layout shift, co-11). Reserving width/height (or aspect-ratio)
// means the image drops into a box that already existed: zero shift.

// A placed image with optional reserved dimensions.
interface Place {
  // => reservedW/H are the box the image will fill; null means "unknown until load"
  reservedW: number | null; // => the reserved width (or null = unknown)
  reservedH: number | null; // => the reserved height (or null = unknown)
  intrinsicW: number; // => the image's real width once loaded
  intrinsicH: number; // => the image's real height once loaded
}

// shiftOnLoad returns how many pixels content moved when the image finally loaded.
function shiftOnLoad(p: Place): number {
  // => co-11: shift = |reserved height - intrinsic height|; reserved => 0 shift
  const beforeH = p.reservedH ?? 0; // => 0 if nothing was reserved
  return Math.abs(beforeH - p.intrinsicH); // => 0 when reserved === intrinsic
}

// WITHOUT reserved dimensions: a 300px image arrives into a 0px hole -> 300px shift.
const unreserved: Place = { reservedW: null, reservedH: null, intrinsicW: 500, intrinsicH: 300 };
// => co-31: always set width/height (or aspect-ratio) so the layout is stable before load

// WITH reserved dimensions matching the intrinsic ratio -> 0 shift.
const reserved: Place = { reservedW: 500, reservedH: 300, intrinsicW: 500, intrinsicH: 300 };

console.log("shift without reserved dims:", shiftOnLoad(unreserved)); // => Output: shift without reserved dims: 300
console.log("shift with reserved dims:", shiftOnLoad(reserved)); // => Output: shift with reserved dims: 0
