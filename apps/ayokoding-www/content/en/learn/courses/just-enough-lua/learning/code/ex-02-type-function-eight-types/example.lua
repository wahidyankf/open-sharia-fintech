-- Example 2: type() on Lua's eight basic types
print(type(nil), type(true), type(1), type("s"), type({}), type(print))
-- => six type() calls: nil/boolean/number/string/table/function
-- => Output: nil    boolean    number    string    table    function
