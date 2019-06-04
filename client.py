import asyncio
import random
from datetime import datetime

import websockets

conn_times = []
ping_times = []

servers = [
    "139.59.136.182",
    "165.22.89.205",
    "165.227.167.134"
]


def write_conn_times():
    with open('conn_times.txt', 'w') as f:
        for conn_time in conn_times:
            f.write(f"{str(conn_time.timestamp())}, 1\n")


def write_ping_times():
    with open('ping_times.txt', 'w') as f:
        for request_time, response_time in ping_times:
            f.write(f"{str(request_time.timestamp())}, {str(response_time.timestamp())}, 1\n")


async def connect_and_wait(task_name, task_number):
    ip = random.choice(servers)
    port = 80
    websocket = await websockets.connect(f"ws://{ip}:{port}")
    conn_times.append(datetime.now())
    await websocket.recv()


async def connect_and_ping(task_name, task_number, sleep_time):
    ip = random.choice(servers)
    port = 80
    websocket = await websockets.connect(f"ws://{ip}:{port}")
    while True:
        req_time = datetime.now()
        await websocket.send("ping")
        response = await websocket.recv()
        resp_time = datetime.now()
        ping_times.append((req_time, resp_time))
        print(f"({task_name}):{response}")
        await asyncio.sleep(sleep_time)


def run_max_conn_test():
    tasks = []
    for i in range(10000):
        tasks.append(connect_and_wait(f"task_{i}", i))
    try:
        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        write_conn_times()


def run_throughput_test():
    tasks = []
    for i in range(1):
        tasks.append(connect_and_ping(f"task_{i}", i, sleep_time=5))
    try:
        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        write_ping_times()


if __name__ == "__main__":
    run_max_conn_test() 
