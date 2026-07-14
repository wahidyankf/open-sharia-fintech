#!/bin/sh
# ex-79: three separate timing variables, extracted from one real request
curl -o /dev/null -s -w "dns=%{time_namelookup} connect=%{time_connect} total=%{time_total}\n" https://example.com
