// Capstone types: a single task plus the discriminated union modeling the whole
// list's loading/error/empty/loaded UI state (co-27, co-28).

export interface Task {
  id: string;
  title: string;
  done: boolean;
}

export type TaskListState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "empty" }
  | { status: "loaded"; tasks: Task[] };

/** A loader is any function returning a Promise of the initial task list --
 * resolving to [] drives the "empty" state, resolving to a non-empty array
 * drives "loaded", and rejecting drives "error". */
export type Loader = () => Promise<Task[]>;
