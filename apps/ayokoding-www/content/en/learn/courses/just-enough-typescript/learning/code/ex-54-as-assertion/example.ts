// Example 54: as Assertion -- `as T` tells the compiler "trust me", at real runtime risk.
type User = { id: number; name: string };

function parseUser(json: string): User {
  const parsed: unknown = JSON.parse(json); // => JSON.parse always returns unknown
  return parsed as User; // => `as User` compiles -- but nothing checks the shape at runtime
}

const user = parseUser('{"id":1,"name":"Ada"}');
console.log(user); // => Output: { id: 1, name: 'Ada' }
