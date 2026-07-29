// Kata 4 (before): an image renders with NO reserved dimensions, so when it loads it shoves content
// down -- a layout shift. The CLS is poor.
// THE BUG: no width/height (or aspect-ratio) is set, so the image's box is 0 tall until it loads.

interface ImageBox {
  reservedHeight: number | null; // => null = no reserved box (the bug)
  intrinsicHeight: number; // => the real height once loaded
}

function layoutShiftOnLoad(img: ImageBox): number {
  // shift = how far content moved when the image arrived (co-11)
  const before = img.reservedHeight ?? 0; // => 0 if nothing reserved
  return Math.abs(before - img.intrinsicHeight); // => 0 only when reserved === intrinsic
}

const bugImage: ImageBox = { reservedHeight: null, intrinsicHeight: 300 }; // => no reserved box
const cls = layoutShiftOnLoad(bugImage); // => 300px of shift
const verdict = cls <= 0.1 ? "good" : "poor"; // => the CLS band (co-11)

console.log("layout shift (px, BUG: huge):", cls); // => 300
console.log("CLS verdict:", verdict); // => poor
