// Example 73 (invalid, Required): omitting a field Required<T> now demands.
type Draft = { title?: string; body?: string };
type Published = Required<Draft>;

const post: Published = { title: "Hi" }; // => TYPE ERROR: 'body' is required now
console.log(post);
