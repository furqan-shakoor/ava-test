import random
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import arrow
from socketclusterclient import Socketcluster

conn_times = {}
ping_times = []

task_to_socket = {}

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
    print("File written")


def write_ping_times():
    with open('ping_times.txt', 'w') as f:
        for request_time, response_time in ping_times:
            f.write(f"{str(request_time.timestamp())}, {str(response_time.timestamp())}, 1\n")
    print("File written")


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
    socket.connect()


def connect_and_ping(task_number):
    def send_ping(socket):
        print("Sending ping")
        request_time = str(datetime.now().timestamp())
        socket.emit("pping", request_time)

    def onconnect(socket):
        print("CONNECTED")
        websocket.on("ppong", pong_handle)
        task_to_socket[task_number] = socket
        send_ping(socket)

    def ondisconnect(socket):
        print("DISCONNECTED")
        del conn_times[task_number]

    def onConnectError(socket, error):
        print(f"ERROR {error}")

    def pong_handle(eventname, request_time):
        resp_time = datetime.now()
        print("Got ppong")
        request_time = arrow.get(request_time).datetime
        ping_times.append((request_time, resp_time))
        send_ping(task_to_socket[task_number])

    ip = random.choice(servers)
    port = 80
    websocket = Socketcluster.socket(f"ws://{ip}:{port}/socketcluster/")
    websocket.setBasicListener(onconnect, ondisconnect, onConnectError)
    websocket.connect()


def run_max_conn_test():
    connections = 5000

    pool = ThreadPoolExecutor(max_workers=connections)
    try:
        for i in range(connections):
            pool.submit(connect_and_wait, i)
    finally:
        print("Sleeping")
        time.sleep(20)
        print("Writing results")
        write_conn_times()


def run_throughput_test():
    connections = 100

    pool = ThreadPoolExecutor(max_workers=connections)
    try:
        for i in range(connections):
            pool.submit(connect_and_ping, i)
    finally:
        print("Sleeping")
        time.sleep(10)
        print("Writing results")
        write_ping_times()


if __name__ == "__main__":
    run_throughput_test()
