# pyright: strict
"""Example 48: nDCG Compute (co-24)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def dcg(
    graded_relevances: list[float],
) -> (
    float
):  # => discounted Cumulative Gain: sum of rel_i / log2(i + 1), i is the 1-based rank
    """Discounted Cumulative Gain: sum of rel_i / log2(i + 1), i is the 1-based rank."""
    return sum(
        rel / math.log2(i + 1) for i, rel in enumerate(graded_relevances, start=1)
    )  # => co-24: later ranks discounted MORE


def ndcg(
    ranked_relevances: list[float], ideal_relevances: list[float]
) -> float:  # => nDCG@len: DCG of the actual ranking, normalized by the IDEAL (best-possible) ranking's DCG
    """nDCG@len: DCG of the actual ranking, normalized by the IDEAL (best-possible) ranking's DCG."""
    ideal_dcg: float = dcg(
        sorted(ideal_relevances, reverse=True)
    )  # => co-24: the best possible ordering of these SAME grades
    if ideal_dcg == 0:  # => true when ideal_dcg == 0
        return 0.0  # => returns 0.0
    return (
        dcg(ranked_relevances) / ideal_dcg
    )  # => co-24: normalized so a perfect ranking scores exactly 1.0


def main() -> None:  # => defines main
    grades: dict[int, float] = {
        1: 3.0,
        2: 2.0,
        3: 1.0,
        4: 0.0,
    }  # => graded relevance, 3=highly relevant, 0=irrelevant

    perfect_ranking: list[int] = [1, 2, 3, 4]  # => best grade first -- the IDEAL order
    shuffled_ranking: list[int] = [
        4,
        1,
        3,
        2,
    ]  # => worst grade FIRST -- a genuinely bad order

    perfect_relevances: list[float] = [
        grades[d] for d in perfect_ranking
    ]  # => perfect relevances = [grades[d] for d in perfect_ranking]
    shuffled_relevances: list[float] = [
        grades[d] for d in shuffled_ranking
    ]  # => shuffled relevances = [grades[d] for d in shuffled_ranking]
    ideal_relevances: list[float] = list(
        grades.values()
    )  # => the SAME grades, any order (sorted internally by dcg)

    ndcg_perfect: float = ndcg(
        perfect_relevances, ideal_relevances
    )  # => co-24: the perfect ranking's nDCG
    ndcg_shuffled: float = ndcg(
        shuffled_relevances, ideal_relevances
    )  # => co-24: the shuffled ranking's nDCG
    print(
        f"perfect ranking {perfect_ranking}: nDCG={ndcg_perfect:.6f}"
    )  # => shows perfect ranking
    print(
        f"shuffled ranking {shuffled_ranking}: nDCG={ndcg_shuffled:.6f}"
    )  # => shows shuffled ranking

    assert math.isclose(ndcg_perfect, 1.0, abs_tol=1e-9), (
        "a PERFECT ranking must score nDCG == 1.0 exactly"
    )  # => a PERFECT ranking must score nDCG == 1.0 exactly
    assert ndcg_shuffled < ndcg_perfect, (
        "a SHUFFLED (worse) ranking must score strictly LESS than the perfect one"
    )  # => a SHUFFLED (worse) ranking must score strictly LESS than the perfect one
    print(
        f"MATCH: the perfect ranking scores exactly {ndcg_perfect}, the shuffled ranking scores less ({ndcg_shuffled:.6f})"
    )  # => shows MATCH: the perfect ranking scores exactly


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
