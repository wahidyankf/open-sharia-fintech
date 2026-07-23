-- A minimal module: it RETURNS a table, which is the whole contract of a Lua module
return {
	greet = function()
		return "hi"
	end, -- => one function field, exposed to callers of require()
}
