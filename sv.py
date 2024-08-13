import sys
sys.path.append('lib')
import asyncio
import websockets # type: ignore

'''
async def handler(websocket, path):
    async for message in websocket:
        print(f"Received: {message}")

start_server = websockets.serve(handler, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server is running on ws://localhost:8080")
asyncio.get_event_loop().run_forever()

'''

import subprocess

# momoの実行コマンドとオプション
command = ['../momo_armv7/momo', '--no-audio-device', 'test']

# subprocessを使ってコマンドを実行
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 標準出力と標準エラーを取得
stdout, stderr = process.communicate()

# 出力を表示
print(stdout.decode())
print(stderr.decode())
