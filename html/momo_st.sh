#!/bin/bash
./momo --no-audio-device test &
echo プロセスID：$!
echo $! > /tmp/momo.pid
echo server http://$(python ipshow.py):8080/html/test.html
