#!/bin/sh
# ex-21: -L follows every redirect; -I keeps each hop to headers-only
curl -IL --http1.1 http://go.dev
