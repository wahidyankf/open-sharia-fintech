"""Example 49: try/except/else/finally."""

# else runs only when try raises nothing; finally always runs, success or failure.
try:  # => runs the block below; no exception occurs in this example
    print("try")  # => runs first -- Output line 1: try
except ValueError:  # => would run only if try raised a ValueError
    print("except")  # => skipped -- no exception was raised
else:  # => runs only when try completes with NO exception
    print("else")  # => runs ONLY if try raised nothing -- Output line 2: else
finally:  # => runs unconditionally, whether try succeeded or an exception fired
    print("finally")  # => ALWAYS runs, exception or not -- Output line 3: finally
