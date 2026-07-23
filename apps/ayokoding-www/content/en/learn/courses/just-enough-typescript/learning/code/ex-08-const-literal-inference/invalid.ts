// Example 8 (invalid): a let-bound "on" has widened to string, so it fails the literal param.
let d = "on"; // => d's inferred type is the wide string, not the literal "on"

function requireOn(mode: "on"): void {
  console.log(mode);
}

requireOn(d); // => TYPE ERROR: string is not assignable to the literal type "on"
