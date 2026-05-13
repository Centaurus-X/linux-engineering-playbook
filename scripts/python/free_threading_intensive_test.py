#!/usr/bin/env python3
import math
import multiprocessing
import sys
import threading
import time


def cpu_bound_range(start_index, end_index, results, result_index):
    total = 0.0

    for number in range(start_index, end_index):
        total += math.sqrt(number ** 3 + number ** 2 + number)

    results[result_index] = total


def split_ranges(limit, worker_count):
    ranges = []
    chunk_size = limit // worker_count

    for index in range(worker_count):
        start_index = index * chunk_size
        if index == worker_count - 1:
            end_index = limit
        else:
            end_index = (index + 1) * chunk_size
        ranges.append((start_index, end_index))

    return ranges


def run_threads(worker_count, limit):
    results = [0.0] * worker_count
    threads = []
    ranges = split_ranges(limit, worker_count)

    start = time.time()

    for index, item in enumerate(ranges):
        start_index, end_index = item
        thread = threading.Thread(target=cpu_bound_range, args=(start_index, end_index, results, index))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return time.time() - start


def run_processes(worker_count, limit):
    manager = multiprocessing.Manager()
    results = manager.list([0.0] * worker_count)
    processes = []
    ranges = split_ranges(limit, worker_count)

    start = time.time()

    for index, item in enumerate(ranges):
        start_index, end_index = item
        process = multiprocessing.Process(target=cpu_bound_range, args=(start_index, end_index, results, index))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return time.time() - start


def run_single(limit):
    results = [0.0]
    start = time.time()
    cpu_bound_range(0, limit, results, 0)
    return time.time() - start


def main():
    limit = 5 * 10 ** 7
    worker_count = multiprocessing.cpu_count()

    print("Python version:", sys.version)
    if hasattr(sys, "_is_gil_enabled"):
        print("GIL enabled:", sys._is_gil_enabled())

    single_duration = run_single(limit)
    thread_duration = run_threads(worker_count, limit)
    process_duration = run_processes(worker_count, limit)

    print("Single thread duration:", format(single_duration, ".2f"), "seconds")
    print("Multithreading duration:", format(thread_duration, ".2f"), "seconds")
    print("Multiprocessing duration:", format(process_duration, ".2f"), "seconds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
