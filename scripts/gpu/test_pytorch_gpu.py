#!/usr/bin/env python3
import sys


def main():
    try:
        import torch
    except Exception as exc:
        print("ERROR: PyTorch import failed:", exc, file=sys.stderr)
        return 1

    print("PyTorch version:", torch.__version__)
    print("Is CUDA available:", torch.cuda.is_available())
    print("CUDA version:", torch.version.cuda)

    if not torch.cuda.is_available():
        print("ERROR: CUDA is not available to PyTorch.", file=sys.stderr)
        return 2

    device = torch.device("cuda:0")
    left = torch.tensor([1.0, 2.0], device=device)
    right = torch.tensor([3.0, 4.0], device=device)
    result = left + right

    print("Device name:", torch.cuda.get_device_name(0))
    print("Addition result:", result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
