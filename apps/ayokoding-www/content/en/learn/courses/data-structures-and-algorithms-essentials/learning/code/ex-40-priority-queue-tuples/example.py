"""Example 40: Priority Queue with (priority, task) Tuples."""

# heapq compares TUPLES element-by-element, so a (priority, task) tuple sorts
# by priority first -- the standard way to build a priority queue (co-12).
import heapq

tasks: list[
    tuple[int, str]
] = []  # => each entry is (priority, task_name); lower = more urgent
heapq.heappush(tasks, (3, "cleanup"))  # => low urgency
heapq.heappush(
    tasks, (1, "fix outage")
)  # => highest urgency -- smallest priority number
heapq.heappush(tasks, (2, "deploy"))  # => medium urgency

order: list[str] = []  # => records the order tasks are served in
while tasks:  # => drains the heap, always taking the lowest-priority-number tuple first
    priority, task = heapq.heappop(
        tasks
    )  # => unpacks the popped (priority, task) tuple
    order.append(task)  # => records just the task name for the assertion below
print(order)  # => Output: ['fix outage', 'deploy', 'cleanup']

assert order == [
    "fix outage",
    "deploy",
    "cleanup",
]  # => confirms urgent-first pop order
print("ex-40 OK")  # => Output: ex-40 OK
