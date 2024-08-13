#!/bin/bash
if [ -f /tmp/momo.pid ]; then
    kill -9 $(cat /tmp/momo.pid)
    rm /tmp/momo.pid
else
    echo "PID file not found. Is momo running?"

    ps -ef | grep momo
    
    echo "最初の方の番号がプロセスIDです。"
    echo "sudo kill プロセスID のコマンドで手動削除してください。"

fi