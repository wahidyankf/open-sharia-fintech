def grade(score: int) -> str:  # => co-27: three branches -- only TWO are exercised by the test below  # fmt: skip
    if score >= 90:  # => branch A  # fmt: skip
        return "A"  # => reached only when branch A's condition is true  # fmt: skip
    if score >= 70:  # => branch B  # fmt: skip
        return "B"  # => reached only when branch B's condition is true  # fmt: skip
    return "C"  # => branch C -- deliberately LEFT UNCOVERED, to give the report something to show  # fmt: skip
