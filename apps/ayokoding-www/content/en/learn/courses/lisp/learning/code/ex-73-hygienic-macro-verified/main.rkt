#lang racket
;; ex-73 · hygienic-macro-verified — original Scheme-first instructional artifact.
(define values '(1 2 3))
(displayln (map add1 values))
