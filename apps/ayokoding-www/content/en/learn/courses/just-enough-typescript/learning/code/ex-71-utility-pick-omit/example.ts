// Example 71: Utility Pick Omit -- Pick keeps a subset of keys; Omit removes a subset.
type User = { id: number; name: string; email: string };
type UserId = Pick<User, "id">; // => { id: number } -- ONLY id
type UserWithoutId = Omit<User, "id">; // => { name: string; email: string } -- everything BUT id

const idOnly: UserId = { id: 1 };
const rest: UserWithoutId = { name: "Ada", email: "ada@example.com" };
console.log(idOnly, rest); // => Output: { id: 1 } { name: 'Ada', email: 'ada@example.com' }
