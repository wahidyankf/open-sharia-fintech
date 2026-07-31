# api.txt and web.txt are independent and may run in parallel.
.PHONY: all
all: api.txt web.txt

api.txt:
	printf 'api built\\n' > $@

web.txt:
	printf 'web built\\n' > $@
