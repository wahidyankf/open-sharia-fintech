// Example 70: Utility Partial -- Partial<T> makes every field of T optional.
type User = { id: number; name: string };
type PartialUser = Partial<User>; // => { id?: number; name?: string }

const patch: PartialUser = { name: "Ada" }; // => id may be omitted -- Partial made it optional
console.log(patch); // => Output: { name: 'Ada' }
