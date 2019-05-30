import asyncio
import random

import websockets


async def hello(task_name, task_number):
    ip = random.choice(["139.59.136.182", "165.22.89.205"])
    port = 80
    websocket = await websockets.connect(f"ws://{ip}:{port}")
    # await websocket.send("ping")
    while True:
        response = await websocket.recv()
        print(f"({task_name}):{response}")


tasks = []
for i in range(3000):
    tasks.append(hello(f"task_{i}", i))

asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
