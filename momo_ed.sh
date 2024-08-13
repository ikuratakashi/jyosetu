#!/bin/bash
if [ -f /tmp/momo.pid ]; then
    kill -9 $(cat /tmp/momo.pid)
    rm /tmp/momo.pid
else
    echo "PID file not found. Is momo running?"
fi