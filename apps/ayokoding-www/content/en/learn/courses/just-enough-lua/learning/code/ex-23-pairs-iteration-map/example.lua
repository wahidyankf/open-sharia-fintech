-- Example 23: pairs() iteration over all keys
for k, v in pairs({ a = 1, b = 2 }) do
	-- => pairs walks EVERY key (array part and hash part), order unspecified
	print(k, v) -- => k is the key, v is the value
end
-- => Output: both "a    1" and "b    2" print, one per line
-- => the ORDER between them varies run to run -- pairs() gives no ordering guarantee
