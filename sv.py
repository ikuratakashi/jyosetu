import sys
sys.path.append('lib')
import asyncio
import websockets # type: ignore
import socket

async def receive_message():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received message:{message}")

asyncio.get_event_loop().run_until_complete(receive_message())

'''
# ホスト名を取得
hostname = socket.gethostname()
# ホスト名をIPv4アドレスに変換
ip_address = socket.gethostbyname(hostname)

asyncio.get_event_loop().run_until_complete(start_server)
print(f"WebSocket server is running on ws://{ip_address}:1000")
asyncio.get_event_loop().run_forever()
'''
