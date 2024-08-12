import sys
sys.path.append('lib')
import asyncio
import websockets # type: ignore

async def handler(websocket, path):
    async for message in websocket:
        print(f"Received: {message}")

start_server = websockets.serve(handler, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server is running on ws://localhost:8080")
asyncio.get_event_loop().run_forever()
