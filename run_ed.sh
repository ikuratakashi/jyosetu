#!/bin/bash
echo "-------------------------------------"
echo "プロセス終了実行"
echo "-------------------------------------"
if [ -f ./tmp/websocket.pid ]; then
    sudo kill -9 $(cat ./tmp/websocket.pid)
fi

#if [ -f ./tmp/rs232c.pid ]; then
#    kill -9 $(cat ./tmp/rs232c.pid)
#fi

if [ -f ./tmp/www.pid ]; then
    sudo kill -9 $(cat ./tmp/www.pid)
fi

echo ""
echo "※プロセス終了できなかった場合"
echo "（実行中のプロセスを以下に表示）"

ps -ef | grep -E 'sv\.py|rs232c\.py|www\.py|momo'

echo ""
echo "（上記に何も表示されなかった場合はプロセスは起動していません。）"
echo "最初の方の番号がプロセスIDです（-9は強制終了のパラメタです）"
echo "sudo kill -9 <プロセスID> のコマンドで手動削除してください。"
echo "例）sudo kill -9 1234"
