-- Example 66: OOP -- an inheritance chain via setmetatable
local Animal = {} -- => base class table
Animal.__index = Animal -- => Animal is its own instances' metatable
function Animal.new(name)
	return setmetatable({ name = name }, Animal)
end -- => base constructor
function Animal:speak()
	return self.name .. " makes a sound"
end -- => base method

local Dog = setmetatable({}, { __index = Animal }) -- => Dog's failed lookups fall through to Animal
Dog.__index = Dog -- => Dog is also its own instances' metatable, exactly like Animal
function Dog.new(name)
	return setmetatable({ name = name }, Dog)
end -- => Dog constructor

local d = Dog.new("Fido") -- => builds a Dog instance
print(d:speak()) -- => Dog has no speak of its own, so the lookup chains: Dog -> Animal
-- => Output: Fido makes a sound
