import asyncio
import random
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from socketclusterclient import Socketcluster

import websockets

conn_times = {}
ping_times = []

servers = [
    "139.59.136.182",
    #"165.22.89.205",
    #"165.227.167.134"
]


def write_conn_times():
    with open('conn_times.txt', 'w') as f:
        for task_id, conn_time in conn_times.items():
            print(f"Task {task_id} was connected")
            f.write(f"{str(conn_time.timestamp())}, 1\n")


def write_ping_times():
    with open('ping_times.txt', 'w') as f:
        for request_time, response_time in ping_times:
            f.write(f"{str(request_time.timestamp())}, {str(response_time.timestamp())}, 1\n")


def connect_and_wait(task_id):
    def onconnect(socket):
        print("CONNECTED")
        conn_times[task_id] = datetime.now()

    def ondisconnect(socket):
        print("DISCONNECTED")
        del conn_times[task_id]

    def onConnectError(socket, error):
        print(f"ERROR {error}")

    socket = Socketcluster.socket(f"ws://{random.choice(servers)}:80/socketcluster/")
    socket.setBasicListener(onconnect, ondisconnect, onConnectError)
    socket.enablelogger(True)
    socket.connect()


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
    pool = ThreadPoolExecutor(max_workers=5000)
    for i in range(5000):
        pool.submit(connect_and_wait, i)
    return pool


def run_throughput_test():
    tasks = []
    for i in range(1):
        tasks.append(connect_and_ping(f"task_{i}", i, sleep_time=5))
    try:
        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
    finally:
        write_ping_times()


if __name__ == "__main__":
    thread_pool = None
    try:
        thread_pool = run_max_conn_test()
    finally:
        print("Sleeping")
        time.sleep(20)
        print("Writing results")
        write_conn_times()
