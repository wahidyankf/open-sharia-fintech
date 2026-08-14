prompt = "Summarize: {text}"  # => framework-style prompt template primitive
assert (
    prompt.format(text="facts") == "Summarize: facts"
)  # => composition remains testable
print("PASS: langchain-abstraction")  # => offline acceptance result
