local Shape = {}
Shape.__index = Shape
function Shape.new(name)
	return setmetatable({ name = name }, Shape)
end
function Shape:describe()
	return self.name .. " is a shape"
end

local Circle = setmetatable({}, { __index = Shape })
function Circle.new(radius)
	return setmetatable({ name = "circle", radius = radius }, Circle)
end

local c = Circle.new(5)
print(c:describe())
