# all composes independent JavaScript and native file artifacts.
.PHONY: all js clean
all: js native-app

js: dist.txt

dist.txt: package.json build.mjs
	npm run build

native-app: native.o
	$(CC) $< -o $@

native.o: native.c
	$(CC) -c $< -o $@

clean:
	rm -f dist.txt native.o native-app
