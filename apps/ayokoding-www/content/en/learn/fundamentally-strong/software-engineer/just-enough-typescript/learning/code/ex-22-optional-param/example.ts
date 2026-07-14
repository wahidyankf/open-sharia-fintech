// Example 22: Optional Param -- title? may be omitted at every call-site.
function greet(name: string, title?: string): string {
  // => title's type is `string | undefined`; a call may omit it entirely
  return title === undefined ? `Hi, ${name}` : `Hi, ${title} ${name}`;
}

console.log(greet("Ada")); // => Output: Hi, Ada -- called with ONE argument, type-checks fine
console.log(greet("Ada", "Dr.")); // => Output: Hi, Dr. Ada
