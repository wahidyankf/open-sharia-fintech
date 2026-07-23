#!/bin/sh
# Example 42: nc -l -- Listen and Show the Raw Bytes curl Actually Sends.
# nc -l opens a raw, passive TCP socket -- co-21: nc as a hand connection-inspection tool.
# Whatever the OTHER side sends arrives on nc's own stdout, byte for byte, no parsing at all.
nc -l 50042
