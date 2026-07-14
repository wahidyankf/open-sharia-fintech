// Example 21 (invalid): a void function body may not return an actual value.
function logLine(text: string): void {
  console.log(text);
  return text; // => TYPE ERROR: string is not assignable to type 'void'
}

logLine("hello");
