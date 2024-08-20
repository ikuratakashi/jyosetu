#!/bin/bash
./momo --data-channel --no-audio-device test &
echo プロセスID：$!
echo $! > /tmp/momo.pid
