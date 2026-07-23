-- Example 74: an anchored pattern with three captures -- parsing a date
print(string.match("2026-07-12", "^(%d+)-(%d+)-(%d+)$"))
-- => ^ and $ anchor the match to the whole string; %d+ matches digit runs
-- => Output: 2026    07    12
