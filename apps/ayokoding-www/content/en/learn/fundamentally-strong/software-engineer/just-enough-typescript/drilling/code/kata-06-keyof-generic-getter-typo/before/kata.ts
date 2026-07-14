// Kata 6 (before): a typo'd key string doesn't satisfy keyof T -- tsc catches it at the call site.
function getValue<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { id: 1, name: "Ada" };
console.log(getValue(user, "naem"));
