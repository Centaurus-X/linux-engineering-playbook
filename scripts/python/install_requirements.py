#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Install Python requirements from a requirements file.")
    parser.add_argument("--file", default="requirements.txt", help="Requirements file path. Default: requirements.txt")
    return parser.parse_args()


def install_requirements(requirements_file):
    path = Path(requirements_file)

    if not path.exists():
        print("ERROR: requirements file not found: " + str(path), file=sys.stderr)
        return 1

    command = [sys.executable, "-m", "pip", "install", "-r", str(path)]
    print("Running:", " ".join(command))

    result = subprocess.run(command, check=False)
    return result.returncode


def main():
    args = parse_args()
    return install_requirements(args.file)


if __name__ == "__main__":
    raise SystemExit(main())
