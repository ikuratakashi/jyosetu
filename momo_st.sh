#!/bin/bash
./momo --no-audio-device test &
echo プロセスID：$!
echo $! > /tmp/momo.pid
