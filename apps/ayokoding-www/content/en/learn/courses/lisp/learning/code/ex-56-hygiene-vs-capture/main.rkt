#lang racket
;; ex-56 · hygiene-vs-capture — original Scheme-first instructional artifact.
(define values '(1 2 3))
(displayln (map add1 values))
