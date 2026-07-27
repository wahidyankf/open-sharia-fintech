# pyright: strict
"""Example 77: PageRank Toy (co-36)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def pagerank(
    links: dict[str, list[str]], damping: float = 0.85, iterations: int = 100
) -> dict[
    str, float
]:  # => power-iteration PageRank, Brin & Page (1998)'s own random-surfer formulation
    """Power-iteration PageRank, Brin & Page (1998)'s own random-surfer formulation."""
    nodes: list[str] = list(links)  # => co-36: every node in the graph
    n: int = len(nodes)  # => this fixture's own size
    scores: dict[str, float] = {
        node: 1.0 / n for node in nodes
    }  # => co-36: uniform starting distribution

    for _ in range(
        iterations
    ):  # => co-36: repeated power-iteration steps, toward convergence
        new_scores: dict[str, float] = {
            node: (1 - damping) / n for node in nodes
        }  # => the random-jump base term
        for node, outlinks in links.items():  # => iterates one item at a time
            if not outlinks:  # => co-36: a DANGLING node -- redistribute its mass to ALL nodes, or the total leaks below 1
                for target in nodes:  # => iterates one item at a time
                    new_scores[target] += (
                        damping * scores[node] / n
                    )  # => part of this step's computation, continued from the line above
                continue  # => part of this step's computation, continued from the line above
            share: float = scores[node] / len(
                outlinks
            )  # => co-36: this node's rank, split evenly among its outlinks
            for target in outlinks:  # => iterates one item at a time
                new_scores[target] += (
                    damping * share
                )  # => co-36: each linked-to node receives its share
        scores = new_scores  # => scores = new_scores
    return scores  # => returns scores


def main() -> None:  # => defines main
    links: dict[
        str, list[str]
    ] = {  # => co-36: A and B and D all point to C -- C should dominate
        "A": ["B", "C"],  # => entry for 'A'
        "B": ["C"],  # => entry for 'B'
        "C": [],  # => entry for 'C'
        "D": ["C"],  # => entry for 'D'
    }  # => opens/closes this multi-line literal
    scores: dict[str, float] = pagerank(
        links
    )  # => co-36: the converged PageRank distribution
    for node, score in sorted(
        scores.items(), key=lambda kv: -kv[1]
    ):  # => iterates one item at a time
        print(f"{node}: {score:.4f}")  # => prints this step's result

    total: float = sum(
        scores.values()
    )  # => co-36: PageRank's own probability-distribution invariant
    top_node: str = max(
        scores, key=lambda n: scores[n]
    )  # => whichever node scored highest
    print(f"sum of scores: {total:.6f}")  # => shows sum of scores

    assert abs(total - 1.0) < 1e-6, (
        "PageRank scores must sum to (approximately) 1.0 -- it's a probability distribution"
    )  # => PageRank scores must sum to (approximately) 1.0 -- it's a probability distribution
    assert top_node == "C", (
        "'C' is linked to by EVERY other node -- it must rank highest"
    )  # => 'C' is linked to by EVERY other node -- it must rank highest
    print(
        f"MATCH: scores sum to {total:.6f} and the most-linked node 'C' ranks highest, as PageRank's own theory predicts"
    )  # => shows MATCH: scores sum to


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
