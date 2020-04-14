import threading
import asyncio
import websockets
import json
from aioconsole import ainput

global_websocket = None

async def handle_input():
    while not global_websocket:
        websocket = global_websocket
    while True:
        line = await ainput("")
        await websocket.send(json.dumps({"type": "established", "content": line}))


async def handle_recv(websocket):
    while True:
        response_info = await websocket.recv()
        response_info = json.loads(response_info)
        if response_info['type'] == 'login':
            print(f"欢迎用户{response_info['content']}登陆聊天室")
        elif response_info['type'] == 'established':
            print(f"用户{response_info['from']}发送:{response_info['content']}")

async def chat(name):
    uri = "ws://localhost:9090"
    async with websockets.connect(uri) as websocket:
        global global_websocket
        global_websocket = websocket
        print(global_websocket)
        await websocket.send(json.dumps({"content": name, "type": "login"}))
        task = asyncio.create_task(handle_recv(websocket))
        await task





def input_thread():

    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handle_input())





def chat_thread(name):

    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(chat(name))


def main():

    name = input("Input your name:")
    thread1 = threading.Thread(target=input_thread,args=())
    thread2 = threading.Thread(target=chat_thread,args=(name,))
    thread1.setDaemon(True)
    thread2.setDaemon(True)
    thread2.start()
    thread1.start()
    thread1.join()
    thread2.join()


if __name__ == '__main__':
    main()