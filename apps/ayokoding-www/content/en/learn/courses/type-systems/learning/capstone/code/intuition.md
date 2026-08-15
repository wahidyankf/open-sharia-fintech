# Concrete map and bind intuition

A functor map changes the successful value while preserving the surrounding Result shape. Bind
uses a function that itself may fail, avoiding Result nested inside Result. In the email domain,
map can format a verified address; bind would chain parsing with another validation step. The
abstraction is useful only because the surrounding code already makes success and error shapes
visible.

This explanation is informed by Milewski's CC BY-SA _Category Theory for Programmers_, but the
domain code and prose here are original.
