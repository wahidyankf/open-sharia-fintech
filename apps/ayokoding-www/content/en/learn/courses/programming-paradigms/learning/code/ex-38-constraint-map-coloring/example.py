"""Example 38: Constraint Map Coloring."""

Region = str  # => a type alias -- purely for readability, region names are just strings
Color = str  # => a type alias -- purely for readability, color names are just strings

adjacency: dict[Region, list[Region]] = {  # => DECLARE the constraint: which regions must differ in color
    "west": ["central"],  # => west is adjacent to central only
    "central": ["west", "east"],  # => central is adjacent to both neighbors
    "east": ["central"],  # => east is adjacent to central only
}  # => nothing here says HOW to search -- just which pairs may never share a color

colors: list[Color] = ["red", "green", "blue"]  # => the available palette (3-coloring)


def solve_coloring(adj: dict[Region, list[Region]], palette: list[Color]) -> dict[Region, Color] | None:  # => the GENERIC part: works for any adjacency map, any palette
    regions = list(adj.keys())  # => a fixed order to assign regions in
    assignment: dict[Region, Color] = {}  # => the partial (then full) solution being built

    def backtrack(index: int) -> bool:  # => try to color every region from `index` onward
        if index == len(regions):  # => base case: every region has a color -- solved
            return True  # => the assignment dict already holds a complete, valid coloring
        region = regions[index]  # => the region we're choosing a color for right now
        for color in palette:  # => CHOICE POINT: try every color in the palette
            if all(assignment.get(neighbor) != color for neighbor in adj[region]):  # => check the constraint
                assignment[region] = color  # => tentatively assign
                if backtrack(index + 1):  # => recurse to the next region
                    return True  # => success propagates straight back up -- no del assignment[region] needed
                del assignment[region]  # => BACKTRACK: undo this color, try the next one
        return False  # => no color in the palette works given the current partial assignment

    return dict(assignment) if backtrack(0) else None  # => copy out only on success


result = solve_coloring(adjacency, colors)  # => run the solver
assert result is not None  # => narrow away None -- this adjacency/palette pair always has a valid coloring
print(result)  # => west and east may share a color; central must differ from both
# => Output: {'west': 'red', 'central': 'green', 'east': 'red'}
print(all(result[a] != result[b] for a, neighbors in adjacency.items() for b in neighbors))  # => verify
# => Output: True
