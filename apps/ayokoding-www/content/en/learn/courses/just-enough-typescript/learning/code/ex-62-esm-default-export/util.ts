// Example 62: util.ts -- a single default export.
export default function shout(text: string): string {
  return text.toUpperCase() + "!"; // => uppercases text and appends an exclamation mark
}
