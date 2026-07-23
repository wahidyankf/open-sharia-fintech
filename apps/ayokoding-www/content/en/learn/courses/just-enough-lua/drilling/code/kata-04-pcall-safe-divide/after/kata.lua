local function divide(a, b)
	if b == 0 then
		error({ code = "DIV_ZERO", message = "cannot divide " .. a .. " by zero" })
	end
	return a / b
end

local function safe_divide(a, b)
	local ok, result = pcall(divide, a, b)
	if ok then
		return result, nil
	else
		return nil, result
	end
end

local r1, err1 = safe_divide(10, 2)
print(r1, err1)

local r2, err2 = safe_divide(10, 0)
print(r2, err2 and err2.message)
