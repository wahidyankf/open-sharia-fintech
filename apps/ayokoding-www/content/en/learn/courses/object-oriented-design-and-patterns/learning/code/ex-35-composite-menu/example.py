"""Example 35: Composite Renders Nested Menu Items Uniformly."""

import abc  # => imports the abc module


class MenuComponent(abc.ABC):  # => the COMPONENT interface -- shared by leaf and group
    @abc.abstractmethod
    def render(self, indent: int = 0) -> str:  # => no body -- required by both
        ...  # => the ellipsis stub -- MenuItem and Menu below fill this in


class MenuItem(MenuComponent):  # => the LEAF -- a single, non-nestable entry
    def __init__(self, label: str) -> None:  # => the constructor
        self.label = label  # => stores label on this instance

    def render(self, indent: int = 0) -> str:  # => the leaf case -- one indented line
        return " " * indent + f"- {self.label}"  # => returns this value to the caller


class Menu(MenuComponent):  # => the COMPOSITE -- a named GROUP of MenuComponents
    def __init__(self, label: str) -> None:  # => the constructor
        self.label = label  # => stores label on this instance
        self._items: list[MenuComponent] = []  # => MenuItems AND nested Menus, mixed freely

    def add(self, item: MenuComponent) -> None:  # => defines the add() method
        self._items.append(item)  # => accepts a MenuItem OR another Menu, identically

    def render(self, indent: int = 0) -> str:  # => the composite case -- itself PLUS children
        header: str = " " * indent + f"+ {self.label}"  # => this group's own header line
        child_lines: list[str] = [item.render(indent + 2) for item in self._items]  # => each child renders itself, MORE indented, possibly recursing again
        return "\n".join([header, *child_lines])  # => returns this value to the caller


file_menu: Menu = Menu("File")  # => constructs file_menu
file_menu.add(MenuItem("New"))  # => a leaf, added directly
file_menu.add(MenuItem("Open"))  # => a leaf, added directly
recent: Menu = Menu("Open Recent")  # => a NESTED composite submenu
recent.add(MenuItem("project.py"))  # => a leaf inside the nested submenu
file_menu.add(recent)  # => the nested Menu is itself just another MenuComponent
print(file_menu.render())  # => leaves and the nested group render through ONE call
# => Output: + File
# =>           - New
# =>           - Open
# =>           + Open Recent
# =>             - project.py
# => `file_menu.render()` never branches on whether an item is a MenuItem or a nested Menu
