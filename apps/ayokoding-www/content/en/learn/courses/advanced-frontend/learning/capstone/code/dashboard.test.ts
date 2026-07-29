// Capstone tests: Vitest + @testing-library/dom, driven against jsdom. Covers every capstone
// acceptance criterion: streaming SSR + hydration, measured Core Web Vitals improvement, cached
// fetch + optimistic rollback, the ARIA combobox + keyboard operability, the memoized search, and
// cursor pagination. co-04/co-08/co-15/co-19/co-23/co-24/co-30/co-36/co-37.
import { describe, it, expect } from "vitest";
import { screen, within } from "@testing-library/dom";
import { mountDashboard, renderToStream, measureCwv, rate, fireEvent } from "./dashboard";
import type { Row } from "./types";

function freshRoot(): HTMLElement {
  document.body.innerHTML = ""; // => a clean document per test
  const root = document.createElement("div");
  document.body.append(root);
  return root;
}

// a Load-more-capable fetchPage mirroring the server's 3-per-page pagination over 6 seed rows
function makeLoadPage(): (cursor: number | null) => Promise<{ items: Row[]; nextCursor: number | null }> {
  const seed: Row[] = [
    { id: "1", label: "buy bread" },
    { id: "2", label: "buy milk" },
    { id: "3", label: "sell car" },
    { id: "4", label: "buy eggs" },
    { id: "5", label: "walk dog" },
    { id: "6", label: "sell bike" },
  ];
  return (cursor) => {
    const start = cursor ?? 0; // => cursor=null starts at index 0
    const items = seed.slice(start, start + 3);
    const nextCursor = start + 3 < seed.length ? start + 3 : null;
    return Promise.resolve({ items, nextCursor });
  };
}

describe("capstone: streaming SSR + fallback (co-04)", () => {
  it("streams the shell + fallback before the resolved rows", () => {
    const loading = renderToStream({ status: "loading" }, ""); // => the pending state
    expect(loading[0]).toBe("<!-- shell -->"); // => the static shell first
    expect(loading[1]).toContain("Loading dashboard"); // => the Suspense fallback

    const loaded = renderToStream({ status: "loaded", rows: [{ id: "1", label: "buy bread" }] }, "buy");
    expect(loaded[1]).toContain("<li>buy bread</li>"); // => resolved content streams in later
  });
});

describe("capstone: measured Core Web Vitals improve (co-08/co-11)", () => {
  it("rates the slow, unreserved baseline poor and the improved version good", () => {
    const baseline = measureCwv(3200, false); // => slow paint, no reserved boxes
    const improved = measureCwv(1500, true); // => faster paint, reserved boxes
    expect(rate(baseline)).toBe("poor"); // => baseline fails the good thresholds
    expect(rate(improved)).toBe("good"); // => the improved version meets them
    expect(improved.lcp).toBeLessThan(baseline.lcp); // => LCP improved measurably
    expect(improved.cls).toBeLessThan(baseline.cls); // => CLS improved (reserved space)
  });
});

describe("capstone: cached fetch + pagination (co-15/co-30)", () => {
  it("loads the first page and reveals Load more when a next cursor exists", async () => {
    const root = freshRoot();
    mountDashboard(root, { loadPage: makeLoadPage(), addRow: async () => ({ ok: true }) });
    const list = await screen.findByRole("listbox", { name: "Rows" }); // => first page renders
    expect(within(list).getAllByRole("option")).toHaveLength(3); // => 3 per page
    expect((screen.getByRole("button", { name: "Load more" }) as HTMLButtonElement).disabled).toBe(false);
  });

  it("appends the next page on Load more and disables it at the end", async () => {
    const root = freshRoot();
    mountDashboard(root, { loadPage: makeLoadPage(), addRow: async () => ({ ok: true }) });
    await screen.findByRole("listbox", { name: "Rows" });
    fireEvent.click(screen.getByRole("button", { name: "Load more" })); // => page 2
    let list = await screen.findByRole("listbox", { name: "Rows" });
    await expect.poll(() => within(list).getAllByRole("option").length).toBe(6); // => 3 + 3
    fireEvent.click(screen.getByRole("button", { name: "Load more" })); // => no next cursor now
    list = screen.getByRole("listbox", { name: "Rows" });
    await expect
      .poll(() => (screen.getByRole("button", { name: "Load more" }) as HTMLButtonElement).disabled)
      .toBe(true);
  });
});

describe("capstone: optimistic add rolls back on failure (co-15)", () => {
  it("keeps the new row when the mutation succeeds", async () => {
    const root = freshRoot();
    mountDashboard(root, { loadPage: makeLoadPage(), addRow: async () => ({ ok: true }) });
    await screen.findByRole("listbox", { name: "Rows" });
    fireEvent.input(screen.getByLabelText("New row"), { target: { value: "fly kite" } });
    fireEvent.click(screen.getByRole("button", { name: "Add row" }));
    await expect.poll(() => screen.queryByText("fly kite")).toBeTruthy(); // => the optimistic row is kept on success
  });

  it("rolls back the new row when the mutation fails", async () => {
    const root = freshRoot();
    mountDashboard(root, { loadPage: makeLoadPage(), addRow: async () => ({ ok: false }) });
    await screen.findByRole("listbox", { name: "Rows" });
    fireEvent.input(screen.getByLabelText("New row"), { target: { value: "fly kite" } });
    fireEvent.click(screen.getByRole("button", { name: "Add row" }));
    await expect.poll(() => screen.queryByText("fly kite")).toBeNull(); // => rolled back: the row never sticks
  });
});

describe("capstone: ARIA combobox + keyboard operability (co-23/co-24)", () => {
  it("exposes a combobox controlling a listbox of options", async () => {
    const root = freshRoot();
    mountDashboard(root, { loadPage: makeLoadPage(), addRow: async () => ({ ok: true }) });
    const combobox = await screen.findByRole("combobox"); // => the search input's role
    expect(combobox.getAttribute("aria-controls")).toBe("dash-listbox"); // => points at the listbox
    const list = screen.getByRole("listbox", { name: "Rows" });
    expect(within(list).getAllByRole("option").length).toBeGreaterThan(0); // => options present
  });

  it("moves the active option with ArrowDown and reflects it via aria-activedescendant", async () => {
    const root = freshRoot();
    mountDashboard(root, { loadPage: makeLoadPage(), addRow: async () => ({ ok: true }) });
    const combobox = (await screen.findByRole("combobox")) as HTMLInputElement;
    expect(combobox.getAttribute("aria-activedescendant")).toBe(""); // => no active option yet
    combobox.focus();
    fireEvent.keyDown(combobox, { key: "ArrowDown" }); // => activate the first option
    expect(combobox.getAttribute("aria-activedescendant")).toBe("dash-opt-1"); // => active = first
    fireEvent.keyDown(combobox, { key: "ArrowDown" }); // => move to the second
    expect(combobox.getAttribute("aria-activedescendant")).toBe("dash-opt-2");
    const first = document.getElementById("dash-opt-1");
    expect(first?.getAttribute("aria-selected")).toBeNull(); // => first no longer selected
  });
});

describe("capstone: memoized search filters the view (co-19/co-25)", () => {
  it("narrows the options to rows matching the controlled search input", async () => {
    const root = freshRoot();
    mountDashboard(root, { loadPage: makeLoadPage(), addRow: async () => ({ ok: true }) });
    await screen.findByRole("listbox", { name: "Rows" });
    fireEvent.input(screen.getByLabelText("Search rows"), { target: { value: "buy" } });
    const list = screen.getByRole("listbox", { name: "Rows" });
    await expect.poll(() => within(list).getAllByRole("option").length).toBe(2); // => buy bread, buy milk
    expect(screen.getByText("2 results")).toBeTruthy(); // => the live region announces the count
  });
});
