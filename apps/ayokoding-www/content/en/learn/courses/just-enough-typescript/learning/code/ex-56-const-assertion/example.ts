// Example 56: const Assertion -- `as const` locks in literal types AND deep readonly-ness.
const cfg = { mode: "dark" } as const; // => cfg's type is { readonly mode: "dark" }, not { mode: string }

console.log(cfg.mode); // => Output: dark
// cfg.mode = "light";  // => would be a TYPE ERROR: mode is readonly under `as const`
