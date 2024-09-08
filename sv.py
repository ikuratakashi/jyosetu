version = "10.2.101"
PgName = "Jyosetu Message Server"

import sys
sys.path.append('lib')
import asyncio
import websockets  # type: ignore
import socket
import os
import platform

port = 50001
host = "0.0.0.0"  # すべてのインターフェースから接続を受け入れる

def Openning():
    print('/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/')
    print('')
    print(f'{PgName}')
    print('')
    print(f'var:{version}')
    print('')
    print('/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/')
    print('')
    print('')
    print(f'Wellcome to {PgName}.')
    print('')
    print('')

async def handler(websocket, path):
    try:
        async for message in websocket:

            if platform.system() == "Windows":
                os.system("cls")
            else:
                os.system("clear")

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
    Openning()
    asyncio.run(main())
