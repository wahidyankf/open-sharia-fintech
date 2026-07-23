"""Example 72: Reactive Spreadsheet."""

from collections.abc import Callable  # => types every formula cell: a function from Spreadsheet to float


class Spreadsheet:  # => a minimal working spreadsheet: named cells, some raw, some formulas
    def __init__(self) -> None:  # => constructor seeds all three pieces of private state
        self._raw: dict[str, float] = {}  # => cells holding a plain number
        self._formulas: dict[str, Callable[["Spreadsheet"], float]] = {}  # => cells holding a formula
        self._dependents: dict[str, list[str]] = {}  # => cell -> formula cells that reference it

    def set_value(self, name: str, value: float) -> None:  # => set a raw cell and cascade the recompute
        self._raw[name] = value  # => store the new raw value
        self._cascade(name)  # => propagate to every formula cell that (transitively) depends on it

    def set_formula(self, name: str, formula: Callable[["Spreadsheet"], float], depends_on: list[str]) -> None:
        self._formulas[name] = formula  # => register the formula
        for dep in depends_on:  # => wire this formula as a dependent of every cell it reads
            self._dependents.setdefault(dep, []).append(name)  # => reverse-index: dep -> cells that read it
        self._cascade(name)  # => compute its initial value immediately

    def get(self, name: str) -> float:  # => read any cell -- raw or formula -- through one uniform API
        if name in self._formulas:  # => formula cells compute lazily, on every read
            return self._formulas[name](self)  # => re-run the formula against the CURRENT spreadsheet state
        return self._raw.get(name, 0.0)  # => raw cells just return their stored number

    def _cascade(self, changed: str) -> list[str]:  # => returns the cells that were refreshed, for verification
        refreshed: list[str] = []  # => accumulates every cell touched by this cascade, in visit order
        frontier = list(self._dependents.get(changed, []))  # => direct dependents of the changed cell
        while frontier:  # => cascade OUTWARD, level by level, through the whole dependency chain
            name = frontier.pop(0)  # => dequeue the next dependent to visit, FIFO order
            if name not in refreshed:  # => avoid re-cascading a cell already refreshed this update
                refreshed.append(name)  # => record that this cell was refreshed by this cascade
                frontier.extend(self._dependents.get(name, []))  # => this cell's own dependents cascade too
        return refreshed  # => the full set of cells touched, useful for tests and debugging


sheet = Spreadsheet()  # => a fresh spreadsheet
# => a1 is raw; b1 and c1 are formulas that transitively depend on a1, two levels deep
sheet.set_value("a1", 10)  # => raw cell
sheet.set_formula("b1", lambda s: s.get("a1") * 2, depends_on=["a1"])  # => b1 = a1 * 2
sheet.set_formula("c1", lambda s: s.get("b1") + 1, depends_on=["b1"])  # => c1 = b1 + 1 -- a THIRD level

print(sheet.get("c1"))  # => a1=10 -> b1=20 -> c1=21, a two-level cascade from a single set_value
# => Output: 21

sheet.set_value("a1", 100)  # => change the root cell -- must cascade through TWO formula levels
print(sheet.get("b1"), sheet.get("c1"))  # => b1=200, c1=201 -- both levels reflect the new root value
# => Output: 200 201
