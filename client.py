import asyncio
import websockets


async def hello():
    websocket = await websockets.connect("ws://localhost:8765")
    for _ in range(1):
        await websocket.send("ping")

        # response = await websocket.recv()
        # print(f"Got response {response}")


tasks = []
for _ in range(10):
    tasks.append(hello())

asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
