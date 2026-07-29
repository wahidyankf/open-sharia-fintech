// Capstone component: an imperative shell that renders a searchable, paginated dashboard into a real
// DOM container, with an ARIA combobox (arrow-key operable), a live result-count region, a cached +
// optimistically-added row list with rollback, and pagination. co-23/co-24 (ARIA + focus), co-15
// (cache + optimistic), co-19 (memoized derived selector), co-30 (pagination), co-37 (error path).
import { fireEvent } from "@testing-library/dom"; // re-exported for the keyboard helpers below
import { fetchPage, renderToStream, measureCwv, rate } from "./server";
import { optimisticAdd, prime, selectFiltered, resetForTests } from "./store";
import type { CoreWebVitals, LoadState, Page, Row } from "./types";

export { renderToStream, measureCwv, rate }; // expose the server/SSR/CWV helpers to the tests
export type { CoreWebVitals, Page, Row };

// addRow resolves ok/fail; the component uses it to drive the optimistic add + rollback path.
export type AddRow = (label: string) => Promise<{ ok: boolean }>;

export interface DashboardOptions {
  loadPage?: (cursor: number | null) => Promise<Page<Row>>; // defaults to the server fetchPage
  addRow: AddRow; // the mutation (ok=true succeeds, ok=false triggers rollback)
}

// mountDashboard builds the whole feature into `root` and wires every handler.
export function mountDashboard(root: HTMLElement, opts: DashboardOptions): void {
  resetForTests(); // => start each mount from a clean cache/memo
  root.innerHTML = ""; // => a fresh container

  const loadPage = opts.loadPage ?? fetchPage; // => the server fetch (co-30)

  // Component state (co-15/co-20): the loaded rows, the query, pagination cursor, active option.
  let loadedRows: Row[] = []; // => the confirmed rows (cache source of truth is primed from this)
  let query = ""; // => the controlled search value
  let nextCursor: number | null = null; // => the pagination cursor (null = no more pages)
  let activeIndex = -1; // => the active option for arrow-key navigation (co-24)

  // --- Build the DOM once (co-23/co-24 ARIA + co-26 form) ---
  const searchLabel = document.createElement("label");
  searchLabel.htmlFor = "dash-search";
  searchLabel.textContent = "Search rows";
  const search = document.createElement("input"); // => a combobox (co-23)
  search.id = "dash-search";
  search.type = "text";
  search.setAttribute("role", "combobox");
  search.setAttribute("aria-autocomplete", "list");
  search.setAttribute("aria-expanded", "false");
  search.setAttribute("aria-controls", "dash-listbox");
  search.setAttribute("aria-activedescendant", "");

  const count = document.createElement("p"); // => a live region (co-23, Example 47)
  count.id = "dash-count";
  count.setAttribute("role", "status");
  count.setAttribute("aria-live", "polite");

  const listbox = document.createElement("ul"); // => the options list (co-23)
  listbox.id = "dash-listbox";
  listbox.setAttribute("role", "listbox");
  listbox.setAttribute("aria-label", "Rows");

  // The add-row form (co-15 optimistic add, co-26 accessible form).
  const form = document.createElement("form");
  form.setAttribute("novalidate", "");
  const newLabel = document.createElement("label");
  newLabel.htmlFor = "dash-new";
  newLabel.textContent = "New row";
  const newInput = document.createElement("input");
  newInput.id = "dash-new";
  newInput.type = "text";
  newInput.required = true;
  const formError = document.createElement("p"); // => co-26 error, programmatically associated
  formError.id = "dash-new-error";
  formError.hidden = true;
  formError.setAttribute("role", "alert");
  newInput.setAttribute("aria-describedby", "dash-new-error");
  const addButton = document.createElement("button");
  addButton.type = "submit";
  addButton.textContent = "Add row";
  form.append(newLabel, newInput, formError, addButton);

  const moreButton = document.createElement("button"); // => co-30 pagination
  moreButton.type = "button";
  moreButton.textContent = "Load more";
  moreButton.disabled = true; // => disabled until a next cursor exists

  root.append(searchLabel, search, count, listbox, form, moreButton);

  // render rebuilds the option list + the live count from the current state. Passing { loading }
  // shows the streaming fallback; the default (no arg) is the loaded re-render path.
  function render(state?: LoadState): void {
    if (state?.status === "loading") {
      count.textContent = "Loading dashboard..."; // => the streaming fallback (co-04)
      listbox.innerHTML = "";
      return;
    }
    const filtered = selectFiltered(loadedRows, query); // => co-19 memoized derived view
    count.textContent = `${filtered.length} result${filtered.length === 1 ? "" : "s"}`;
    listbox.innerHTML = "";
    filtered.forEach((row, i) => {
      const li = document.createElement("li");
      li.id = `dash-opt-${row.id}`;
      li.setAttribute("role", "option");
      li.textContent = row.label;
      if (i === activeIndex) li.setAttribute("aria-selected", "true"); // => co-24 active option
      listbox.append(li);
    });
    search.setAttribute("aria-expanded", String(filtered.length > 0)); // => combobox expanded?
    search.setAttribute(
      "aria-activedescendant",
      activeIndex >= 0 && filtered[activeIndex] ? `dash-opt-${filtered[activeIndex].id}` : "",
    );
  }

  // --- Event wiring ---
  search.addEventListener("input", () => {
    query = search.value; // => controlled input (co-25)
    activeIndex = -1; // => reset the active option when the query changes
    render();
  });

  // Arrow-key navigation (co-24): ArrowDown/Up move the active option within the listbox.
  search.addEventListener("keydown", (event) => {
    const filtered = selectFiltered(loadedRows, query);
    if (filtered.length === 0) return;
    if (event.key === "ArrowDown") {
      event.preventDefault(); // => stop the page from scrolling
      activeIndex = (activeIndex + 1) % filtered.length; // => move forward, wrap
      render();
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      activeIndex = (activeIndex - 1 + filtered.length) % filtered.length; // => move back, wrap
      render();
    }
  });

  // Add-row submit: optimistic add with rollback on failure (co-15, Example 34).
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (newInput.value.trim().length === 0) {
      formError.hidden = false; // => co-26: required-field error, associated via aria-describedby
      formError.textContent = "Enter a row label";
      return;
    }
    formError.hidden = true;
    const label = newInput.value.trim();
    newInput.value = "";
    const result = await opts.addRow(label); // => the mutation (ok=true/false)
    const row: Row = { id: `local-${Date.now()}`, label };
    const r = optimisticAdd(row, !result.ok); // => optimistic; rolls back if !result.ok
    loadedRows = r.rows; // => adopt the confirmed (or rolled-back) row list
    prime(loadedRows); // => keep the cache in sync with the confirmed rows
    render();
  });

  // Load-more pagination (co-30): fetch the next page by cursor and append.
  moreButton.addEventListener("click", async () => {
    if (nextCursor === null) return;
    const page = await loadPage(nextCursor); // => fetch the next page
    loadedRows = [...loadedRows, ...page.items]; // => append the new page
    nextCursor = page.nextCursor; // => advance (or null out) the cursor
    moreButton.disabled = nextCursor === null; // => disable when there is no next page
    prime(loadedRows); // => resync the cache
    render();
  });

  // --- Initial load (co-04 streaming fallback first, then the resolved rows) ---
  render({ status: "loading" }); // => the SSR streaming fallback paints first
  loadPage(null).then((page) => {
    loadedRows = page.items; // => the first page
    nextCursor = page.nextCursor; // => the cursor for "Load more"
    moreButton.disabled = nextCursor === null;
    prime(loadedRows); // => populate the cache
    render(); // => the resolved rows replace the fallback
  });
}

// re-export fireEvent so the e2e-style test file can drive the keyboard through one import.
export { fireEvent };
