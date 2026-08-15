#lang racket
;; ex-39 · syntax-rules-swap
(define-syntax swap!
  (syntax-rules () [(_ a b) (let ([saved a]) (set! a b) (set! b saved))]))
