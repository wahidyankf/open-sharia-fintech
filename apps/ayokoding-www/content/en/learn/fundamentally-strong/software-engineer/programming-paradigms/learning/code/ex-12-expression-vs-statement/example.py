"""Example 12: Expression vs Statement."""


def classify_via_statement(n: int) -> str:  # => the STATEMENT form: if/assign, several steps
    if n >= 0:  # => statement #1: a branch that does not itself produce a value
        label = "non-negative"  # => statement #2: assignment, a separate step from the branch
    else:  # => statement #1's else-arm
        label = "negative"  # => statement #2's else-arm
    return label  # => statement #3: a THIRD step to hand the accumulated value back


def classify_via_expression(n: int) -> str:  # => the EXPRESSION form: one value-producing expression
    return "non-negative" if n >= 0 else "negative"  # => the conditional IS the value, no named box


for n in (5, -5, 0):  # => try a spread of representative inputs
    stmt = classify_via_statement(n)  # => run the statement-based version
    expr = classify_via_expression(n)  # => run the expression-based version
    print(stmt == expr, expr)  # => both must compute the identical string for every input
# => Output: True non-negative
# => Output: True negative
# => Output: True non-negative
