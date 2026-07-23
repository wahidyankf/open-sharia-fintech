// Example 76: Generic Constrained Getter -- T[K] returns the EXACT type of that one property.
function get<T, K extends keyof T>(obj: T, key: K): T[K] {
  // => K is constrained to obj's own keys -- the return type is precisely T[K]
  return obj[key];
}

const user = { id: 1, name: "Ada" };
const userName = get(user, "name"); // => userName's type is inferred as string, from T["name"]
console.log(userName); // => Output: Ada
