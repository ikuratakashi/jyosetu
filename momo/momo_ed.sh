#!/bin/bash
if [ -f /tmp/momo.pid ]; then
    kill -9 $(cat /tmp/momo.pid)
    rm /tmp/momo.pid

    echo ""
    echo "※プロセス終了できなかった場合"
    echo ""

    ps -ef | grep momo
    
    echo ""
    echo "最初の方の番号がプロセスIDです。"
    echo "sudo kill -9 <プロセスID> のコマンドで手動削除してください。"
    echo "例）sudo kill -9 1234"

else
    echo "PID file not found. Is momo running?"
    echo ""

    ps -ef | grep momo
    
    echo ""
    echo "最初の方の番号がプロセスIDです。"
    echo "sudo kill -9 <プロセスID> のコマンドで手動削除してください。"
    echo "例）sudo kill -9 1234"

fi