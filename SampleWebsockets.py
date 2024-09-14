import sys
sys.path.append('lib')
import asyncio
import websockets  # type: ignore
import signal

# WebSocketサーバーとして動作する関数
async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"Echo: {message}")

# WebSocketサーバーを起動する関数
async def start_server():
    server = await websockets.serve(echo, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    
    # サーバーが終了するまで待つ
    await server.wait_closed()

def shutdown():
    print("\nShutting down WebSocket server...")
    sys.exit(0)

# メイン処理
if __name__ == "__main__":
    # Ctrl+Cで終了するためのハンドラを登録
    signal.signal(signal.SIGINT, lambda sig, frame: shutdown())

    try:
        # イベントループを開始
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
