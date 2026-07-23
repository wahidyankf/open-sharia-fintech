local function parse_line(line)
	return line:match("(%a+):(%a+)")
end

print(parse_line("theme: dark"))
