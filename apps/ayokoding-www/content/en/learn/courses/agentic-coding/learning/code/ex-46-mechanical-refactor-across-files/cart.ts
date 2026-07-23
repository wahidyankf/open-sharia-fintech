// learning/code/ex-46-mechanical-refactor-across-files/cart.ts
// ex-46-mechanical-refactor-across-files: cart.ts -- co-15, co-17
// CALL SITE 1 of 3 -- reviewed and approved as its own, separate diff.
import { computeOrderTotal, type LineItem } from "./pricing"; // => co-15: import updated to the renamed export -- was `calculateTotal`

const CART_ITEMS: readonly LineItem[] = [
  // => co-15: sample cart, unrelated to the rename itself
  { unitPrice: 12.5, quantity: 2 }, // => co-15: line item 1
  { unitPrice: 7.0, quantity: 3 }, // => co-15: line item 2
]; // => co-15: closes CART_ITEMS

export function getCartTotal(): number {
  // => co-15: call site 1 -- exercises the renamed function
  return computeOrderTotal(CART_ITEMS); // => co-15: was `calculateTotal(CART_ITEMS)` before the rename
} // => co-15: closes getCartTotal
