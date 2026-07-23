// Example 21: void Return -- `: void` marks a function whose return value is not usable.
function logLine(text: string): void {
  // => void means "no meaningful return value" -- console.log itself also returns void
  console.log(text); // => Output: hello
}

logLine("hello");
