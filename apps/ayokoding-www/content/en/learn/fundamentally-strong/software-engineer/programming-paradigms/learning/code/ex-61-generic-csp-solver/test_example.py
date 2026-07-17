"""Example 61: pytest verification for Generic CSP Solver (with Propagation)."""

from example import Assignment, Constraint, CSPSolver, solve_map_coloring


def test_generic_solver_solves_map_coloring() -> None:
    result = solve_map_coloring()  # => same call as the module-level demo
    assert result is not None  # => a valid 3-coloring exists for this simple adjacency
    assert result["central"] != result["west"]  # => the actual declared constraints
    assert result["central"] != result["east"]


def test_generic_solver_solves_a_tiny_sudoku_style_grid() -> None:
    # => reuse the SAME CSPSolver class for a 2x2 latin-square: each row/col has distinct values 1,2
    variables = ["r0c0", "r0c1", "r1c0", "r1c1"]
    domains = {v: [1, 2] for v in variables}

    def distinct(a: str, b: str) -> Constraint:  # => matches example.py's make_constraint signature
        def constraint(assignment: Assignment) -> bool:  # => fully typed closure, no Unknown inference
            return a not in assignment or b not in assignment or assignment[a] != assignment[b]

        return constraint

    constraints = [
        distinct("r0c0", "r0c1"),  # => row 0 distinct
        distinct("r1c0", "r1c1"),  # => row 1 distinct
        distinct("r0c0", "r1c0"),  # => column 0 distinct
        distinct("r0c1", "r1c1"),  # => column 1 distinct
    ]
    result = CSPSolver(variables, domains, constraints).solve()
    assert result is not None  # => a valid 2x2 latin square exists
    assert result["r0c0"] != result["r0c1"]  # => spot-check one of the declared constraints holds


# => Run: pytest -- Output: 2 passed
