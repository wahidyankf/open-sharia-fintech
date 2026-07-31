# Expansion timing

| Operator | Value is expanded            |
| -------- | ---------------------------- |
| `=`      | when the variable is used    |
| `:=`     | when the variable is defined |

Use `=` when a later value must remain visible; use `:=` when a derived value must stay fixed.
