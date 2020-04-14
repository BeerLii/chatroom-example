import asyncio
import websockets
import json
USERS = {}

async def chat(websocket,path):
    async for message in websocket:
        user_info = {}
        data = json.loads(message)
        if data["type"] == "login":
            global USERS

            USERS[data['content']] = websocket
            user_info = json.dumps({"type":"login","content":data["content"]})

        elif data["type"] == "established":
            print(data)
            name = "404"
            for k,v in USERS.items():
                if v == websocket:
                    name = k
            user_info = json.dumps({"type":"established","content":data['content'],"from":name})
        await asyncio.wait([user.send(user_info) for user in USERS.values()])




if __name__ == '__main__':
    start_server = websockets.serve(chat,"localhost",9090)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()