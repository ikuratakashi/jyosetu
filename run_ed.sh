#!/bin/bash
echo "-------------------------------------"
echo "プロセス終了実行"
echo "-------------------------------------"
if [ -f ./tmp/websocket.pid ]; then
    kill -9 $(cat ./tmp/websocket.pid)
fi

#if [ -f ./tmp/rs232c.pid ]; then
#    kill -9 $(cat ./tmp/rs232c.pid)
#fi

if [ -f ./tmp/www.pid ]; then
    kill -9 $(cat ./tmp/www.pid)
fi

echo ""
echo "上記に何も表示されなければ、プロセスは終了しました。"
echo ""
echo ""
echo "※プロセス終了できなかった場合"

ps -ef | grep -E 'sv\.py|rs232c\.py|www\.py'

echo ""
echo "最初の方の番号がプロセスIDです（-9は強制終了のパラメタです）"
echo "sudo kill -9 <プロセスID> のコマンドで手動削除してください。"
echo "例）sudo kill -9 1234"
