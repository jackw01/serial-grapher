__version__ = "0.1.0"

import argparse
import time
import collections
import threading
import csv

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#serialgrapher -p COM3 --y-max 100
#serialgrapher -p COM3 -l 5000 --y-max 100 --rate-limit 0.1

def main():
    parser = argparse.ArgumentParser(
        description='Utility for graphing CSV data received over a serial port'
    )
    parser.add_argument('-p', type=str, metavar='PORT',
                        help='Serial port')
    parser.add_argument('-b', type=int, default=115200, metavar='BAUD_RATE',
                        help='Baud rate')
    parser.add_argument('-l', type=int, default=1000, metavar='LENGTH',
                        help='Number of data points to show on graph')
    parser.add_argument('--dont-save', action='store_true',
                        help='Don\'t save the data to a CSV file')
    parser.add_argument('--rate-limit', type=float, default=2, metavar='LIMIT',
                        help='Maximum sample rate in samples/second')
    parser.add_argument('--auto-scale-y', action='store_true',
                        help='Automatically scale the y axis')
    parser.add_argument('--y-min', type=float, default=0.0, metavar='MIN',
                        help='Minimum y value')
    parser.add_argument('--y-max', type=float, default=1.0, metavar='MAX',
                        help='Maximum y value')
    args = parser.parse_args()

    ser = serial.Serial(args.p, args.b, timeout=10)

    if not args.dont_save:
        csv_file = open(f'{time.strftime("%Y%m%dT%H%M%S")}.csv', 'w', newline='')
        writer = csv.writer(csv_file)

    def get_line():
        return ser.readline().decode('ascii').strip()

    line = ''
    while line == '':
        line = get_line()
    headers = line.split(',')
    if not args.dont_save:
        writer.writerow(['Time'] + headers)

    DataPoint = collections.namedtuple('DataPoint', 'time values')

    data = collections.deque([DataPoint(0, [0] * len(headers))] * args.l, args.l)
    fig, axes = plt.subplots(len(headers))

    plots = []
    value_texts = []
    for i, header in enumerate(headers):
        ax = axes if len(headers) == 1 else axes[i]
        ax.set_xlim([0, args.l])
        ax.set_ylim([args.y_min, args.y_max])
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(header)
        plots.append(ax.plot([], [], label=header)[0])
        value_texts.append(ax.text(0.02, 0.9, '', transform=ax.transAxes))

    run_serial_loop = True

    event = threading.Event()
    read_interval = 1.0 / args.rate_limit

    def read_serial():
        while run_serial_loop:
            values = [float(v) for v in get_line().split(',')]
            t = time.perf_counter()
            if t - data[-1].time > read_interval:
                data.append(DataPoint(t, values))
                if not args.dont_save:
                    writer.writerow([t] + values)
                #event.wait(max(0, read_interval - (time.perf_counter() - t)))

    thread = threading.Thread(target=read_serial, daemon=True)
    thread.start()

    y_limit_margin = 0.05

    def animate(frame):
        for i, plot in enumerate(plots):
            ax = axes if len(headers) == 1 else axes[i]
            times = [dp.time for dp in data]
            time_max = max(times)
            prev_xlim = ax.get_xlim()
            ax.set_xlim([prev_xlim[0] + (time_max - prev_xlim[1]),
                         max(time_max, min(times) + 0.001)])

            series = [dp.values[i] for dp in data]
            if args.auto_scale_y:
                series_min, series_max = min(series), max(series)
                margin = y_limit_margin * (series_max - series_min)
                ax.set_ylim([series_min - margin, series_max + margin])
            plot.set_data(times, series)
            value_texts[i].set_text(f'{headers[i]}: {series[-1]}')

    animation_interval = max(read_interval * 1000, 200)
    anim = animation.FuncAnimation(fig, animate, fargs=(), interval=animation_interval)

    plt.show()

    run_serial_loop = False
    event.set()
    thread.join()
    ser.close()
    if not args.dont_save:
        csv_file.close()

