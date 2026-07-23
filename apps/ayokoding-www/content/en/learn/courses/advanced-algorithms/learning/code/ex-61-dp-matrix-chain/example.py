"""Example 61: Matrix-Chain Multiplication Order -- 2D Interval DP."""

# dp[i][j] = min scalar multiplications to multiply matrices i..j (co-24):
# try EVERY possible split point k, combining the cost of the two resulting
# sub-chains plus the cost of that final multiplication -- an interval DP,
# indexed by chain LENGTH rather than by a simple linear position.
INF = float("inf")  # => sentinel for "not yet computed / impossible"


def matrix_chain_min_cost(  # => tries every split point, keeps the cheapest for each interval
    dims: list[int],  # => n+1 dimension entries describing n matrices
) -> int:  # => dims has n+1 entries for n matrices; matrix i is dims[i-1] x dims[i]
    n = len(dims) - 1  # => number of matrices in the chain
    dp: list[list[float]] = [  # => opens the 2D table construction
        [0.0] * (n + 1)
        for _ in range(n + 1)  # => one fresh row of zeros per matrix index
    ]  # => dp[i][j] = min cost to multiply matrices i..j (1-indexed)
    for chain_len in range(2, n + 1):  # => builds by INCREASING chain length, 2 up to n
        for i in range(1, n - chain_len + 2):  # => every valid starting matrix index
            j = i + chain_len - 1  # => the ending matrix index for this chain length
            dp[i][j] = INF  # => starts as "no split tried yet"
            for k in range(i, j):  # => tries every possible SPLIT POINT k
                cost = (  # => opens the split-cost computation
                    dp[i][k]
                    + dp[k + 1][j]
                    + dims[i - 1] * dims[k] * dims[j]  # => split cost
                )  # => left sub-chain + right sub-chain + this final multiplication
                dp[i][j] = min(dp[i][j], cost)  # => keeps the cheapest split found
    return int(dp[1][n])  # => the minimum cost to multiply the ENTIRE chain


dims: list[int] = [  # => opens the classic CLRS dimension list
    30,  # => p0
    35,  # => p1
    15,  # => p2
    5,  # => p3
    10,  # => p4
    20,  # => p5
    25,  # => p6
]  # => the classic CLRS example: 6 matrices, dims p0..p6
min_cost = matrix_chain_min_cost(dims)  # => the minimum possible scalar-multiply count
print(min_cost)  # => Output: 15125

assert min_cost == 15125  # => confirms the well-known CLRS answer for this chain
assert matrix_chain_min_cost([10, 20]) == 0  # => a single matrix needs zero multiplies
assert matrix_chain_min_cost([10, 20, 30]) == 6000  # => two matrices: only one way
print("ex-61 OK")  # => Output: ex-61 OK
