-- Example 14: if/elseif/else branching -- a grade classifier
local function grade(score) -- => defines a local function taking one parameter
	if score >= 90 then -- => first condition checked top to bottom
		return "A" -- => returned only when score >= 90
	elseif score >= 80 then -- => only checked if the first condition was false
		return "B" -- => returned only when 80 <= score < 90
	elseif score >= 70 then -- => only checked if both prior conditions were false
		return "C" -- => returned only when 70 <= score < 80
	else -- => catch-all when no condition matched
		return "F" -- => returned for any score below 70
	end -- => closes the if/elseif/else chain
end -- => closes the function
print(grade(85)) -- => 85 >= 90 is false, 85 >= 80 is true -- returns "B"
-- => Output: B
