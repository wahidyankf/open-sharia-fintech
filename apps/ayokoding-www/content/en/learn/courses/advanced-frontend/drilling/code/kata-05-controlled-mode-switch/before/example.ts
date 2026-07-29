// Kata 5 (before): an input that is sometimes controlled (value defined) and sometimes uncontrolled
// (value undefined) tries to SWITCH modes mid-life -- React warns and the input misbehaves.
// THE BUG: `value` is `string | undefined`, so an empty state yields value=undefined -> uncontrolled.

let warnings: string[] = []; // => the React dev warnings

function inputMode(value: string | undefined): "controlled" | "uncontrolled" {
  // => value present -> controlled; undefined -> uncontrolled (Example 30)
  return value === undefined ? "uncontrolled" : "controlled";
}

// Render 1: value = "hi" (controlled). Render 2: value = undefined (a cleared field set to undefined).
const modes = [inputMode("hi"), inputMode(undefined)]; // => controlled, then uncontrolled
if (modes[0] !== modes[1]) {
  // THE BUG: the input switched modes across renders -> React warns
  warnings.push("Warning: changing controlled to uncontrolled. Inputs should not switch modes.");
}

console.log("modes:", modes.join(" -> ")); // => controlled -> uncontrolled (a forbidden switch)
console.log("warnings:", warnings); // => the cannot-switch warning
