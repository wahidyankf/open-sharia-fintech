// Example 73 (invalid, Readonly): writing to a Readonly<T> field fails to compile.
type Config = { mode: string };
const frozen: Readonly<Config> = { mode: "dark" };

frozen.mode = "light"; // => TYPE ERROR: 'mode' is a read-only property
console.log(frozen.mode);
