# app links both object files; an edit rebuilds its dependent object and app.
app: main.o greeting.o
	$(CC) $^ -o $@

%.o: %.c
	$(CC) -c $< -o $@

.PHONY: clean
clean:
	rm -f app main.o greeting.o
