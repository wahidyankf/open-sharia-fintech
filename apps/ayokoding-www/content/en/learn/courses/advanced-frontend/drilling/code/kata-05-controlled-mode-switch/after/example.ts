// Kata 5 (after): the input's value is ALWAYS a string (empty string when cleared, never undefined),
// so it stays controlled for its whole life.
// THE FIX: clear with "" (not undefined) so `value` is always defined -> always controlled.

let warnings: string[] = [];

function inputMode(value: string): "controlled" | "uncontrolled" {
  // => value is always a string now -> always controlled
  return "controlled";
}

// Render 1: value = "hi". Render 2: value = "" (cleared with an empty string, NOT undefined).
const modes = [inputMode("hi"), inputMode("")]; // => controlled, controlled (no switch)
if (modes[0] !== modes[1]) {
  warnings.push("Warning: changing controlled to uncontrolled.");
}

console.log("modes:", modes.join(" -> ")); // => controlled -> controlled (consistent)
console.log("warnings:", warnings); // => [] (no switch, no warning)
