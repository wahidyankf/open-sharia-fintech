// Example 75: Mapped Type -- { [K in keyof T]: ... } transforms EVERY property of T.
type User = { id: number; name: string };
type Flags<T> = { [K in keyof T]: boolean }; // => same keys as T, every value type becomes boolean

const changed: Flags<User> = { id: true, name: false }; // => id and name, both boolean now
console.log(changed); // => Output: { id: true, name: false }
