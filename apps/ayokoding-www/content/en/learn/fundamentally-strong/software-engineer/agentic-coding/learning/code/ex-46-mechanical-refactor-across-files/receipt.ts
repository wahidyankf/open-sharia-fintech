// learning/code/ex-46-mechanical-refactor-across-files/receipt.ts
// ex-46-mechanical-refactor-across-files: receipt.ts -- co-15, co-17
// CALL SITE 3 of 3 -- reviewed and approved as its own, separate diff.
// Also this example's ENTRY POINT: running this file exercises all three
// call sites (cart.ts, checkout.ts, and the gift-wrap line below) in one run.
import { computeOrderTotal, type LineItem } from "./pricing"; // => co-15: import updated to the renamed export -- was `calculateTotal`
import { getCartTotal } from "./cart"; // => co-15: pulls in call site 1's result
import { getCheckoutTotalWithTax } from "./checkout"; // => co-15: pulls in call site 2's result

const GIFT_WRAP_ITEMS: readonly LineItem[] = [
  { unitPrice: 3.5, quantity: 1 }, // => co-15: a third, independent line item
]; // => co-15: closes GIFT_WRAP_ITEMS

function printReceipt(): void {
  // => co-15: call site 3 -- exercises the renamed function directly
  const cartTotal = getCartTotal(); // => co-15: from cart.ts (call site 1)
  const checkoutTotal = getCheckoutTotalWithTax(); // => co-15: from checkout.ts (call site 2)
  const giftWrapTotal = computeOrderTotal(GIFT_WRAP_ITEMS); // => co-15: was `calculateTotal(GIFT_WRAP_ITEMS)` before the rename -- call site 3
  console.log(`cart total:            ${cartTotal.toFixed(2)}`); // => co-15: prints call site 1's result
  console.log(`checkout total w/ tax: ${checkoutTotal.toFixed(2)}`); // => co-15: prints call site 2's result
  console.log(`gift wrap total:       ${giftWrapTotal.toFixed(2)}`); // => co-15: prints call site 3's result
  const allPositive = cartTotal > 0 && checkoutTotal > 0 && giftWrapTotal > 0; // => co-15: sanity check -- refactor must not have broken any call site
  console.log(`all three call sites returned a positive total: ${allPositive}`); // => co-15: reached only if every call above ran without throwing
} // => co-15: closes printReceipt

printReceipt(); // => co-15: executes this file's entry point
