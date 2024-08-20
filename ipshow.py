import sys
import socket

# ホスト名を取得
hostname = socket.gethostname()
# ホスト名をIPv4アドレスに変換
ip_address = socket.gethostbyname(hostname)

print(ip_address)