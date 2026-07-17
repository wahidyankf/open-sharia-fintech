"""Example 70: Logic Type-Inference Toy."""

from dataclasses import dataclass  # => @dataclass generates __init__ for each of the four term kinds below

Term = object  # => any of IntLit, BoolLit, Add, or If below


@dataclass(frozen=True)  # => a leaf term: an int literal
class IntLit:  # => frozen=True -- terms are immutable syntax, never mutated after construction
    value: int  # => the literal's own int value, unused by inference itself but part of the term shape


@dataclass(frozen=True)  # => a leaf term: a bool literal
class BoolLit:  # => frozen=True, same reasoning as IntLit above
    value: bool  # => the literal's own bool value


@dataclass(frozen=True)  # => a term built from two sub-terms -- typing this requires RULES, not just a lookup table
class Add:
    left: Term  # => the left operand -- itself any Term, so terms nest recursively
    right: Term  # => the right operand


@dataclass(frozen=True)  # => a conditional term: condition must be bool, both branches must share one type
class If:
    cond: Term  # => must infer to "bool" for this term to type-check
    then_branch: Term  # => the branch taken (at runtime) when cond is true
    else_branch: Term  # => must infer to the SAME type as then_branch


def infer_type(term: Term) -> str:  # => the type rules, expressed as a small set of logic-flavored clauses
    # => rule: IntLit  => "int"
    if isinstance(term, IntLit):  # => base case 1: an int literal always types as "int"
        return "int"  # => matches the rule above exactly
    # => rule: BoolLit => "bool"
    if isinstance(term, BoolLit):  # => base case 2: a bool literal always types as "bool"
        return "bool"  # => matches the rule above exactly
    # => rule: Add(L, R) => "int"  IF  type(L) == "int"  AND  type(R) == "int"
    if isinstance(term, Add):  # => recursive case: typing Add requires typing its two sub-terms first
        left_type = infer_type(term.left)  # => recursively infer the sub-term's type first
        right_type = infer_type(term.right)  # => and the other sub-term's type
        if left_type == "int" and right_type == "int":  # => the rule's premise, checked explicitly
            return "int"  # => the rule's conclusion, once the premise holds
        raise TypeError(f"Add requires two ints, got {left_type} and {right_type}")  # => the rule's premise failed
    # => rule: If(C, T, E) => type(T)  IF  type(C) == "bool"  AND  type(T) == type(E)
    if isinstance(term, If):  # => recursive case: typing If requires typing all three sub-terms
        cond_type = infer_type(term.cond)  # => recursively infer the condition's type
        then_type = infer_type(term.then_branch)  # => recursively infer the then-branch's type
        else_type = infer_type(term.else_branch)  # => recursively infer the else-branch's type
        if cond_type == "bool" and then_type == else_type:  # => the rule's premise, checked explicitly
            return then_type  # => the rule's conclusion -- the branches' shared type, once premise holds
        raise TypeError("If requires a bool condition and matching branch types")  # => the rule's premise failed
    raise TypeError(f"unknown term: {term!r}")  # => no rule matched -- an unrecognized term shape


expr = If(BoolLit(True), Add(IntLit(1), IntLit(2)), IntLit(0))  # => if true then (1+2) else 0
print(infer_type(expr))  # => the condition is bool, both branches infer to "int"
# => Output: int
