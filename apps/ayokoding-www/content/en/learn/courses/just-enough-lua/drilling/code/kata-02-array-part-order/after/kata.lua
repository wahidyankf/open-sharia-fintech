local function build_receipt()
	local items = {
		{ name = "bread", price = 3 },
		{ name = "milk", price = 2 },
		{ name = "eggs", price = 4 },
	}
	local total = 0
	for _, item in ipairs(items) do
		print(item.name, item.price)
		total = total + item.price
	end
	print("total", total)
end

build_receipt()
