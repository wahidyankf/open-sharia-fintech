// Capstone imperative shell: owns state, wires the DOM once, and re-renders on every
// change (co-18, co-20, co-22, co-23, co-24, co-26). renderTaskList (the functional core)
// never touches state directly -- only this file does, via closures.
import { renderTaskList } from "./render";
import type { Loader, Task, TaskListState } from "./types";

// co-24: a client-generated task id must never collide with an id the loader already
// supplied -- two DOM elements sharing an id breaks the label[for] accessible-name
// association. Deriving the next id from the loaded tasks' own ids keeps client- and
// loader-issued ids in the same never-colliding sequence.
function nextIdAfterLoad(tasks: Task[]): number {
  let maxId = 0;
  for (const task of tasks) {
    const parsed = Number(task.id);
    if (Number.isInteger(parsed) && parsed > maxId) maxId = parsed;
  }
  return maxId + 1;
}

export function mountApp(root: HTMLElement, loadTasks: Loader): void {
  root.innerHTML = "";

  let nextId = 1;
  let state: TaskListState = { status: "loading" };
  let filter = "";

  // -- Filter (controlled input, co-22) --
  const filterLabel = document.createElement("label");
  filterLabel.htmlFor = "filter-input";
  filterLabel.textContent = "Filter tasks";
  const filterInput = document.createElement("input");
  filterInput.id = "filter-input";
  filterInput.type = "text";

  // -- Add-task form (controlled + validated, co-22/co-23/co-24) --
  const form = document.createElement("form");
  form.setAttribute("novalidate", ""); // this component owns the full validate/block/show-error flow itself
  const titleLabel = document.createElement("label");
  titleLabel.htmlFor = "title-input";
  titleLabel.textContent = "New task";
  const titleInput = document.createElement("input");
  titleInput.id = "title-input";
  titleInput.type = "text";
  titleInput.required = true;
  titleInput.minLength = 3;
  const formError = document.createElement("p");
  formError.id = "form-error";
  formError.hidden = true;
  formError.setAttribute("role", "alert"); // co-25: announced immediately to assistive tech
  const submitButton = document.createElement("button"); // a REAL button (co-25/co-26): free keyboard operability + role
  submitButton.type = "submit";
  submitButton.textContent = "Add task";
  form.append(titleLabel, titleInput, formError, submitButton);

  const listContainer = document.createElement("div");

  root.append(filterLabel, filterInput, form, listContainer);

  function render(): void {
    renderTaskList(listContainer, state, filter, { onToggle });
  }

  function onToggle(id: string): void {
    if (state.status !== "loaded") return;
    state = {
      status: "loaded",
      tasks: state.tasks.map((task) => (task.id === id ? { ...task, done: !task.done } : task)),
    };
    render();
  }

  filterInput.addEventListener("input", () => {
    filter = filterInput.value;
    render();
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    // checkValidity() covers `required`; the minimum-length rule is checked explicitly
    // here too so this component's validation behavior does not depend on how completely
    // a given DOM implementation (jsdom, in tests, versus a real browser) implements the
    // `minlength` constraint -- both paths report the identical "too short" outcome.
    const tooShort = titleInput.value.trim().length < titleInput.minLength;
    if (!titleInput.checkValidity() || tooShort) {
      formError.hidden = false;
      formError.textContent = "Enter a task title of at least 3 characters";
      return;
    }
    formError.hidden = true;
    const newTask: Task = { id: String(nextId++), title: titleInput.value, done: false };
    state =
      state.status === "loaded"
        ? { status: "loaded", tasks: [...state.tasks, newTask] }
        : { status: "loaded", tasks: [newTask] };
    titleInput.value = "";
    render();
  });

  // co-27: render the loading branch synchronously, first -- then genuinely await the
  // loader before ever moving to error/empty/loaded, exactly the async shape a real app has.
  render();
  loadTasks().then(
    (tasks) => {
      // guard against a lost update: if a local add already happened while this load was
      // still pending, state has already moved past "loading" -- keep that local state and
      // drop the (now-stale) loader result instead of silently overwriting it
      if (state.status !== "loading") return;
      nextId = nextIdAfterLoad(tasks);
      state = tasks.length === 0 ? { status: "empty" } : { status: "loaded", tasks };
      render();
    },
    (error: unknown) => {
      if (state.status !== "loading") return;
      state = {
        status: "error",
        message: error instanceof Error ? error.message : "Failed to load tasks",
      };
      render();
    },
  );
}
