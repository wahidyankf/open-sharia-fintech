#!/bin/sh
# ex-49: -w extracts just the status code; -o /dev/null discards the body entirely
for code in 200 301 404 500; do                                      # => one representative from each of HTTP's four status classes
	curl -s -o /dev/null -w "%{http_code}\n" "https://mock.codes/$code" # => prints just the code
done                                                                 # => loop runs exactly four times, once per class
