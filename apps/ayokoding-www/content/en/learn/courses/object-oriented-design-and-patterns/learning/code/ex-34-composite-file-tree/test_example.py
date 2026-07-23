"""Example 34: pytest verification for Composite File Tree size()."""

from example import Directory, File


def test_recursive_size_sums_nested_directories_through_one_interface() -> None:
    root: Directory = Directory("project")
    root.add(File("readme.md", 120))
    src: Directory = Directory("src")
    src.add(File("main.py", 300))
    src.add(File("utils.py", 180))
    root.add(src)  # => a Directory nested inside another Directory
    assert root.size() == 600  # => 120 + 300 + 180, computed recursively


def test_a_single_file_answers_size_directly() -> None:
    assert File("a.txt", 42).size() == 42  # => the leaf case needs no recursion at all


# => Run: pytest -- Output: 2 passed
