// learning/code/ex-46-mechanical-refactor-across-files/checkout.ts
// ex-46-mechanical-refactor-across-files: checkout.ts -- co-15, co-17
// CALL SITE 2 of 3 -- reviewed and approved as its own, separate diff.
import { computeOrderTotal, type LineItem } from "./pricing"; // => co-15: import updated to the renamed export -- was `calculateTotal`

const TAX_RATE = 0.08; // => co-15: flat 8% tax, unrelated to the rename itself

const CHECKOUT_ITEMS: readonly LineItem[] = [
  { unitPrice: 40.0, quantity: 1 }, // => co-15: line item 1 -- a different sample cart than cart.ts
]; // => co-15: closes CHECKOUT_ITEMS

export function getCheckoutTotalWithTax(): number {
  // => co-15: call site 2 -- exercises the renamed function
  const subtotal = computeOrderTotal(CHECKOUT_ITEMS); // => co-15: was `calculateTotal(CHECKOUT_ITEMS)` before the rename
  return Math.round(subtotal * (1 + TAX_RATE) * 100) / 100; // => co-15: applies tax, rounds to 2 decimals -- unrelated logic, untouched by the rename
} // => co-15: closes getCheckoutTotalWithTax
