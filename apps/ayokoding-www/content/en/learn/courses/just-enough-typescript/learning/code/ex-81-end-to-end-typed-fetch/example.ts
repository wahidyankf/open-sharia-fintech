// Example 81: End-To-End Typed Fetch -- an async fetch, narrowed by a user-defined type guard.
type User = { id: number; name: string };

// => simulates a network response -- resolves to `unknown`, exactly like a real fetch().json()
async function fetchJson(raw: string): Promise<unknown> {
  return JSON.parse(raw); // => JSON.parse's return type is always unknown-worthy (any, narrowed here)
}

function isUser(value: unknown): value is User {
  // => the actual runtime shape check backing the `value is User` predicate
  return (
    typeof value === "object" &&
    value !== null &&
    typeof (value as User).id === "number" &&
    typeof (value as User).name === "string"
  );
}

async function loadUser(raw: string): Promise<string> {
  const parsed = await fetchJson(raw); // => parsed's type is unknown
  if (isUser(parsed)) {
    // => after this guard, parsed is narrowed to User
    return `user: ${parsed.name}`; // => .name is safe to read here
  }
  return "invalid payload"; // => rejected -- parsed did not match the User shape
}

async function run(): Promise<void> {
  console.log(await loadUser('{"id":1,"name":"Ada"}')); // => valid payload -- Output: user: Ada
  console.log(await loadUser('{"id":"oops"}')); // => invalid payload -- Output: invalid payload
}

run();
