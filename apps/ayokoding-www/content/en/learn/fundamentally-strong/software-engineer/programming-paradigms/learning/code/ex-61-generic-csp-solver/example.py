"""Example 61: Generic CSP Solver (with Propagation)."""

from collections.abc import Callable  # => types every Constraint stored below

Variable = str  # => a type alias -- variable names are just strings
Value = int  # => a type alias -- domain values are just integers
Assignment = dict[Variable, Value]  # => a partial or full mapping from variable to chosen value
Constraint = Callable[[Assignment], bool]  # => a constraint checks a PARTIAL assignment for consistency


class CSPSolver:  # => generic over variables, domains, and constraints -- knows nothing about "sudoku"
    def __init__(  # => constructor takes the whole CSP declaration: variables, domains, constraints
        self,
        variables: list[Variable],  # => every variable that needs a value
        domains: dict[Variable, list[Value]],  # => each variable's own candidate values
        constraints: list[Constraint],  # => every rule an assignment must satisfy
    ) -> None:
        self.variables = variables  # => stored as-is -- this solver never mutates the declared variable list
        self.domains = domains  # => stored as-is -- solve() works from a fresh copy, not this original
        self.constraints = constraints  # => stored as-is -- checked by _consistent() below

    def _consistent(self, assignment: Assignment) -> bool:  # => check every constraint against what's assigned
        return all(c(assignment) for c in self.constraints)  # => a constraint referencing an unassigned var
        # => must itself handle that (return True until enough variables are bound to judge)

    def _propagate_domain(self, var: Variable, value: Value, assignment: Assignment) -> dict[Variable, list[Value]]:  # => forward-checking entry point
        # => forward-checking PROPAGATION: after assigning var=value, shrink neighbors' remaining domains
        pruned = {v: list(d) for v, d in self.domains.items()}  # => a working copy, original domains untouched
        trial = {**assignment, var: value}  # => a "what if" assignment, used only to test consistency
        for other in self.variables:  # => check every OTHER variable's remaining candidates against `trial`
            if other == var or other in assignment:  # => skip the variable just assigned and any already-fixed
                continue  # => nothing to prune for a variable that already has (or doesn't need) a value
            pruned[other] = [val for val in pruned[other] if self._consistent({**trial, other: val})]  # => keep only values still consistent
        return pruned  # => every remaining domain, possibly shrunk by this one assignment

    def solve(self) -> Assignment | None:  # => backtracking search, augmented with propagation
        def backtrack(assignment: Assignment, domains: dict[Variable, list[Value]]) -> Assignment | None:  # => the recursive search itself
            if len(assignment) == len(self.variables):  # => every variable assigned -- solved
                return dict(assignment)  # => copy out only on success, matching solve_coloring's convention
            unassigned = [v for v in self.variables if v not in assignment][0]  # => next variable to try
            for value in domains[unassigned]:  # => CHOICE POINT, but only over the ALREADY-PRUNED domain
                if self._consistent({**assignment, unassigned: value}):  # => only try values that satisfy every constraint so far
                    assignment[unassigned] = value  # => tentatively assign
                    pruned = self._propagate_domain(unassigned, value, assignment)  # => propagate immediately
                    if all(pruned[v] for v in self.variables if v not in assignment):  # => no domain went empty
                        result = backtrack(assignment, pruned)  # => recurse with the SHRUNK domains
                        if result is not None:  # => a deeper call already found a full solution
                            return result  # => propagate success straight back up the recursion
                    del assignment[unassigned]  # => BACKTRACK: undo, try the next value
            return None  # => no value in this domain led to a solution given the current partial assignment

        return backtrack({}, {v: list(d) for v, d in self.domains.items()})  # => start the search from an empty assignment and full domains


def solve_map_coloring() -> Assignment | None:  # => reuses the SAME solver for a totally different puzzle
    adjacency = {"west": ["central"], "central": ["west", "east"], "east": ["central"]}  # => same graph as example 38
    variables = list(adjacency.keys())  # => one CSP variable per region
    domains = {v: [0, 1, 2] for v in variables}  # => 0, 1, 2 stand in for three colors

    def make_constraint(a: str, b: str) -> Constraint:  # => a factory closing over which pair must differ
        def constraint(assignment: Assignment) -> bool:  # => returns True until BOTH sides are assigned
            return a not in assignment or b not in assignment or assignment[a] != assignment[b]  # => vacuously true if either side is still unassigned

        return constraint  # => a fresh closure per adjacent pair, capturing a and b by reference

    constraints = [make_constraint(a, b) for a, neighbors in adjacency.items() for b in neighbors if a < b]  # => one constraint per undirected edge, counted once
    return CSPSolver(variables, domains, constraints).solve()  # => the SAME generic solve() as any other CSP


result = solve_map_coloring()  # => the SAME generic solver, applied to map coloring
# => neither CSPSolver nor backtrack() contains a single line of map-coloring-specific logic
print(result is not None)  # => a solution was found
# => Output: True
