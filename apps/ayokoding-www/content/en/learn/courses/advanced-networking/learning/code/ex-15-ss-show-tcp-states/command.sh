#!/bin/sh
# ex-15: ss -tan lists every TCP socket's current state -- run once WHILE a
# connection is open (ESTAB), then again shortly after it closes, to watch
# the state transition described by co-07's state machine
curl -s -o /dev/null https://example.com &
sleep 0.05
echo "--- while open (ESTAB) ---"
ss -tan | grep -i estab
wait
sleep 1
echo "--- after close ---"
ss -tan | grep -E 'State|:443'
