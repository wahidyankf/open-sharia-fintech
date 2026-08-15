---
title: "Learning Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Concepts

1. **co-01 · static-vs-dynamic** — static checks reject shape errors before running.
2. **co-02 · sum-types** — a value has one named variant.
3. **co-03 · product-types** — a value has several fields.
4. **co-04 · algebraic-data-types** — sums of products model domains.
5. **co-05 · illegal-states-unrepresentable** — type construction excludes invalid forms.
6. **co-06 · pattern-matching** — match deconstructs variants.
7. **co-07 · exhaustiveness-checking** — missing variants are compiler-visible.
8. **co-08 · parametric-polymorphism** — generic code works for all types.
9. **co-09 · hindley-milner-inference** — principal types are inferred.
10. **co-10 · type-annotations** — ascriptions constrain or clarify inference.
11. **co-11 · unit-and-bottom** — unit has one value; bottom has none.
12. **co-12 · option-type** — Option/Maybe makes absence explicit.
13. **co-13 · result-type** — Result/Either makes failure explicit.
14. **co-14 · recursive-types** — self-reference models nested data.
15. **co-15 · type-aliases** — aliases name an existing type.
16. **co-16 · typeclasses** — constrained ad-hoc polymorphism.
17. **co-17 · typeclass-instances** — types supply class behavior.
18. **co-18 · modules-functors** — modules compose through module parameters.
19. **co-19 · signatures** — signatures define module interfaces.
20. **co-20 · higher-kinded-types** — abstraction ranges over constructors.
21. **co-21 · functor** — map preserves a structure's shape.
22. **co-22 · applicative** — wrapped functions apply to wrapped values.
23. **co-23 · monad** — bind sequences dependent computation.
24. **co-24 · monad-laws** — lawful bind obeys identity and association.
25. **co-25 · map-bind-pipeline** — total pipelines compose explicit effects.
26. **co-26 · fsharp-adts** — F# offers matching ADTs on .NET.
27. **co-27 · soundness** — sound typing contrasts TypeScript's deliberate unsoundness.
28. **co-28 · type-variance** — subtyping direction depends on consumption/production.
29. **co-29 · phantom-types** — a parameter can carry only compile-time information.
30. **co-30 · newtype-wrapper** — a wrapper gives a representation distinct meaning.

All 78 examples have artifacts under [learning/code](./code/README.md).
