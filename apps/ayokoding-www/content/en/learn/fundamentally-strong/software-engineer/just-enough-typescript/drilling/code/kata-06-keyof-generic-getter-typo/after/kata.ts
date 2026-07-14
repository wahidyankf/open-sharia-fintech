// Kata 6 (after): "name" is a real key of user, so it satisfies keyof T.
function getValue<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { id: 1, name: "Ada" };
console.log(getValue(user, "name"));
