# The application needs the compiled object.
app: main.o
	$(CC) $< -o $@

# The object needs the source before it can be compiled.
main.o: main.c
	$(CC) -c $< -o $@
