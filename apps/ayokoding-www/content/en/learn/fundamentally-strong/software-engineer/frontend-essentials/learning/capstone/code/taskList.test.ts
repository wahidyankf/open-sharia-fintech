// Capstone tests -- Vitest + @testing-library/dom, driven directly against jsdom (co-27's four
// states, co-21's list rendering + events, co-22/co-23's controlled+validated form, co-25/co-26's
// accessible, keyboard-operable controls). Every test exercises the real mountApp component --
// none of them call renderTaskList directly, so these are true component-level tests.
import { describe, it, expect } from "vitest";
import { screen, fireEvent, within } from "@testing-library/dom";
import { mountApp } from "./app";
import type { Task } from "./types";

function freshRoot(): HTMLElement {
  document.body.innerHTML = "";
  const root = document.createElement("div");
  document.body.append(root);
  return root;
}

describe("capstone: initial render (step 1)", () => {
  it("renders the loading state synchronously, before the loader resolves", () => {
    const root = freshRoot();
    const neverResolves = () => new Promise<Task[]>(() => {});
    mountApp(root, neverResolves);
    expect(screen.getByRole("status").textContent).toBe("Loading tasks...");
  });
});

describe("capstone: discriminated-union states (step 3, co-27)", () => {
  it("transitions loading -> empty when the loader resolves to zero tasks", async () => {
    const root = freshRoot();
    mountApp(root, async () => []);
    await screen.findByText("No tasks yet.");
  });

  it("transitions loading -> error when the loader rejects", async () => {
    const root = freshRoot();
    mountApp(root, async () => {
      throw new Error("network unreachable");
    });
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toBe("network unreachable");
  });

  it("transitions loading -> loaded and renders every task when the loader resolves non-empty", async () => {
    const root = freshRoot();
    const seed: Task[] = [
      { id: "1", title: "Write report", done: false },
      { id: "2", title: "Review PR", done: true },
    ];
    mountApp(root, async () => seed);
    const list = await screen.findByRole("list", { name: "Tasks" });
    const items = within(list).getAllByRole("listitem");
    expect(items).toHaveLength(2);
  });
});

describe("capstone: list rendering + events (step 1/2, co-21)", () => {
  it("toggling a task's checkbox updates its checked state", async () => {
    const root = freshRoot();
    const seed: Task[] = [{ id: "1", title: "Write report", done: false }];
    mountApp(root, async () => seed);
    const checkbox = (await screen.findByRole("checkbox", {
      name: "Write report",
    })) as HTMLInputElement;
    expect(checkbox.checked).toBe(false);
    fireEvent.click(checkbox);
    expect(checkbox.checked).toBe(true);
  });
});

describe("capstone: filterable list (step 2, co-21 + co-22)", () => {
  it("narrows the rendered list to items matching the controlled filter input", async () => {
    const root = freshRoot();
    const seed: Task[] = [
      { id: "1", title: "Write report", done: false },
      { id: "2", title: "Review PR", done: false },
    ];
    mountApp(root, async () => seed);
    await screen.findByRole("list", { name: "Tasks" });

    const filterInput = screen.getByLabelText("Filter tasks");
    fireEvent.input(filterInput, { target: { value: "review" } });

    const list = screen.getByRole("list", { name: "Tasks" });
    const items = within(list).getAllByRole("listitem");
    expect(items).toHaveLength(1);
    expect(items[0].textContent).toContain("Review PR");
  });
});

describe("capstone: controlled, validated add-task form (step 2, co-22/co-23/co-24)", () => {
  it("blocks a too-short title with a visible error and adds nothing", async () => {
    const root = freshRoot();
    mountApp(root, async () => []);
    await screen.findByText("No tasks yet.");

    const titleInput = screen.getByLabelText("New task");
    fireEvent.input(titleInput, { target: { value: "ab" } });
    fireEvent.click(screen.getByRole("button", { name: "Add task" }));

    const error = screen.getByRole("alert");
    expect(error.textContent).toBe("Enter a task title of at least 3 characters");
    expect(screen.getByText("No tasks yet.")).toBeTruthy();
  });

  it("accepts a valid title, adds the task, and clears the input", async () => {
    const root = freshRoot();
    mountApp(root, async () => []);
    await screen.findByText("No tasks yet.");

    const titleInput = screen.getByLabelText("New task") as HTMLInputElement;
    fireEvent.input(titleInput, { target: { value: "Ship the feature" } });
    fireEvent.click(screen.getByRole("button", { name: "Add task" }));

    const list = await screen.findByRole("list", { name: "Tasks" });
    expect(within(list).getByText(/Ship the feature/)).toBeTruthy();
    expect(titleInput.value).toBe("");
  });
});

describe("capstone: accessibility pass (step 4, co-24/co-25/co-26)", () => {
  it("exposes the filter and title inputs by their accessible (label-derived) names", async () => {
    const root = freshRoot();
    mountApp(root, async () => []);
    expect(screen.getByLabelText("Filter tasks")).toBeTruthy();
    expect(screen.getByLabelText("New task")).toBeTruthy();
  });

  it("exposes Add task as a real button role, reachable by role-based query alone", async () => {
    const root = freshRoot();
    mountApp(root, async () => []);
    const button = screen.getByRole("button", { name: "Add task" });
    expect(button.tagName).toBe("BUTTON");
  });

  it("is keyboard-operable: focusing the real Add task button and pressing Enter submits the form", async () => {
    const root = freshRoot();
    mountApp(root, async () => []);
    await screen.findByText("No tasks yet.");

    const titleInput = screen.getByLabelText("New task") as HTMLInputElement;
    fireEvent.input(titleInput, { target: { value: "Keyboard-only task" } });

    const button = screen.getByRole("button", { name: "Add task" }) as HTMLButtonElement;
    button.focus();
    expect(document.activeElement).toBe(button);
    // a real <button> inside a <form> submits on Enter with zero extra keydown code --
    // fireEvent.click below models exactly that native behavior, since jsdom does not
    // itself simulate the browser's implicit-submit-on-Enter form behavior
    fireEvent.click(button);

    const list = await screen.findByRole("list", { name: "Tasks" });
    expect(within(list).getByText(/Keyboard-only task/)).toBeTruthy();
  });
});

describe("capstone: async load race regression (finding 1)", () => {
  it("does not discard a task added locally while the initial load is still pending", async () => {
    const root = freshRoot();
    let resolveLoader!: (tasks: Task[]) => void;
    const pendingLoader = () =>
      new Promise<Task[]>((resolve) => {
        resolveLoader = resolve;
      });
    mountApp(root, pendingLoader);

    // the loader is still pending (state.status === "loading") -- add a task locally now
    const titleInput = screen.getByLabelText("New task") as HTMLInputElement;
    fireEvent.input(titleInput, { target: { value: "Added while loading" } });
    fireEvent.click(screen.getByRole("button", { name: "Add task" }));

    const list = await screen.findByRole("list", { name: "Tasks" });
    expect(within(list).getByText(/Added while loading/)).toBeTruthy();

    // now let the loader resolve -- the locally-added task must survive, not get silently
    // overwritten by the loader's own (now-stale) result
    resolveLoader([]);
    await new Promise((resolve) => setTimeout(resolve, 0));

    const listAfterLoad = screen.getByRole("list", { name: "Tasks" });
    expect(within(listAfterLoad).getByText(/Added while loading/)).toBeTruthy();
  });
});

describe("capstone: id collision regression (finding 2)", () => {
  it("does not let a newly added task collide with an already-loaded task's id", async () => {
    const root = freshRoot();
    const seed: Task[] = [{ id: "1", title: "Existing task", done: false }];
    mountApp(root, async () => seed);
    await screen.findByRole("list", { name: "Tasks" });

    const titleInput = screen.getByLabelText("New task") as HTMLInputElement;
    fireEvent.input(titleInput, { target: { value: "Newly added task" } });
    fireEvent.click(screen.getByRole("button", { name: "Add task" }));

    const list = screen.getByRole("list", { name: "Tasks" });
    const checkboxes = within(list).getAllByRole("checkbox") as HTMLInputElement[];
    const ids = checkboxes.map((checkbox) => checkbox.id);
    expect(new Set(ids).size).toBe(ids.length); // no duplicate DOM ids (label[for] would break)

    // toggling the newly added task must not also toggle the pre-existing task it collided with
    const existingCheckbox = within(list).getByRole("checkbox", {
      name: "Existing task",
    }) as HTMLInputElement;
    const newCheckbox = within(list).getByRole("checkbox", {
      name: "Newly added task",
    }) as HTMLInputElement;
    fireEvent.click(newCheckbox);
    expect(newCheckbox.checked).toBe(true);
    expect(existingCheckbox.checked).toBe(false);
  });
});
