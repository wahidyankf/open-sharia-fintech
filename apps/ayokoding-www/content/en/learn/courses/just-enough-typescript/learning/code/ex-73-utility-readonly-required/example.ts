// Example 73: Utility Readonly Required -- Readonly blocks writes; Required removes optionality.
type Draft = { title?: string; body?: string };
type Published = Required<Draft>; // => { title: string; body: string } -- no more `?`

const post: Published = { title: "Hi", body: "World" }; // => both fields are now mandatory
console.log(post); // => Output: { title: 'Hi', body: 'World' }

type Config = { mode: string };
const frozen: Readonly<Config> = { mode: "dark" }; // => every field becomes readonly
console.log(frozen.mode); // => Output: dark
