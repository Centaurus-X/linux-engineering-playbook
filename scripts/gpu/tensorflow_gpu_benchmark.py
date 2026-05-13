#!/usr/bin/env python3
import argparse
import sys
import time


def parse_args():
    parser = argparse.ArgumentParser(description="Run a TensorFlow GPU matrix multiplication benchmark.")
    parser.add_argument("--size", type=int, default=4096, help="Matrix size. Default: 4096")
    return parser.parse_args()


def run_benchmark(tf, size):
    with tf.device("/device:GPU:0"):
        left = tf.random.normal([size, size], dtype=tf.float32)
        right = tf.random.normal([size, size], dtype=tf.float32)

        start = time.time()
        result = tf.matmul(left, right)
        result.numpy()
        duration = time.time() - start

    return duration


def main():
    args = parse_args()

    try:
        import tensorflow as tf
    except Exception as exc:
        print("ERROR: TensorFlow import failed:", exc, file=sys.stderr)
        return 1

    gpus = tf.config.list_physical_devices("GPU")
    if not gpus:
        print("ERROR: No TensorFlow GPU device detected.", file=sys.stderr)
        return 2

    duration = run_benchmark(tf, args.size)
    print("TensorFlow version:", tf.__version__)
    print("GPU devices:", gpus)
    print("Matrix size:", str(args.size) + "x" + str(args.size))
    print("Duration seconds:", format(duration, ".4f"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
