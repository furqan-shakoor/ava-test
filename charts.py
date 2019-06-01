import matplotlib.pyplot as plt
import arrow


def load_conn_times(filename):
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


def plot_conn_times(time_conn_cuml):
    plt.plot(list(time_conn_cuml.keys()), list(time_conn_cuml.values()))
    plt.show()


def main():
    plot_conn_times(load_conn_times('conn_times_7k.txt'))
    plot_conn_times(load_conn_times('conn_times_7k_2.txt'))


if __name__ == "__main__":
    main()
