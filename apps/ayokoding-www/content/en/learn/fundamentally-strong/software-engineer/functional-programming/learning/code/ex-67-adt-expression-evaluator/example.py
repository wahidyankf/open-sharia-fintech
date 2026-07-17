"""Example 67: An Expression AST as an ADT With a match Evaluator."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Expr' forward references below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds each AST node variant


@dataclass(frozen=True)  # => a leaf node: a literal number
class Num:  # => the class body begins here
    value: float  # => the literal's own value


@dataclass(frozen=True)  # => a branch node: left + right
class Add:  # => the class body begins here
    left: "Expr"  # => the left operand, itself an Expr
    right: "Expr"  # => the right operand, itself an Expr


@dataclass(frozen=True)  # => a branch node: left * right
class Mul:  # => the class body begins here
    left: "Expr"  # => the left operand, itself an Expr
    right: "Expr"  # => the right operand, itself an Expr


Expr = (
    Num | Add | Mul
)  # => the ADT: any expression is EXACTLY one of these three shapes


def evaluate(
    expr: Expr,
) -> float:  # => match/case walks the AST, one branch per variant
    match expr:  # => opens the match/case block over expr
        case Num(value=v):  # => a leaf -- just return its value
            return v  # => the leaf's own value
        case Add(left=l, right=r):  # => recurse into both children, then add
            return evaluate(l) + evaluate(r)  # => the actual addition Add represents
        case Mul(left=l, right=r):  # => recurse into both children, then multiply
            return evaluate(l) * evaluate(
                r
            )  # => the actual multiplication Mul represents


expression = Add(Num(2.0), Mul(Num(3.0), Num(4.0)))  # => represents "2.0 + (3.0 * 4.0)"

# => an interpreter is the canonical use case for ADTs plus match/case together
print(evaluate(expression))  # => Output: 14.0
