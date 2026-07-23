#!/bin/sh
# ex-50a: read the claimed Content-Length from the headers
curl -sI --http1.1 https://info.cern.ch | grep -i content-length

# ex-50b: independently count the real body's bytes
curl -s --http1.1 https://info.cern.ch | wc -c
