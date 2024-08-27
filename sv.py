import sys
sys.path.append('lib')
import asyncio
import websockets  # type: ignore
import socket

port = 1000
host = "0.0.0.0"  # すべてのインターフェースから接続を受け入れる

async def handler(websocket, path):
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            #await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

async def main():
    start_server = await websockets.serve(handler, host, port)

    # ホスト名とIPアドレスの取得
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"WebSocket server is running on ws://{ip_address}:{port} or ws://{hostname}:{port}")

    await start_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
