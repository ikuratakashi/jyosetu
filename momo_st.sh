#!/bin/bash
./momo --no-audio-device test &
echo $! > /tmp/momo.pid
