#!/bin/sh
# ex-25: time_total covers DNS + connect + TLS + the full HTTP exchange
curl -o /dev/null -s -w "time_total=%{time_total}\n" https://example.com
