-- Example 37: string.format -- float width and precision
print(string.format("%5.2f", 3.14159))
-- => %5.2f: total field width 5, 2 decimal digits -- rounds to "3.14", padded
-- => Output:  3.14  (one leading space, then 3.14)
