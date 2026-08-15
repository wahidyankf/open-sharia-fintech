---
title: "Learning Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Concepts

1. **co-01 · compiler-pipeline** — source becomes tokens, AST, checks, and output.
2. **co-02 · lexer-tokenizer** — lexers turn characters into tokens.
3. **co-03 · token-du** — tokens are explicit variants.
4. **co-04 · whitespace-comments** — trivia is skipped deliberately.
5. **co-05 · lexer-errors** — unexpected characters become diagnostics.
6. **co-06 · grammar** — grammar defines valid productions.
7. **co-07 · recursive-descent** — one parser function handles one rule.
8. **co-08 · ast-du** — AST variants model syntax shapes.
9. **co-09 · operator-precedence** — precedence determines tree shape.
10. **co-10 · pratt-parsing** — binding power guides expression parsing.
11. **co-11 · associativity** — equal-precedence operators choose grouping.
12. **co-12 · parser-combinators** — parsers compose as values.
13. **co-13 · fparsec-primitives** — primitives consume atomic syntax.
14. **co-14 · fparsec-sepby** — combinators parse delimited sequences.
15. **co-15 · parser-equivalence** — parsers should yield equivalent trees.
16. **co-16 · parse-errors** — errors state source position and expectation.
17. **co-17 · tree-walking-interpreter** — recursive evaluation walks an AST.
18. **co-18 · exhaustive-eval** — all AST variants receive evaluation.
19. **co-19 · environments-scopes** — environments hold bindings.
20. **co-20 · lexical-scope** — inner bindings shadow outer bindings.
21. **co-21 · semantic-analysis** — checks run after parsing.
22. **co-22 · name-resolution** — names resolve to bindings.
23. **co-23 · type-checking-pass** — invalid operand types are rejected.
24. **co-24 · ir** — intermediate representation separates front and back end.
25. **co-25 · code-generation** — a back end produces target syntax.
26. **co-26 · transpilation** — source can target another high-level language.
27. **co-27 · source-maps** — mappings preserve diagnostic origin.
28. **co-28 · optimization** — transformations preserve semantics.
29. **co-29 · test-corpus** — examples make language behavior executable.
30. **co-30 · diagnostic-quality** — helpful errors are a language feature.

Every ex-01 through ex-78 has a colocated F# artifact.
