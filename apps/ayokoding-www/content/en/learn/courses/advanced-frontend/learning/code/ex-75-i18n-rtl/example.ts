// Example 75: An RTL-Aware Mirrored Layout. (co-35)
//
// Setting `dir="rtl"` (right-to-left, for Arabic/Hebrew) mirrors the inline axis: what was "left"
// becomes "right". Logical properties (margin-inline-start, inset-inline-start) flow with the
// direction, so the SAME CSS works in both LTR and RTL -- only the dir attribute changes.

// A layout direction and its effect on the inline (horizontal) axis.
type Dir = "ltr" | "rtl"; // => the document/wrapper direction

// resolveLogical maps a logical inline-start to a physical side, depending on direction.
function resolveLogical(property: "margin-inline-start", dir: Dir): string {
  // => co-35: logical properties flip physical side with dir; one rule serves both directions
  if (property === "margin-inline-start") {
    return dir === "ltr" ? "margin-left" : "margin-right"; // => start = left in LTR, right in RTL
  }
  return property; // => (only one logical property modeled here)
}

// renderLayout builds the wrapper and shows which physical side the logical start resolved to.
function renderLayout(dir: Dir): { html: string; startSide: string } {
  // => co-35: setting dir alone mirrors the layout; logical CSS adapts automatically
  const html = `<div dir="${dir}">...</div>`; // => the dir attribute carries the whole mirroring
  return { html, startSide: resolveLogical("margin-inline-start", dir) }; // => the resolved physical side
}

const ltr = renderLayout("ltr"); // => English/standard: start = left
const rtl = renderLayout("rtl"); // => Arabic/Hebrew: start = right (mirrored)

console.log("LTR start side:", ltr.startSide); // => Output: LTR start side: margin-left
console.log("RTL start side:", rtl.startSide); // => Output: RTL start side: margin-right
console.log("RTL wrapper:", rtl.html); // => Output: RTL wrapper: <div dir="rtl">...</div>
