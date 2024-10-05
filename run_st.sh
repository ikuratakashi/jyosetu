#!/bin/bash

cd /home/jyosetu/jyosetu

#sudo /usr/bin/python ./sv.py &
sudo ./sv.py &
echo 通信サーバ プロセスID：$!
echo $! > ./tmp/websocket.pid

#sudo /usr/bin/python ./rs232c.py &
#echo RS232C確認 プロセスID：$!
#echo $! > ./tmp/rs232c.pid

cd ./www
#/usr/bin/python ./www.py &
sudo ./www.py &
echo Webサーバ プロセスID：$!
echo $! > ../tmp/www.pid

echo server http://$(python ipshow.py):50100/

cd ..
