CC ?= cc
CFLAGS ?= -std=c17 -Wall -Wextra -pedantic

inventory: main.o inventory.o
	$(CC) $(CFLAGS) $^ -o $@

main.o: main.c item.h
inventory.o: inventory.c item.h

clean:
	rm -f inventory main.o inventory.o

.PHONY: clean
