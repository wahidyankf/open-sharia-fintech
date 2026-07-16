// Full-stack capstone: render.ts -- the functional core (topic 14), reused pattern from Frontend
// Essentials' own capstone: a pure `renderTaskList(root, state, callbacks)` function that never
// reads or writes any state itself, only renders whatever `state` it's handed. Loading, error,
// and empty are each a real, independently reachable branch of the TaskListState union -- never
// simulated, never CSS-hidden placeholders.
import type { TaskListState, Task } from "./types";

export interface RenderCallbacks {
  onEdit: (task: Task) => void;
}

export function renderTaskList(root: HTMLElement, state: TaskListState, callbacks: RenderCallbacks): void {
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
      const ul = document.createElement("ul");
      ul.setAttribute("aria-label", "Tasks");
      for (const task of state.tasks) {
        const li = document.createElement("li");
        const summary = document.createElement("span");
        summary.textContent = `${task.title} [${task.status}]`;
        const editButton = document.createElement("button"); // a REAL button: free keyboard
        editButton.type = "button"; // operability + role, never a clickable <div>
        editButton.textContent = "Edit";
        editButton.addEventListener("click", () => callbacks.onEdit(task));
        li.append(summary, editButton);
        ul.append(li);
      }
      root.append(ul);
      return;
    }
  }
}
