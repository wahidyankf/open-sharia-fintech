// Example 49: An Accessible Error Summary Moves Focus. (co-26)
//
// When a form with errors is submitted, an accessible error SUMMARY collects every error and
// receives focus itself. Moving focus to the summary announces the errors in order and gives the
// keyboard user a single place to start fixing them -- rather than leaving them stranded wherever
// they were.

// A single error in the summary.
interface FieldError {
  // => each summary row points back at the field so the user can jump to it
  fieldId: string; // => the input the error belongs to
  message: string; // => the error text
}

// The simulated document.activeElement (what currently has focus).
let activeElementId: string | null = null; // => stands in for document.activeElement
// => moving focus to the summary is the a11y requirement, not just rendering it

// summarize builds the summary, gives it focus, and returns the focus target's id.
function summarize(errors: FieldError[]): string {
  // => co-26: the summary element receives focus so its errors are announced together
  activeElementId = "error-summary"; // => focus moves TO the summary on submit-with-errors
  return activeElementId; // => the summary is now the active element
}

const errors: FieldError[] = [
  // => two invalid fields, collected into one summary the reader announces in order
  { fieldId: "email", message: "Email is required" },
  { fieldId: "age", message: "Age must be 18 or older" },
];

const focused = summarize(errors); // => submit with errors -> focus the summary

console.log("focus moved to:", focused); // => Output: focus moved to: error-summary
console.log("active element is the summary:", activeElementId === "error-summary"); // => Output: active element is the summary: true
console.log("errors announced:", errors.map((e) => e.message).join("; ")); // => Output: errors announced: Email is required; Age must be 18 or older
