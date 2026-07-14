// Example 55: Non-Null Assertion -- x! tells the compiler "this is never null here".
function findUser(id: number): { name: string } | null {
  return id === 1 ? { name: "Ada" } : null; // => genuinely nullable return type
}

const user = findUser(1)!; // => the ! asserts the result is NOT null, at your own risk
console.log(user.name); // => .name is safe to read -- Output: Ada
