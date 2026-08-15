---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**Why have a token DU?**

<details><summary>Answer</summary>It gives parser code a closed set of input shapes and makes an
unhandled token visible.</details>

**Why is an AST different from source text?**

<details><summary>Answer</summary>An AST preserves syntactic structure and precedence without
requiring later phases to reparse characters.</details>

## Calculation practice

Tokenize 2 + 3 \* 4, then draw the AST whose multiplication child sits under addition.

## Scenario judgment

Report an unknown character at the lexer. Do not continue as though it were whitespace; later
errors become misleading.

## Design exercise

Define a tiny expression grammar, parse a name binding and arithmetic expression, type-check it,
then evaluate it through an environment.

## Automaticity checklist

- [ ] I can state a pipeline phase and its input/output.
- [ ] I can explain precedence with a tree.
- [ ] I can make an AST match exhaustive.
- [ ] I can distinguish parsing from semantic analysis.
- [ ] I can write an error with source context.

## Why / why not prompts

- Why not evaluate raw source text directly?
- Why not encode every token as a string?
- Why not handle an unknown name as zero?
- Why not optimize before the interpreter is correct?
- Why are tests a language specification aid?
