"""Example 45: pytest verification for Process Isolation of Global State."""

import multiprocessing

from example import mutate_in_child, shared_looking_list


def test_child_process_mutation_is_invisible_to_the_parent() -> None:
    shared_looking_list.clear()
    shared_looking_list.append(1)  # => the parent's own state before spawning the child
    child = multiprocessing.Process(target=mutate_in_child)
    child.start()
    child.join()
    assert shared_looking_list == [1]  # => the child's append(999) never reached the parent's own list


# => Run: pytest -- Output: 1 passed
