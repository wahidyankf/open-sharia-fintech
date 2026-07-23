// Full-stack capstone: types.ts -- Task mirrors the backend's Task Pydantic model field-for-
// field (topic 14 typed UI + topic 11 HTTP JSON API: one shared shape, expressed on both sides
// of the wire), plus the TaskListState discriminated union modeling the whole list's
// loading/error/empty/loaded UI state (topic 14, reused from Frontend Essentials' own capstone).

export type TaskStatus = "todo" | "in_progress" | "done";

export interface Task {
  id: number;
  title: string;
  description: string;
  status: TaskStatus;
  created_at: string;
}

export type TaskListState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "empty" }
  | { status: "loaded"; tasks: Task[] };
