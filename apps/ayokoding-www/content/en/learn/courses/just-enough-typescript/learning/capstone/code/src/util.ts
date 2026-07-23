// Capstone: util.ts -- a generic utility, reused by main.ts (exactly Example 76's shape).
export function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  // => K is constrained to items' own keys -- the return type is exactly T[K][]
  return items.map((item) => item[key]); // => extracts one field from every item
}
