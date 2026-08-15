#lang racket
;; Primary Scheme capstone: recursion, higher-order list work, and a hygienic control form.
(define (sum-positive values)
  (cond [(null? values) 0]
        [(positive? (car values)) (+ (car values) (sum-positive (cdr values)))]
        [else (sum-positive (cdr values))]))

(define-syntax unless
  (syntax-rules ()
    [(_ condition body ...)
     (if (not condition) (begin body ...) (void))]))

(define (increment-all values)
  (map add1 values))

(module+ main
  (displayln (sum-positive '(4 -2 6)))
  (displayln (increment-all '(1 2 3)))
  (unless #f (displayln "macro body ran")))
