"""Example 71: pytest verification for Constraint Scheduling."""

from example import Task, schedule


def test_returned_schedule_respects_every_precedence_constraint() -> None:
    tasks = [
        Task("design", 2),
        Task("build", 3, depends_on=("design",)),
        Task("test", 2, depends_on=("build",)),
        Task("docs", 1, depends_on=("design",)),
    ]
    result = schedule(tasks)  # => same tasks as the module-level demo
    for task in tasks:  # => every declared dependency must finish before the dependent task starts
        for dep in task.depends_on:
            assert result[dep][1] <= result[task.name][0]


def test_returned_schedule_never_double_books_the_single_resource() -> None:
    tasks = [Task("a", 2), Task("b", 3, depends_on=("a",)), Task("c", 1, depends_on=("a",))]
    result = schedule(tasks)
    intervals = sorted(result.values())  # => sort by (start, end)
    for (_s1, e1), (s2, _e2) in zip(intervals, intervals[1:]):  # => every consecutive pair
        assert e1 <= s2  # => no two tasks overlap in time -- the single-resource constraint holds


# => Run: pytest -- Output: 2 passed
