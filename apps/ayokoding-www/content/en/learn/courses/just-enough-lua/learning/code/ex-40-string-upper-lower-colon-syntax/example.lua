-- Example 40: string.upper/lower via colon syntax
print(("Neovim"):upper(), ("Neovim"):lower())
-- => colon-call sugar for string.upper("Neovim")/string.lower("Neovim")
-- => Output: NEOVIM    neovim
