// Example 74: Utility ReturnType -- ReturnType<typeof fn> extracts a function's return type.
function makeUser(name: string): { id: number; name: string } {
  return { id: 1, name };
}

type MakeUserResult = ReturnType<typeof makeUser>; // => { id: number; name: string }

const u: MakeUserResult = { id: 2, name: "Grace" }; // => matches makeUser's return shape exactly
console.log(u); // => Output: { id: 2, name: 'Grace' }
