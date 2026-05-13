#!/usr/bin/env python3
import multiprocessing
import sys
import threading
import time


def cpu_bound_task(limit):
    total = 0
    for number in range(limit):
        total += number * number
    return total


def worker_process(limit):
    cpu_bound_task(limit)


def run_threads(worker_count, limit):
    threads = []

    start = time.time()

    for _index in range(worker_count):
        thread = threading.Thread(target=cpu_bound_task, args=(limit,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return time.time() - start


def run_processes(worker_count, limit):
    processes = []

    start = time.time()

    for _index in range(worker_count):
        process = multiprocessing.Process(target=worker_process, args=(limit,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return time.time() - start


def main():
    limit = 10 ** 7
    worker_count = 4

    print("Python version:", sys.version)
    if hasattr(sys, "_is_gil_enabled"):
        print("GIL enabled:", sys._is_gil_enabled())

    start = time.time()
    cpu_bound_task(limit)
    single_duration = time.time() - start

    thread_duration = run_threads(worker_count, limit)
    process_duration = run_processes(worker_count, limit)

    print("Single thread duration:", format(single_duration, ".2f"), "seconds")
    print("Multithreading duration:", format(thread_duration, ".2f"), "seconds")
    print("Multiprocessing duration:", format(process_duration, ".2f"), "seconds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
