// Capstone functional core: a pure(ish) render function -- DOM out, given state and a
// filter string in (co-18 ui-as-function-of-state, co-21 list-rendering, co-27 discriminated
// union). It never reads or writes any state itself; the imperative shell in app.ts owns that.
import type { TaskListState } from "./types";

export interface RenderCallbacks {
  onToggle: (id: string) => void;
}

export function renderTaskList(
  root: HTMLElement,
  state: TaskListState,
  filter: string,
  callbacks: RenderCallbacks,
): void {
  root.innerHTML = "";

  switch (state.status) {
    case "loading": {
      const p = document.createElement("p");
      p.id = "task-list-status";
      p.setAttribute("role", "status");
      p.textContent = "Loading tasks...";
      root.append(p);
      return;
    }
    case "error": {
      const p = document.createElement("p");
      p.id = "task-list-status";
      p.setAttribute("role", "alert");
      p.textContent = state.message;
      root.append(p);
      return;
    }
    case "empty": {
      const p = document.createElement("p");
      p.id = "task-list-status";
      p.textContent = "No tasks yet.";
      root.append(p);
      return;
    }
    case "loaded": {
      const visible = state.tasks.filter((task) => task.title.toLowerCase().includes(filter.toLowerCase()));
      if (visible.length === 0) {
        const p = document.createElement("p");
        p.id = "task-list-status";
        p.textContent = "No tasks match your filter.";
        root.append(p);
        return;
      }
      const ul = document.createElement("ul");
      ul.setAttribute("aria-label", "Tasks");
      for (const task of visible) {
        const li = document.createElement("li");
        const label = document.createElement("label");
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.id = "task-" + task.id;
        checkbox.checked = task.done;
        checkbox.addEventListener("change", () => callbacks.onToggle(task.id));
        label.htmlFor = checkbox.id;
        label.append(checkbox, document.createTextNode(" " + task.title));
        li.append(label);
        ul.append(li);
      }
      root.append(ul);
      return;
    }
  }
}
