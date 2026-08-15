raw, stop = "answer<END>ignored", "<END>"  # => generated text and sentinel
answer = raw.split(stop, maxsplit=1)[0]  # => output terminates at the stop sequence
assert answer == "answer"  # => trailing text is excluded
print("PASS: stop-sequences")  # => offline acceptance result
