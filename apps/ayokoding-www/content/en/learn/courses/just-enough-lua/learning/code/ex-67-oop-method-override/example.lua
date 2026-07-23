-- Example 67: OOP -- overriding an inherited method
local Animal = {} -- => base class table
Animal.__index = Animal -- => Animal is its own instances' metatable
function Animal.new(name)
	return setmetatable({ name = name }, Animal)
end -- => base constructor
function Animal:speak()
	return self.name .. " makes a sound"
end -- => base method

local Dog = setmetatable({}, { __index = Animal }) -- => Dog falls back to Animal for anything undefined
Dog.__index = Dog -- => Dog is also its own instances' metatable
function Dog.new(name)
	return setmetatable({ name = name }, Dog)
end -- => Dog constructor
function Dog:speak() -- => defining speak directly on Dog shadows Animal's version
	return self.name .. " barks"
end -- => closes the override

local a = Animal.new("Rex") -- => a plain Animal instance
local d = Dog.new("Fido") -- => a Dog instance
print(a:speak()) -- => a is unaffected by Dog's override -- Output: Rex makes a sound
print(d:speak()) -- => d finds speak on Dog before the lookup reaches Animal
-- => Output: Fido barks
