"""Example 47: Offloading CPU Bound Work to a Process Pool.

A genuinely CPU-bound function offloaded to a ProcessPoolExecutor so it runs in a SEPARATE process, in parallel
-- the event loop stays responsive, and the GIL of the main process is not held. Run: python3 example.py. (co-03, co-06)
"""

import asyncio  # => the event loop (co-02)
from concurrent.futures import ProcessPoolExecutor  # => true parallelism for CPU work (co-03)


def cpu_heavy(n: int) -> int:  # => a CPU-bound function -- GIL-bound if run on the loop's thread
    total = 0  # => accumulator
    for i in range(n):  # => a tight CPU loop
        total += i * i % 7  # => meaningless arithmetic that burns CPU
    return total  # => the result


async def main() -> int:  # => offloads the CPU work so the loop never stalls
    loop = asyncio.get_running_loop()  # => the running loop
    # => a ProcessPoolExecutor runs the function in SEPARATE processes -- real parallelism for CPU work (co-03)
    with ProcessPoolExecutor() as pool:  # => a pool of worker processes
        # => run_in_executor(offloader) keeps the loop responsive while the CPU work proceeds elsewhere (co-06)
        result = await loop.run_in_executor(pool, cpu_heavy, 1_000_000)  # => resolves to the int
    return result  # => the CPU-bound result, with the loop never blocked


if __name__ == "__main__":  # => only runs when executed directly
    out = asyncio.run(main())  # => drive the async main
    print(out)  # => Output: the computed total (loop stayed responsive throughout)
