// Example 8: const Literal Inference -- a const initializer infers a narrow literal type.
const c = "on"; // => c's inferred type is the literal "on", not the wide string
let d = "on"; // => d's inferred type widens to string, since let permits reassignment

function requireOn(mode: "on"): void {
  // => mode's parameter type only accepts the exact literal "on"
  console.log(mode); // => Output: on
}

requireOn(c); // => OK -- c's type IS the literal "on"
console.log(typeof d); // => Output: string -- widened, still a string at the type level
