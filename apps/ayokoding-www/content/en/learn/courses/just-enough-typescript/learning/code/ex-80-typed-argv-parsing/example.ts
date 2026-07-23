// Example 80: Typed Argv Parsing -- process.argv is a plain string[], typed by @types/node.
const args: string[] = process.argv.slice(2); // => drops "node" and the script path, keeps the rest
const who: string = args[0] ?? "stranger"; // => ?? falls back when no argument was passed

console.log(`hello, ${who}`); // => Output depends on the argument passed at the CLI
