// Full-stack capstone -- the Testing-Library UI test (topic 15 Software Testing, Step 4 of the
// capstone spec): Vitest + @testing-library/dom, driven against the real mountApp component with
// a MOCKED global fetch -- no live server -- verifying loading/error/empty/loaded states and that
// the create/update form genuinely calls the API and refetches, exactly the sequence a real
// browser session drives (verified separately, live, in overview.md's browser walkthrough).
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, fireEvent, within } from "@testing-library/dom";
import { mountApp } from "./app.js";
import { makeApi } from "./api.js";
import type { Task } from "./types.js";

function freshRoot(): HTMLElement {
  document.body.innerHTML = "";
  const root = document.createElement("div");
  document.body.append(root);
  return root;
}

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

const TASK: Task = {
  id: 1,
  title: "Write the report",
  description: "Q3 summary",
  status: "todo",
  created_at: "2026-07-16 00:00:00",
};

beforeEach(() => {
  vi.restoreAllMocks();
});

describe("capstone: initial render (step 2)", () => {
  it("renders the loading state synchronously, before fetch resolves", () => {
    const root = freshRoot();
    vi.stubGlobal(
      "fetch",
      vi.fn(() => new Promise<Response>(() => {})),
    );
    mountApp(root, makeApi("http://api.test"));
    expect(screen.getByRole("status").textContent).toBe("Loading tasks...");
  });
});

describe("capstone: discriminated-union states (step 2, co-27 reused)", () => {
  it("transitions loading -> empty when GET /tasks resolves to []", async () => {
    const root = freshRoot();
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.resolve(jsonResponse([]))),
    );
    mountApp(root, makeApi("http://api.test"));
    await screen.findByText("No tasks yet.");
  });

  it("transitions loading -> error when GET /tasks returns a non-2xx status", async () => {
    const root = freshRoot();
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.resolve(jsonResponse({ error: { code: "boom", message: "database unreachable" } }, 500))),
    );
    mountApp(root, makeApi("http://api.test"));
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toBe("database unreachable");
  });

  it("transitions loading -> error with the browser's own message when fetch rejects (network failure, no response at all)", async () => {
    const root = freshRoot();
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.reject(new TypeError("Failed to fetch"))),
    );
    mountApp(root, makeApi("http://api.test"));
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toBe("Failed to fetch"); // => the generic `error instanceof Error`
    // => branch in app.ts's errorMessage(), distinct from the ApiError branch tested above
  });

  it("transitions loading -> loaded, rendering an Edit button per task", async () => {
    const root = freshRoot();
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.resolve(jsonResponse([TASK]))),
    );
    mountApp(root, makeApi("http://api.test"));
    const item = await screen.findByText("Write the report [todo]");
    const list = item.closest("li");
    expect(list).not.toBeNull();
    within(list as HTMLElement).getByRole("button", { name: "Edit" });
  });
});

describe("capstone: create/update form (step 3)", () => {
  it("submitting the create form POSTs to /tasks, then refetches -- the new task appears", async () => {
    const root = freshRoot();
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const method = init?.method ?? "GET";
      if (method === "GET" && fetchMock.mock.calls.length === 1) {
        return Promise.resolve(jsonResponse([])); // initial mount load: empty
      }
      if (method === "POST" && url === "http://api.test/tasks") {
        return Promise.resolve(jsonResponse(TASK, 201)); // the create call
      }
      return Promise.resolve(jsonResponse([TASK])); // the refetch after create
    });
    vi.stubGlobal("fetch", fetchMock);

    mountApp(root, makeApi("http://api.test"));
    await screen.findByText("No tasks yet.");

    fireEvent.input(screen.getByLabelText("Title"), { target: { value: "Write the report" } });
    fireEvent.input(screen.getByLabelText("Description"), { target: { value: "Q3 summary" } });
    fireEvent.submit(screen.getByRole("button", { name: "Add task" }).closest("form") as HTMLFormElement);

    await screen.findByText("Write the report [todo]"); // reflects the REFETCH, not an optimistic splice
    expect(fetchMock).toHaveBeenCalledTimes(3); // initial GET, POST, refetch GET
    const postCall = fetchMock.mock.calls[1];
    expect(postCall[1]?.method).toBe("POST");
    expect(JSON.parse(String(postCall[1]?.body))).toEqual({
      title: "Write the report",
      description: "Q3 summary",
    });
  });

  it("clicking Edit switches to update mode, and submitting PUTs then refetches", async () => {
    const root = freshRoot();
    const updated: Task = { ...TASK, status: "done" };
    const fetchMock = vi.fn((_input: RequestInfo | URL, init?: RequestInit) => {
      const method = init?.method ?? "GET";
      if (method === "PUT") return Promise.resolve(jsonResponse(updated));
      if (fetchMock.mock.calls.length === 1) return Promise.resolve(jsonResponse([TASK]));
      return Promise.resolve(jsonResponse([updated])); // the refetch after update
    });
    vi.stubGlobal("fetch", fetchMock);

    mountApp(root, makeApi("http://api.test"));
    await screen.findByText("Write the report [todo]");

    fireEvent.click(screen.getByRole("button", { name: "Edit" }));
    expect(screen.getByLabelText<HTMLInputElement>("Title").value).toBe("Write the report");
    fireEvent.change(screen.getByLabelText("Status"), { target: { value: "done" } });
    fireEvent.submit(screen.getByRole("button", { name: "Update task" }).closest("form") as HTMLFormElement);

    await screen.findByText("Write the report [done]");
    const putCall = fetchMock.mock.calls.find((call) => call[1]?.method === "PUT");
    expect(putCall).toBeDefined();
    expect(JSON.parse(String(putCall?.[1]?.body))).toEqual({
      title: "Write the report",
      description: "Q3 summary",
      status: "done",
    });
  });

  it("submitting an empty title shows a validation error without calling fetch again", async () => {
    const root = freshRoot();
    const fetchMock = vi.fn(() => Promise.resolve(jsonResponse([])));
    vi.stubGlobal("fetch", fetchMock);

    mountApp(root, makeApi("http://api.test"));
    await screen.findByText("No tasks yet.");
    const callsBeforeSubmit = fetchMock.mock.calls.length;

    fireEvent.submit(screen.getByRole("button", { name: "Add task" }).closest("form") as HTMLFormElement);

    expect(await screen.findByRole("alert")).toHaveProperty("textContent", "Enter a task title");
    expect(fetchMock.mock.calls.length).toBe(callsBeforeSubmit); // no network call was made
  });

  // => there's no client-side mirror of the backend's 200-char title limit (models.py's
  // => `Field(max_length=200)`), so an over-length title genuinely reaches the server and comes
  // => back as a real 422 -- in FastAPI's OWN default validation-error envelope
  // => (`{"detail": [...]}`), never this app's `{"error": {"message": ...}}` envelope. The exact
  // => body below is what a real POST with a 201-character title returns from the live backend.
  it("shows FastAPI's own validation-error reason when the server rejects an over-length title with a 422", async () => {
    const root = freshRoot();
    const overLengthTitle = "x".repeat(201);
    const fetchMock = vi.fn((_input: RequestInfo | URL, init?: RequestInit) => {
      const method = init?.method ?? "GET";
      if (method === "POST") {
        return Promise.resolve(
          jsonResponse(
            {
              detail: [
                {
                  type: "string_too_long",
                  loc: ["body", "title"],
                  msg: "String should have at most 200 characters",
                  input: overLengthTitle,
                  ctx: { max_length: 200 },
                },
              ],
            },
            422,
          ),
        );
      }
      return Promise.resolve(jsonResponse([])); // initial mount load; no refetch since the POST fails
    });
    vi.stubGlobal("fetch", fetchMock);

    mountApp(root, makeApi("http://api.test"));
    await screen.findByText("No tasks yet.");

    fireEvent.input(screen.getByLabelText("Title"), { target: { value: overLengthTitle } });
    fireEvent.submit(screen.getByRole("button", { name: "Add task" }).closest("form") as HTMLFormElement);

    expect(await screen.findByRole("alert")).toHaveProperty(
      "textContent",
      "String should have at most 200 characters", // not the generic "request failed with status 422"
    );
  });
});
