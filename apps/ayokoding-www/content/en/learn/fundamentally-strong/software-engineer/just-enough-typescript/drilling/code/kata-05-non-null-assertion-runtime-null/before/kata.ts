// Kata 5 (before): `!` asserts findUser's result is never null -- but for id 2, it genuinely is.
function findUser(id: number): { name: string } | null {
  return id === 1 ? { name: "Ada" } : null;
}

const user = findUser(2)!; // => compiles clean -- the assertion silences the type checker
console.log(user.name); // => runtime crash: user is actually null here
