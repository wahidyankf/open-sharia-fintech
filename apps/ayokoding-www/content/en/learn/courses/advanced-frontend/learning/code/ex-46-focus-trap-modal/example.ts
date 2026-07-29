// Example 46: A Focus Trap Keeps Focus Inside a Dialog. (co-24)
//
// A modal dialog must trap focus: Tab and Shift+Tab cycle among the dialog's focusable elements
// without ever leaving the dialog. Focus cannot escape to the page behind, which is what makes a
// modal a modal for keyboard and screen-reader users.

// The dialog's focusable elements, in tab order.
interface Focusable {
  // => a focus trap cycles among exactly these elements
  id: string; // => identity
  kind: string; // => what kind of control (input, button, close)
}

const dialog: Focusable[] = [
  // => the trap boundary contains only these elements
  { id: "close-btn", kind: "button" },
  { id: "name-input", kind: "input" },
  { id: "ok-btn", kind: "button" },
];

let activeId = dialog[1].id; // => focus starts on the name input (a common default)
const trail: string[] = [activeId]; // => record where focus went after each Tab

// tab moves focus forward; wrapping at the last element back to the first (the trap).
function tab(): void {
  // => co-24: forward Tab wraps inside the dialog; it never reaches the page behind
  const i = dialog.findIndex((f) => f.id === activeId); // => current position
  const next = (i + 1) % dialog.length; // => wrap to 0 after the last element
  activeId = dialog[next].id; // => focus moves, still inside the dialog
  trail.push(activeId);
}

// shiftTab moves focus backward; wrapping at the first element to the last.
function shiftTab(): void {
  // => co-24: backward Tab also wraps inside the dialog
  const i = dialog.findIndex((f) => f.id === activeId); // => current position
  const next = (i - 1 + dialog.length) % dialog.length; // => wrap to last after the first
  activeId = dialog[next].id; // => focus moves, still inside the dialog
  trail.push(activeId);
}

tab(); // => name-input -> ok-btn
tab(); // => ok-btn -> close-btn (wraps)
tab(); // => close-btn -> name-input (wraps)
shiftTab(); // => name-input -> close-btn (wraps backward)

console.log("focus trail (all inside dialog):", trail); // => Output: the wrap-around trail
console.log("focus escaped the dialog:", !dialog.some((f) => f.id === activeId)); // => Output: focus escaped the dialog: false
