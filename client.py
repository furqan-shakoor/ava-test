import asyncio
import random

import websockets


async def hello(task_name, task_number):
    port = random.choice([8765, 8766])
    websocket = await websockets.connect(f"ws://localhost:{port}")
    while True:
        response = await websocket.recv()
        ident = ">  " * task_number
        print(f"{ident}({task_name}):{response}")


tasks = []
for i in range(4):
    tasks.append(hello(f"task_{i}", i))

asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
