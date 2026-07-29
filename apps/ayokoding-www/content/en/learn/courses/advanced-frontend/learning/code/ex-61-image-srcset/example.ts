// Example 61: Responsive srcset and sizes Per Viewport. (co-31)
//
// `srcset` lists the SAME image at several widths with `w` descriptors; `sizes` declares the layout
// width at each breakpoint. The browser picks the smallest source that fills the layout width (and
// the screen's pixel ratio), so phones download a small file and desktops a large one.

// A candidate image source: its intrinsic width in pixels and its file URL.
interface Source {
  // => each source is the same image at a different resolution
  width: number; // => the intrinsic pixel width (the `w` descriptor)
  url: string; // => the file to fetch at that width
}

// chooseSource picks the narrowest source >= layoutWidth * dpr (the browser's selection rule).
function chooseSource(sources: Source[], layoutWidth: number, dpr: number): Source {
  // => co-31: the browser wants the smallest source that still fills layoutWidth at the device ratio
  const need = layoutWidth * dpr; // => effective pixels the image must cover
  // => pick the first source wide enough; if none, fall back to the widest available
  return (
    sources.find((s) => s.width >= need) ?? sources[sources.length - 1] // => smallest-sufficient source
  );
}

// The same hero image at three widths.
const sources: Source[] = [
  { width: 480, url: "hero-480w.jpg" }, // => for narrow viewports / phones
  { width: 1024, url: "hero-1024w.jpg" }, // => for tablets
  { width: 1920, url: "hero-1920w.jpg" }, // => for desktops
];

const phone = chooseSource(sources, 320, 2); // => need 640px -> 1024w source
const desktop = chooseSource(sources, 1200, 1); // => need 1200px -> 1920w source

console.log("phone picks:", phone.url); // => Output: phone picks: hero-1024w.jpg
console.log("desktop picks:", desktop.url); // => Output: desktop picks: hero-1920w.jpg
