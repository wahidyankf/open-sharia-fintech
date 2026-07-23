"""Example 71: Constraint Scheduling."""

from dataclasses import dataclass  # => @dataclass generates Task's __init__ from its three fields


@dataclass(frozen=True)  # => a task DECLARED with its duration and which tasks must finish first
class Task:  # => frozen=True -- a task's own declared shape is a fact, never edited in place
    name: str  # => the task's identifier, referenced by other tasks' depends_on tuples
    duration: int  # => how long this task takes, once it starts
    depends_on: tuple[str, ...] = ()  # => precedence constraints -- these tasks must finish before this one


tasks: list[Task] = [  # => the whole schedule is DECLARED as data -- no imperative "plan the day" code
    Task("design", 2),  # => no dependencies -- can start immediately
    Task("build", 3, depends_on=("design",)),  # => can't start until design finishes
    Task("test", 2, depends_on=("build",)),  # => can't start until build finishes
    Task("docs", 1, depends_on=("design",)),  # => docs only needs design, so it can overlap with build
]  # => closes the declared task list -- four tasks, three of them with a precedence constraint

RESOURCE_CAPACITY = 1  # => only ONE task may run at a time (a single worker) -- a resource constraint
# => the scheduler below enforces both this resource constraint AND every task's precedence constraint


def schedule(tasks: list[Task]) -> dict[str, tuple[int, int]]:  # => returns name -> (start, end)
    start_time: dict[str, int] = {}  # => the schedule being built
    end_time: dict[str, int] = {}  # => a task counts as "done" once it has an entry here
    busy_until = 0  # => tracks when the single resource becomes free next (RESOURCE_CAPACITY == 1)

    def ready(t: Task) -> bool:  # => a task is ready once every precedence constraint is satisfied
        return all(dep in end_time for dep in t.depends_on)  # => every dependency must already be scheduled

    remaining = list(tasks)  # => working copy, shrinks as tasks get scheduled
    while remaining:  # => keep scheduling until every task has been placed
        candidates = [t for t in remaining if ready(t)]  # => only precedence-satisfied tasks may be picked
        if not candidates:  # => defensive check: a cycle would leave no task ready
            raise ValueError("unsatisfiable precedence constraints")  # => fails loudly instead of looping forever
        chosen = min(candidates, key=lambda t: t.duration)  # => a simple, deterministic tie-break policy
        start = max(busy_until, max((end_time[d] for d in chosen.depends_on), default=0))  # => resource AND precedence, both respected
        end = start + chosen.duration  # => the chosen task's computed end time
        start_time[chosen.name] = start  # => record this task's start
        end_time[chosen.name] = end  # => record this task's end -- also satisfies `ready()` for its dependents
        busy_until = end  # => the single resource is occupied until this task finishes
        remaining.remove(chosen)  # => this task is fully scheduled -- no longer tracked as "remaining"
    return {name: (start_time[name], end_time[name]) for name in start_time}  # => the full computed schedule


result = schedule(tasks)  # => run the constraint-driven scheduler
print(result)  # => a feasible schedule respecting both precedence and the single-resource constraint
# => Output: {'design': (0, 2), 'docs': (2, 3), 'build': (3, 6), 'test': (6, 8)}
