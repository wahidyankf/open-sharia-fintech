# learning/code/ex-48-reduction-3sat-to-clique/reduction_3sat_clique.py
"""Example 48: Reducing a 3-SAT Instance to a Clique Instance."""  # => co-25: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import itertools  # => co-25: brute-force clique search AND brute-force SAT search, for the equivalence check

Clause = tuple[int, int, int]  # => co-25: a 3-SAT clause -- three literals (positive = var, negative = its negation)
Node = tuple[int, int]  # => co-25: a clique-graph node -- (clause index, literal position within that clause)


def literals_compatible(lit_a: int, lit_b: int) -> bool:  # => co-25: the reduction's edge rule
    """Two literals are compatible (an edge exists) unless they are negations of the same variable."""  # => co-25: documents literals_compatible's contract -- no runtime output, just sets its __doc__
    return not (lit_a == -lit_b)  # => co-25: x and NOT x can never BOTH be True -- exactly the excluded pair


def reduce_3sat_to_clique(clauses: list[Clause]) -> tuple[set[tuple[Node, Node]], dict[Node, int]]:  # => co-25
    """Build the standard 3-SAT -> Clique reduction: one node per (clause, literal), edges between
    compatible literals from DIFFERENT clauses. A satisfying assignment exists iff a clique of size
    len(clauses) exists (one node picked per clause, all mutually compatible)."""  # => co-25: closes reduce_3sat_to_clique's docstring above -- no runtime output, just sets its __doc__
    # => co-25: the two paragraphs above spell out the reduction's node/edge construction rule in prose
    nodes: dict[Node, int] = {}  # => co-25: node -> the literal value it represents
    for ci, clause in enumerate(clauses):  # => co-25: one node per (clause index, position) pair
        for pos, literal in enumerate(clause):  # => co-25: three positions per clause (3-SAT)
            nodes[(ci, pos)] = literal  # => co-25: records which literal this graph node stands for
    edges: set[tuple[Node, Node]] = set()  # => co-25: undirected edges, stored as (smaller, larger) tuples
    for (n1, lit1), (n2, lit2) in itertools.combinations(nodes.items(), 2):  # => co-25: every distinct node pair
        if n1[0] != n2[0] and literals_compatible(lit1, lit2):  # => co-25: DIFFERENT clauses AND not a negation pair
            edges.add((n1, n2))  # => co-25: an edge -- these two literals CAN be chosen together
    return edges, nodes  # => co-25: returns this computed value to the caller


def has_clique_of_size(edges: set[tuple[Node, Node]], nodes: list[Node], k: int) -> bool:  # => co-25: brute-force clique check
    """Brute-force: does any k-subset of `nodes` form a clique (every pair connected by an edge)?"""  # => co-25: documents has_clique_of_size's contract -- no runtime output, just sets its __doc__
    edge_lookup = edges | {(b, a) for a, b in edges}  # => co-25: a symmetric lookup set, both orderings present
    for subset in itertools.combinations(nodes, k):  # => co-25: every possible k-node subset, exhaustive
        if all((a, b) in edge_lookup for a, b in itertools.combinations(subset, 2)):  # => co-25: EVERY pair connected
            return True  # => co-25: found a genuine clique of size k
    return False  # => co-25: no k-subset was fully connected


if __name__ == "__main__":  # => co-25: entry point -- this block runs only when the file executes directly, not on import
    satisfiable_clauses: list[Clause] = [(1, 2, 3), (-1, 2, -3), (1, -2, 3)]  # => co-25: assignment 1=T,2=T,3=T satisfies all
    unsatisfiable_clauses: list[Clause] = [(1, 1, 1), (-1, -1, -1)]  # => co-25: x=T fails clause 2; x=F fails clause 1
    for label, clauses in [("satisfiable", satisfiable_clauses), ("unsatisfiable", unsatisfiable_clauses)]:  # => co-25
        edges, nodes = reduce_3sat_to_clique(clauses)  # => co-25: the reduction's graph, built mechanically
        clique_exists = has_clique_of_size(edges, list(nodes), k=len(clauses))  # => co-25: does a size-k clique exist?
        # independent, direct brute-force SAT check on the SAME instance -- confirms the reduction is FAITHFUL
        direct_sat = any(  # => co-25: True iff SOME assignment satisfies every clause, checked directly
            all(  # => co-25: every clause satisfied under this candidate assignment
                any((lit > 0) == bits[abs(lit) - 1] for lit in clause)  # => co-25: at least one literal True
                for clause in clauses  # => co-25: continues the statement started above
            )  # => co-25: closes the multi-line construct opened above
            for bits in itertools.product([False, True], repeat=3)  # => co-25: all 8 assignments over 3 variables
        )  # => co-25: closes the multi-line construct opened above
        print(f"{label}: clique of size {len(clauses)} exists = {clique_exists}, direct SAT check = {direct_sat}")  # => co-25: continues the statement started above
        assert clique_exists == direct_sat, f"the reduction must preserve satisfiability for the {label} instance"  # => co-25
    print(f"Clique existence matches direct satisfiability on both instances: True")  # => co-25: both cases agreed
    # => co-25: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
    # => co-25: has_clique_of_size is intentionally brute-force (itertools.combinations) -- the REDUCTION must be poly-time, not the clique search itself
