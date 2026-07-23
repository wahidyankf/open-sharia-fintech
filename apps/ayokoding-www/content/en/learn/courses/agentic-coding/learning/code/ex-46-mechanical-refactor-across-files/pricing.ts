// learning/code/ex-46-mechanical-refactor-across-files/pricing.ts
// ex-46-mechanical-refactor-across-files: pricing.ts -- co-15, co-17
// This file DEFINES the renamed export. Every call site below imports the
// new name (computeOrderTotal), never the old one (calculateTotal).
export interface LineItem {
  // => co-15: shared type, untouched by the rename itself
  readonly unitPrice: number; // => co-15: price per unit
  readonly quantity: number; // => co-15: units in this line item
} // => co-15: closes LineItem

// BEFORE this refactor: `export function calculateTotal(...)`.        // => co-15: documents what the diff actually changed
// AFTER this refactor (below): renamed to `computeOrderTotal`, body    // => co-15: the rename itself -- logic is byte-for-byte identical
// left otherwise untouched.                                           // => co-15: continues the note above
export function computeOrderTotal(items: readonly LineItem[]): number {
  // => co-15: THE RENAME -- was calculateTotal, body unchanged
  return items.reduce((sum, item) => sum + item.unitPrice * item.quantity, 0); // => co-15: sums price*qty across every item, pure, no side effects
} // => co-15: closes computeOrderTotal
