// Full-stack capstone: app.ts -- the imperative shell (topic 14): owns state, wires the DOM
// once, and re-renders on every change. render.ts (the functional core) never touches state
// directly -- only this file does, via closures. This is the ONE file that wires api.ts's
// typed HTTP client to the DOM: every create/update goes through the real backend (topic 11)
// over real HTTP (topic 12), never a local-only in-memory mutation.
import { renderTaskList } from "./render.js";
import type { Api } from "./api.js";
import { ApiError } from "./api.js";
import type { Task, TaskListState, TaskStatus } from "./types.js";

export function mountApp(root: HTMLElement, api: Api): void {
  root.innerHTML = "";

  let state: TaskListState = { status: "loading" };
  let editingId: number | null = null; // null => the form is in CREATE mode

  // -- Create/update form --
  const form = document.createElement("form");
  form.setAttribute("novalidate", ""); // this component owns its own validate/block/show-error flow

  const titleLabel = document.createElement("label");
  titleLabel.htmlFor = "title-input";
  titleLabel.textContent = "Title";
  const titleInput = document.createElement("input");
  titleInput.id = "title-input";
  titleInput.type = "text";
  titleInput.required = true;

  const descriptionLabel = document.createElement("label");
  descriptionLabel.htmlFor = "description-input";
  descriptionLabel.textContent = "Description";
  const descriptionInput = document.createElement("textarea");
  descriptionInput.id = "description-input";

  const statusLabel = document.createElement("label");
  statusLabel.htmlFor = "status-select";
  statusLabel.textContent = "Status";
  const statusSelect = document.createElement("select");
  statusSelect.id = "status-select";
  for (const value of ["todo", "in_progress", "done"] as const) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    statusSelect.append(option);
  }
  statusLabel.hidden = true; // only shown once an existing task is being edited
  statusSelect.hidden = true;

  const formError = document.createElement("p");
  formError.id = "form-error";
  formError.hidden = true;
  formError.setAttribute("role", "alert"); // announced immediately to assistive tech

  const submitButton = document.createElement("button");
  submitButton.type = "submit";
  submitButton.textContent = "Add task";

  const cancelButton = document.createElement("button");
  cancelButton.type = "button";
  cancelButton.textContent = "Cancel edit";
  cancelButton.hidden = true;

  form.append(
    titleLabel,
    titleInput,
    descriptionLabel,
    descriptionInput,
    statusLabel,
    statusSelect,
    formError,
    submitButton,
    cancelButton,
  );

  const listContainer = document.createElement("div");

  root.append(form, listContainer);

  function render(): void {
    renderTaskList(listContainer, state, { onEdit });
  }

  function resetFormToCreateMode(): void {
    editingId = null;
    titleInput.value = "";
    descriptionInput.value = "";
    statusSelect.value = "todo";
    statusLabel.hidden = true;
    statusSelect.hidden = true;
    submitButton.textContent = "Add task";
    cancelButton.hidden = true;
    formError.hidden = true;
  }

  function onEdit(task: Task): void {
    editingId = task.id;
    titleInput.value = task.title;
    descriptionInput.value = task.description;
    statusSelect.value = task.status;
    statusLabel.hidden = false;
    statusSelect.hidden = false;
    submitButton.textContent = "Update task";
    cancelButton.hidden = false;
    formError.hidden = true;
    titleInput.focus();
  }

  cancelButton.addEventListener("click", () => {
    resetFormToCreateMode();
  });

  async function refetch(): Promise<void> {
    try {
      const tasks = await api.fetchTasks();
      state = tasks.length === 0 ? { status: "empty" } : { status: "loaded", tasks };
    } catch (error: unknown) {
      state = { status: "error", message: errorMessage(error) };
    }
    render();
  }

  function errorMessage(error: unknown): string {
    if (error instanceof ApiError) return error.message;
    if (error instanceof Error) return error.message;
    return "Failed to load tasks";
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const title = titleInput.value.trim();
    if (!title) {
      formError.hidden = false;
      formError.textContent = "Enter a task title";
      return;
    }
    formError.hidden = true;

    const submit =
      editingId === null
        ? api.createTask({ title, description: descriptionInput.value })
        : api.updateTask(editingId, {
            title,
            description: descriptionInput.value,
            status: statusSelect.value as TaskStatus,
          });

    submit.then(
      () => {
        // Step 3: a UI action persists to the DB, and the list reflects it -- via a genuine
        // REFETCH (a fresh GET /tasks), never an optimistic local-only splice.
        resetFormToCreateMode();
        void refetch();
      },
      (error: unknown) => {
        formError.hidden = false;
        formError.textContent = errorMessage(error);
      },
    );
  });

  // render the loading branch synchronously, first -- then genuinely await the fetch before
  // ever moving to error/empty/loaded, exactly the async shape a real app has
  render();
  void refetch();
}
