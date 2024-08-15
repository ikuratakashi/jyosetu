import sys
sys.path.append('lib')
import asyncio
import websockets # type: ignore
import socket

async def handler(websocket, path):
    async for message in websocket:
        print(f"Received: {message}")

start_server = websockets.serve(handler, "0.0.0.0", 1000)
#start_server = websockets.serve(handler, "localhost", 8080)

# ホスト名を取得
hostname = socket.gethostname()
# ホスト名をIPv4アドレスに変換
ip_address = socket.gethostbyname(hostname)

asyncio.get_event_loop().run_until_complete(start_server)
print(f"WebSocket server is running on ws://{ip_address}:1000")
asyncio.get_event_loop().run_forever()
