"""Example 34: Composite Treats File and Directory Uniformly for size()."""

import abc  # => imports the abc module


class FileSystemEntry(abc.ABC):  # => the COMPONENT interface -- shared by leaf AND composite
    @abc.abstractmethod
    def size(self) -> int:  # => no body -- required by both File and Directory
        ...  # => the ellipsis stub -- File and Directory below fill this in


class File(FileSystemEntry):  # => the LEAF -- has no children of its own
    def __init__(self, name: str, size_bytes: int) -> None:  # => the constructor
        self.name = name  # => stores name on this instance
        self._size_bytes = size_bytes  # => stores this leaf's own, fixed size

    def size(self) -> int:  # => the leaf case -- just returns its own size
        return self._size_bytes  # => returns this value to the caller


class Directory(FileSystemEntry):  # => the COMPOSITE -- holds a list of ANY FileSystemEntry
    def __init__(self, name: str) -> None:  # => the constructor
        self.name = name  # => stores name on this instance
        self._children: list[FileSystemEntry] = []  # => Files AND Directories, mixed freely

    def add(self, entry: FileSystemEntry) -> None:  # => defines the add() method
        self._children.append(entry)  # => accepts a File OR another Directory, identically

    def size(self) -> int:  # => the composite case -- sums every child, RECURSIVELY
        return sum(child.size() for child in self._children)  # => each child.size() call may itself recurse into a nested Directory


root: Directory = Directory("project")  # => constructs root
root.add(File("readme.md", 120))  # => a leaf, added directly to the root
src: Directory = Directory("src")  # => a NESTED composite
src.add(File("main.py", 300))  # => a leaf inside the nested directory
src.add(File("utils.py", 180))  # => a second leaf inside the nested directory
root.add(src)  # => the nested Directory is itself just another FileSystemEntry
print(root.size())  # => 120 + (300 + 180) -- computed through ONE uniform size() call
# => Output: 600
# => `root.size()` never checks whether a child is a File or a Directory -- both answer size() the same way
