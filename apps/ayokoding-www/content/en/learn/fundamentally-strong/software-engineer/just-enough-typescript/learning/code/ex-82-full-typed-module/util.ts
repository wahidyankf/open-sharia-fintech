// Example 82: util.ts -- a small generic utility, reused from main.ts.
export function firstOf<T>(items: T[]): T | undefined {
  // => T is inferred from whatever array is passed in -- no annotation needed at the call site
  return items[0]; // => the generic T flows through untouched
}
