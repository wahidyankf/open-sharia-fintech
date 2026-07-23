-- Example 43: string.match -- pattern captures
print(string.match("key=value", "(%w+)=(%w+)"))
-- => %w+ matches alphanumerics; each (...) is a CAPTURE returned separately
-- => Output: key    value
