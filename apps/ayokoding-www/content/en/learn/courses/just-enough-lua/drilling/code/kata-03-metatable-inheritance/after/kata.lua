local Shape = {}
Shape.__index = Shape
function Shape.new(name)
	return setmetatable({ name = name }, Shape)
end
function Shape:describe()
	return self.name .. " is a shape"
end

local Circle = setmetatable({}, { __index = Shape })
Circle.__index = Circle
function Circle.new(radius)
	return setmetatable({ name = "circle", radius = radius }, Circle)
end
function Circle:area()
	return math.floor(3.14159 * self.radius * self.radius)
end

local c = Circle.new(5)
print(c:describe())
print(c:area())
