"""Live plot of load cell data streamed from the Arduino over serial.

Usage: python plot_loadcell.py [--port COM4] [--baud 115200] [--window 20] [--csv out.csv]
Close the plot window (or Ctrl+C) to stop.
"""
import argparse
import collections
import sys

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

ap = argparse.ArgumentParser()
ap.add_argument("--port", default="COM4")
ap.add_argument("--baud", type=int, default=115200)
ap.add_argument("--window", type=float, default=20.0, help="seconds shown")
ap.add_argument("--csv", help="optionally log data to this CSV file")
args = ap.parse_args()

ser = serial.Serial(args.port, args.baud, timeout=0.05)
log = open(args.csv, "w") if args.csv else None
if log:
    log.write("time_s,raw\n")

t_buf = collections.deque()
v_buf = collections.deque()
t0 = None

fig, ax = plt.subplots()
(line,) = ax.plot([], [], lw=1)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Load cell (raw counts, tared)")
ax.grid(True)


def update(_):
    global t0
    while ser.in_waiting:
        raw = ser.readline().decode(errors="ignore").strip()
        parts = raw.split(",")
        if len(parts) != 2:
            continue
        try:
            t, v = int(parts[0]), int(parts[1])
        except ValueError:
            continue  # header or garbled line
        if t0 is None:
            t0 = t
        ts = (t - t0) / 1000.0
        t_buf.append(ts)
        v_buf.append(v)
        if log:
            log.write(f"{ts},{v}\n")
        while t_buf and ts - t_buf[0] > args.window:
            t_buf.popleft()
            v_buf.popleft()
    if t_buf:
        line.set_data(t_buf, v_buf)
        ax.set_xlim(max(0, t_buf[-1] - args.window), max(args.window, t_buf[-1]))
        lo, hi = min(v_buf), max(v_buf)
        pad = max((hi - lo) * 0.1, 1)
        ax.set_ylim(lo - pad, hi + pad)
    return (line,)


ani = animation.FuncAnimation(fig, update, interval=50, blit=False, cache_frame_data=False)
try:
    plt.show()
finally:
    ser.close()
    if log:
        log.close()
