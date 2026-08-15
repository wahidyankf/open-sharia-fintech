example: main.o add.o
	$(CC) $^ -o $@

CC ?= cc
CFLAGS ?= -std=c17 -Wall -Wextra -pedantic
main.o: example.c
	$(CC) $(CFLAGS) -c $< -o $@
add.o: add.c
	$(CC) $(CFLAGS) -c $< -o $@
