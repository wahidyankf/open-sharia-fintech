// Kata 4 (after): the image has RESERVED dimensions, so it loads into a box that already existed --
// zero layout shift.
// THE FIX: set width/height (or aspect-ratio) so the box is reserved before the image arrives.

interface ImageBox {
  reservedHeight: number | null;
  intrinsicHeight: number;
}

function layoutShiftOnLoad(img: ImageBox): number {
  const before = img.reservedHeight ?? 0;
  return Math.abs(before - img.intrinsicHeight); // => 0 when reserved === intrinsic
}

const fixedImage: ImageBox = { reservedHeight: 300, intrinsicHeight: 300 }; // => reserved box
const cls = layoutShiftOnLoad(fixedImage); // => 0 shift
const verdict = cls <= 0.1 ? "good" : "poor";

console.log("layout shift (px, FIX: zero):", cls); // => 0
console.log("CLS verdict:", verdict); // => good
