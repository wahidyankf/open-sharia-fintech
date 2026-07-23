-- Example 3: nil vs false truthiness
if 0 then -- => 0 is truthy in Lua (unlike C, Python, or JavaScript)
	print("0 is truthy") -- => Output line 1: 0 is truthy
end -- => closes the first if
if "" then -- => "" (empty string) is truthy too
	print("empty string is truthy") -- => Output line 2: empty string is truthy
end -- => closes the second if; only nil/false ever skip a branch
