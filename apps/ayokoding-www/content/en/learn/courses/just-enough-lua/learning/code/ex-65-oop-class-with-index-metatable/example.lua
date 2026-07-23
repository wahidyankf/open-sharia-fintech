-- Example 65: OOP -- a class built from __index
local Animal = {} -- => the class table
Animal.__index = Animal -- => Animal doubles as its own instances' metatable
function Animal.new(name) -- => the constructor: builds a plain table, tags it with Animal
	return setmetatable({ name = name }, Animal) -- => setmetatable returns the same table it was given
end -- => closes the constructor
function Animal:speak() -- => colon syntax: sugar for `function Animal.speak(self)`
	return self.name .. " makes a sound"
end -- => closes the method
print(Animal.new("Rex"):speak()) -- => builds an instance, then :speak() looks up speak via __index
-- => Output: Rex makes a sound
