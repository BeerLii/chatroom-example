import asyncio
import websockets
import json
from aioconsole import ainput


async def handle_input(websocket):
    while True:
        line = await ainput("")
        await websocket.send(json.dumps({"type":"established","content":line}))

async def hanle_recv(websocket):
    while True:
        response_info = await websocket.recv()
        response_info = json.loads(response_info)
        if response_info['type'] == 'login':
            print(f"欢迎用户{response_info['content']}登陆聊天室",end="\r")
        elif response_info['type'] == 'established':
            print(f"用户{response_info['from']}发送:{response_info['content']}",end="\r")


async def client():
    uri = "ws://localhost:9090"
    async with websockets.connect(uri) as websocket:
        name = input("Input your name:")
        await websocket.send(json.dumps({"content": name, "type": "login"}))
        task1 = asyncio.create_task(handle_input(websocket))
        task2 = asyncio.create_task(hanle_recv(websocket))
        await task1
        await task2


loop = asyncio.get_event_loop()
loop.run_until_complete(client())
loop.run_forever()