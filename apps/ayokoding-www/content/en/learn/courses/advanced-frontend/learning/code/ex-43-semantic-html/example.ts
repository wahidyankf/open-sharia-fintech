// Example 43: A Semantic Document Outline of Landmarks. (co-23)
//
// Semantic landmark elements (header, nav, main, article, section, footer) convey document
// structure that generic divs cannot. They map automatically to ARIA landmark roles, feeding the
// accessibility tree so screen-reader users can jump between regions.

// Each region carries its tag, its implicit ARIA role, and its heading level.
interface Landmark {
  // => the tag NAME decides the implicit role -- no extra ARIA attribute needed
  tag: "header" | "nav" | "main" | "article" | "footer"; // => the semantic element
  role: string; // => the implicit landmark role it maps to
  heading: string; // => the visible heading inside it
}

// The document outline: a sequence of semantic regions in reading order.
const outline: Landmark[] = [
  // => co-23: each landmark element maps to a role for free; a styled div would map to nothing
  { tag: "header", role: "banner", heading: "Site header" }, // => <header> -> banner
  { tag: "nav", role: "navigation", heading: "Main menu" }, // => <nav> -> navigation
  { tag: "main", role: "main", heading: "Page content" }, // => <main> -> main
  { tag: "article", role: "article", heading: "A blog post" }, // => <article> -> article
  { tag: "footer", role: "contentinfo", heading: "Site footer" }, // => <footer> -> contentinfo
];

// landmarkRoles lists every implicit role the outline exposes to assistive tech.
const landmarkRoles = outline.map((l) => `${l.tag} -> role="${l.role}"`); // => the free mapping
// => a screen reader can list these landmarks and let the user jump straight to `main`

console.log("document outline (tag -> implicit role):"); // => Output header
landmarkRoles.forEach((line) => console.log("  " + line)); // => one line per landmark
console.log("landmark count:", outline.length); // => Output: landmark count: 5
