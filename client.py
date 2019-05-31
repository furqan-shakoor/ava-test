import asyncio
import random
from datetime import datetime

import websockets

conn_times = []


def write_conn_times():
    with open('conn_times.txt', 'w') as f:
        for conn_time in conn_times:
            f.write(f"{str(conn_time.timestamp())}, 1\n")


async def hello(task_name, task_number):
    ip = random.choice(["139.59.136.182", "165.22.89.205"])
    port = 80
    websocket = await websockets.connect(f"ws://{ip}:{port}")
    conn_times.append(datetime.now())
    # await websocket.send("ping")
    while True:
        response = await websocket.recv()
        print(f"({task_name}):{response}")


def main():
    tasks = []
    for i in range(10):
        tasks.append(hello(f"task_{i}", i))

    try:
        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        write_conn_times()


if __name__ == "__main__":
    main()
