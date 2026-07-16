// Full-stack capstone: api.ts -- the typed HTTP client (topic 12 Networking Essentials: `fetch`
// over HTTP) talking to the backend's CORS-safe endpoints (topic 11). This is the ONLY module
// that calls `fetch` -- app.ts never does, so every request this app makes has one typed,
// testable choke point.
import type { Task, TaskStatus } from "./types";

export interface TaskDraft {
  title: string;
  description: string;
}

export interface TaskUpdateBody {
  title: string;
  description: string;
  status: TaskStatus;
}

// => a request-scoped error carrying the server's own message, not a generic "fetch failed"
export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function parseErrorMessage(response: Response): Promise<string> {
  try {
    const body: unknown = await response.json();
    if (
      typeof body === "object" &&
      body !== null &&
      "error" in body &&
      typeof (body as { error: unknown }).error === "object" &&
      (body as { error: { message?: unknown } }).error !== null &&
      typeof (body as { error: { message?: unknown } }).error.message === "string"
    ) {
      return (body as { error: { message: string } }).error.message;
    }
    // => this app's own handlers (404s, etc.) always use the {"error": {"message": ...}}
    // => envelope above, but FastAPI's DEFAULT 422 handler for a Pydantic validation failure
    // => (e.g. a title over the 200-char limit) is never routed through that envelope -- it's
    // => {"detail": ...}, where `detail` is either a plain string or FastAPI's list-of-error-
    // => objects shape (each entry carrying a human-readable `msg`)
    if (typeof body === "object" && body !== null && "detail" in body) {
      const detail = (body as { detail: unknown }).detail;
      if (typeof detail === "string") return detail;
      if (Array.isArray(detail)) {
        const messages = detail.filter(
          (item): item is { msg: string } =>
            typeof item === "object" && item !== null && typeof (item as { msg?: unknown }).msg === "string",
        );
        if (messages.length > 0) return messages.map((item) => item.msg).join("; ");
      }
    }
  } catch {
    // => body wasn't JSON, or didn't match a recognized error envelope -- fall through to the
    // => generic message below rather than let a parse error mask the real one
  }
  return `request failed with status ${response.status}`;
}

export function makeApi(baseUrl: string) {
  async function fetchTasks(): Promise<Task[]> {
    const response = await fetch(`${baseUrl}/tasks`);
    if (!response.ok) throw new ApiError(await parseErrorMessage(response), response.status);
    return (await response.json()) as Task[];
  }

  async function createTask(draft: TaskDraft): Promise<Task> {
    const response = await fetch(`${baseUrl}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(draft),
    });
    if (!response.ok) throw new ApiError(await parseErrorMessage(response), response.status);
    return (await response.json()) as Task;
  }

  async function updateTask(id: number, body: TaskUpdateBody): Promise<Task> {
    const response = await fetch(`${baseUrl}/tasks/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new ApiError(await parseErrorMessage(response), response.status);
    return (await response.json()) as Task;
  }

  return { fetchTasks, createTask, updateTask };
}

export type Api = ReturnType<typeof makeApi>;
