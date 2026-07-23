"""Example 35: pytest verification for Composite Menu Rendering."""

from example import Menu, MenuItem


def test_leaf_and_nested_group_render_through_one_interface() -> None:
    file_menu: Menu = Menu("File")
    file_menu.add(MenuItem("New"))
    recent: Menu = Menu("Open Recent")
    recent.add(MenuItem("project.py"))
    file_menu.add(recent)  # => a Menu nested inside another Menu
    rendered: str = file_menu.render()
    assert "+ File" in rendered  # => the top-level group's own header
    assert "- New" in rendered  # => a direct leaf item
    assert "+ Open Recent" in rendered  # => the nested group's own header
    assert "- project.py" in rendered  # => a leaf inside the nested group


def test_nested_items_are_indented_more_than_their_parent() -> None:
    root: Menu = Menu("Root")
    root.add(MenuItem("Top"))
    lines: list[str] = root.render().splitlines()
    assert lines[0] == "+ Root"  # => no indentation at the top level
    assert lines[1] == "  - Top"  # => one nesting level deeper, two spaces indented


# => Run: pytest -- Output: 2 passed
