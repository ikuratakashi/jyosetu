import sys
sys.path.append('lib')
import asyncio
import websockets # type: ignore
import socket

port = 1000
host = "localhost"

async def echo(websocket, path):
    '''
    メッセージを取得した時の動作
    '''
    async for message in websocket:
        print(f"message: {message} / path:{path}")
        await websocket.send(f"Echo: {message}")

# サーバーの起動
start_server = websockets.serve(echo, host, port)

# ホスト名を取得
hostname = socket.gethostname()
# ホスト名をIPv4アドレスに変換
ip_address = socket.gethostbyname(hostname)
# サーバーの永続化
asyncio.get_event_loop().run_until_complete(start_server)
print(f"WebSocket server is running on ws://{ip_address}:{port} or ws://{hostname}:{port}")
asyncio.get_event_loop().run_forever()
