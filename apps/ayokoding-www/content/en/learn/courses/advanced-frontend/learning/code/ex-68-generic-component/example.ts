// Example 68: A Typed Generic List Component. (co-33)
//
// A generic component `<T,>` carries its item type as a type parameter, so the SAME component works
// for `User[]`, `Product[]`, or any other shape -- with full type inference on the items and on the
// render callback. Generics let one component be reused without losing per-shape type safety.

// The props carry the item type parameter T through both `items` and the `render` callback.
interface ListProps<T> {
  // => T flows from items into render, so the callback is typed for the exact item shape
  items: T[]; // => the data, typed as T[]
  render: (item: T) => string; // => a callback that receives a T (not `any`)
}

// List is generic in T; calling it with User[] infers T = User everywhere.
function List<T>(props: ListProps<T>): string {
  // => co-33: one generic definition serves every item shape, fully typed
  return "<ul>" + props.items.map((item) => `<li>${props.render(item)}</li>`).join("") + "</ul>";
  // => `item` is typed T inside the map, so render's contract is enforced
}

// Two different item shapes, both rendered by the SAME generic component.
interface User {
  id: number; // => a User has an id
  name: string; // => a User has a name
}
interface Product {
  sku: string; // => a Product has a sku
  price: number; // => a Product has a price
}

const userList = List<User>({
  // => T inferred as User from the items array
  items: [
    { id: 1, name: "Ada" },
    { id: 2, name: "Alan" },
  ],
  render: (u) => `${u.id}: ${u.name}`, // => u is typed User, so u.name is safe
});
const productList = List<Product>({
  // => T inferred as Product -- the same component, a different shape
  items: [
    { sku: "A1", price: 10 },
    { sku: "B2", price: 25 },
  ],
  render: (p) => `${p.sku} ($${p.price})`, // => p is typed Product, so p.sku is safe
});

console.log(userList); // => Output: the rendered user list
console.log(productList); // => Output: the rendered product list
