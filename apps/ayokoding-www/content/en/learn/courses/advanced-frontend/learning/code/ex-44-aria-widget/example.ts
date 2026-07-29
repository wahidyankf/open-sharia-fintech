// Example 44: An ARIA Tabs Widget with Roles and States. (co-23)
//
// A custom tabs widget needs explicit ARIA to expose what a native control gives for free: a
// tablist contains tabs; each tab controls a tabpanel; the selected tab carries aria-selected, and
// each tab points at its panel via aria-controls. These roles and states ARE the widget's
// accessibility contract.

// A tab + the panel it controls, with the ARIA attributes a real widget must set.
interface Tab {
  // => the ARIA wiring is what makes a div-based tab behave like a tab to assistive tech
  id: string; // => the tab's id (the panel's aria-labelledby points here)
  label: string; // => the visible tab label
  selected: boolean; // => drives aria-selected
  controls: string; // => aria-controls: the id of this tab's panel
}

// The tabs in the widget; exactly one is selected at a time.
const tabs: Tab[] = [
  // => co-23: roles (tablist/tab/tabpanel) + states (aria-selected) + relations (aria-controls)
  { id: "tab-1", label: "Overview", selected: true, controls: "panel-1" },
  { id: "tab-2", label: "Details", selected: false, controls: "panel-2" },
  { id: "tab-3", label: "Reviews", selected: false, controls: "panel-3" },
];

// renderAria prints the role/state/relation each node exposes -- the widget's a11y contract.
function renderAria(allTabs: Tab[]): string[] {
  // => the output is exactly what an accessibility tree would expose
  const lines: string[] = ['tablist (role="tablist")'];
  for (const t of allTabs) {
    // => each tab reports its role, selected state, and which panel it controls
    lines.push(`  tab "${t.label}" role="tab" aria-selected="${t.selected}" aria-controls="${t.controls}"`);
  }
  return lines; // => the full contract, one node per line
}

const tree = renderAria(tabs); // => the exposed accessibility tree

tree.forEach((line) => console.log(line)); // => Output: the tablist + 3 tab nodes with states
console.log(
  "selected tabs:",
  tabs.filter((t) => t.selected).map((t) => t.label),
); // => Output: selected tabs: [ 'Overview' ]
