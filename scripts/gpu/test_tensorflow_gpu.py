#!/usr/bin/env python3
import sys


def main():
    try:
        import tensorflow as tf
    except Exception as exc:
        print("ERROR: TensorFlow import failed:", exc, file=sys.stderr)
        return 1

    print("TensorFlow version:", tf.__version__)
    print("Is built with CUDA:", tf.test.is_built_with_cuda())

    gpus = tf.config.list_physical_devices("GPU")
    print("Available GPUs:", gpus)

    if not gpus:
        print("ERROR: No TensorFlow GPU device detected.", file=sys.stderr)
        return 2

    with tf.device("/device:GPU:0"):
        left = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        right = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        result = tf.matmul(left, right)

    print("Matrix multiplication result:")
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
