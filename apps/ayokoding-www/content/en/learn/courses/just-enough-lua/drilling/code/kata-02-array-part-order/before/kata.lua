local function build_receipt_buggy()
	local items = {}
	items["bread"] = 3
	items["milk"] = 2
	items["eggs"] = 4
	local total = 0
	for name, price in pairs(items) do
		print(name, price)
		total = total + price
	end
	print("total", total)
end

build_receipt_buggy()
