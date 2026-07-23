from typing import TypedDict


class Task(TypedDict):  # => co-14: the repo returns a TYPED shape, not a loose dict-of-anything
    id: int
    title: str
    done: bool


class TaskRepository:  # => co-14/co-24: the ONLY place that touches the "store" -- a mocked in-memory table
    def __init__(self) -> None:
        self._rows: dict[int, Task] = {}  # => stands in for a real DB table for this pure kata
        self._next_id = 1  # => stands in for an auto-increment primary key

    def create(self, title: str) -> Task:  # => co-14: INSERT-equivalent
        task: Task = {"id": self._next_id, "title": title, "done": False}
        self._rows[self._next_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task | None:  # => co-14: SELECT-by-id-equivalent
        return self._rows.get(task_id)  # => None if absent -- the CALLER decides how to map that to a 404

    def update_done(self, task_id: int, done: bool) -> Task | None:  # => co-14: UPDATE-equivalent
        task = self._rows.get(task_id)
        if task is None:  # => co-14: nothing to update -- signal absence, don't raise a generic error
            return None
        task["done"] = done  # => in a real repo this would be a parameterized UPDATE ... WHERE id = ?
        return task

    def delete(self, task_id: int) -> bool:  # => co-14: DELETE-equivalent
        return self._rows.pop(task_id, None) is not None  # => True only if a row actually existed


def complete_task_handler(repo: TaskRepository, task_id: int) -> dict[str, object]:
    # => co-24: the HANDLER holds zero persistence logic -- it only calls the repo and shapes a response
    task = repo.update_done(task_id, True)  # => all the "how do we store this" detail lives in the repo
    if task is None:
        return {"status": 404, "body": {"error": "task not found"}}  # => co-11: a structured 404
    return {"status": 200, "body": task}


repo = TaskRepository()
created = repo.create("Write the report")  # => co-14: id=1 assigned by the repo, not the handler
print(created)  # => Output: {'id': 1, 'title': 'Write the report', 'done': False}
assert created == {"id": 1, "title": "Write the report", "done": False}

response = complete_task_handler(repo, created["id"])  # => the handler never sees a single line of SQL
missing_response = complete_task_handler(repo, 999)  # => a task id that was never created

print(response)  # => Output: {'status': 200, 'body': {'id': 1, 'title': 'Write the report', 'done': True}}
print(missing_response)  # => Output: {'status': 404, 'body': {'error': 'task not found'}}

assert response["status"] == 200
body = response["body"]
assert isinstance(body, dict) and body["done"] is True  # => the repo's update actually persisted
assert missing_response["status"] == 404  # => co-14/co-11: a clean 404, not a KeyError leaking upward
print("kata-11 OK")
