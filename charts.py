import math

from matplotlib import pyplot
import arrow


def load_conn_times(filename):
    # TODO: Sort on times
    time_conn_cuml = {}
    i = 1
    start_time = None
    with open(filename) as f:
        for line in f:
            time, _ = line.split(', ')
            time = arrow.get(time)
            if start_time is None:
                start_time = time
            seconds_from_start = (time - start_time).total_seconds()
            time_conn_cuml[seconds_from_start] = i
            i += 1
    return time_conn_cuml


def load_ping_times(filename):
    response_by_time = {}

    start_time = None
    with open(filename) as f:
        for line in f:
            req_ts, res_ts, _ = line.split(', ')
            req_time, res_time = arrow.get(req_ts), arrow.get(res_ts)
            if start_time is None:
                start_time = req_time
            resp_delta_sec = math.floor((res_time - start_time).total_seconds())
            response_by_time[resp_delta_sec] = response_by_time.get(resp_delta_sec, 0) + 1

    return response_by_time


def plot_conn_times(time_conn_cuml):
    pyplot.plot(list(time_conn_cuml.keys()), list(time_conn_cuml.values()))
    # pyplot.ylim(0, 10000)
    # pyplot.xlim(0, 15)
    pyplot.show()


def plot_ping_times(timedelta_to_pingcount):
    pyplot.plot(list(timedelta_to_pingcount.keys()), list(timedelta_to_pingcount.values()))
    # pyplot.ylim(0, 1000)
    pyplot.show()


def main():
    # plot_conn_times(load_conn_times('conn_times_ava_3_10k.txt'))
    # plot_conn_times(load_conn_times('conn_times_ava_2_10k.txt'))
    plot_conn_times(load_conn_times("conn_times_sc_1_7k.txt"))
    plot_conn_times(load_conn_times("conn_times.txt"))


if __name__ == "__main__":
    main()
