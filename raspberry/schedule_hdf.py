import numpy as np
import h5py
import sys
sys.path.append("../")
from HDF5.HDF5Schedule import HDF5Schedule, Datasets
from HDF5.HDF5Write import HDF5Write
import argparse
import socket
import sys
import random
import numpy as np
from time import time, sleep
from raspberry.time_series import *

HOST_IP = "127.0.0.1"
NUMBERS = 21 + 14 # 21 wind speed and 14 gusts
EVENTS = 5

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--group', help='dataset group (speed) or (direction)', type=str, default="holiday", required=True)
    parser.add_argument('-cr', '--collect_random_samples', help='collects random samples', type=bool, default=True, required=True)
    parser.add_argument('-sim', '--simulate', help='simulates the collection', type=bool, default=True, required=True)
    parser.add_argument('-rf', '--reset_frequency', help='frequency to reset the data collection', type=float, default=5, required=True)
    parser.add_argument('-gu', '--gust', help='include gusts collection', type=bool, default=True, required=False)
    parser.add_argument('-dl', '--direction_log', help='log file used for direction', type=str, default="", required=False)
    parser.add_argument('-sl', '--speed_log', help='log file used for speed', type=str, default="", required=False)
    parser.add_argument('-sd', '--speed_dataset', help='dataset used for speed', type=str, default=None, required=False)
    parser.add_argument('-dd', '--direction_dataset', help='dataset used for direction', type=str, default=None, required=False)
    parser.add_argument('-p', '--port', help='port for calculation', type=int, default=None, required=True)

    return parser.parse_args()

if __name__ == "__main__":

    args = parse_args()

    PORT = int(args.port)
    data = sys.stdin.read().split("/")
    data = list(map(lambda d: float(d), data))

    speed_log = args.group if args.group == "speed" else None
    direction_log = args.group if args.group == "direction" else None
    if not speed_log and not direction_log:
        print("The log file must be mentioned..")
    schedule = HDF5Schedule(speed_log, direction_log)
    write = HDF5Write()
    dataset = args.speed_dataset if args.speed_dataset else args.direction_dataset
    if dataset and args.simulate:
        write.create_file(dataset)
        dataset = schedule.create_dataset(args.group, write)
        schedule.write_dataset(
            write, args.group, dataset.name, 
            np.array(data).astype(np.float64), 0
        )
    elif args.reset_frequency:
        cron = Cron()
        while True:
            sleep(args.reset_frequency)
            cron.reset_cron()
