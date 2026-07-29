// Capstone types: a dashboard row, the paginated slice, and the discriminated-union load state.
// (co-33 discriminated-union-state; co-30 pagination cursor.)

export interface Row {
  // a single dashboard record the user searches and paginates over
  id: string; // stable key (co-20)
  label: string; // the searchable, visible text
}

// The async load state modeled as an exhaustive discriminated union (Example 66 / co-33).
export type LoadState =
  | { status: "loading" } // the SSR/streaming fallback state
  | { status: "error"; message: string } // payload unique to this branch
  | { status: "loaded"; rows: Row[] }; // payload unique to this branch

// A cursor-paginated slice of the row list (co-30): the visible page plus a next cursor.
export interface Page<T> {
  items: T[]; // the rows on THIS page
  nextCursor: number | null; // null => no more pages (the terminal cursor)
}

// A Core Web Vitals measurement (co-08): the three numbers Lighthouse would report.
export interface CoreWebVitals {
  lcp: number; // ms; good <= 2500
  inp: number; // ms; good <= 200
  cls: number; // score; good <= 0.1
}
