# A skill is named packaged procedure content.
skills = {"review": ("inspect", "summarize")}
# Loading selects the procedure only when needed.
procedure = skills["review"]
# The agent receives the declared reusable steps.
assert procedure == ("inspect", "summarize")
# Print the loaded skill.
print(procedure)
