local function parse_line(line)
	return line:match("(%a+):%s*(%a+)")
end

print(parse_line("theme: dark"))
print(parse_line("mode:fast"))
