#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys
import time


def parse_args():
    parser = argparse.ArgumentParser(description="Experimental X11 keyboard lock helper.")
    parser.add_argument("--seconds", type=int, default=10, help="Seconds to keep the keyboard detached.")
    parser.add_argument("--device-id", default="", help="Explicit xinput device ID. If omitted, only devices are listed.")
    parser.add_argument("--master-id", default="3", help="XInput master keyboard ID for reattach. Default: 3")
    parser.add_argument("--apply", action="store_true", help="Actually detach and reattach the device.")
    return parser.parse_args()


def run_command(command):
    return subprocess.run(command, capture_output=True, text=True, check=False)


def list_devices():
    result = run_command(["xinput", "--list"])
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return []

    devices = []
    for line in result.stdout.splitlines():
        if "keyboard" not in line.lower():
            continue

        match = re.search(r"id=(\d+)", line)
        if match:
            devices.append((match.group(1), line.strip()))

    return devices


def print_devices(devices):
    print("Detected keyboard-like XInput devices:")
    for device_id, line in devices:
        print("- id=" + device_id + " :: " + line)


def detach_device(device_id):
    return run_command(["xinput", "float", device_id])


def reattach_device(device_id, master_id):
    return run_command(["xinput", "reattach", device_id, master_id])


def main():
    args = parse_args()
    devices = list_devices()
    print_devices(devices)

    if not args.apply:
        print("")
        print("Dry run only. Re-run with --apply --device-id <ID> to test detaching.")
        return 0

    if not args.device_id:
        print("ERROR: --device-id is required with --apply.", file=sys.stderr)
        return 1

    print("Detaching device:", args.device_id)
    result = detach_device(args.device_id)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode

    try:
        print("Keyboard detached for", args.seconds, "seconds.")
        time.sleep(args.seconds)
    finally:
        print("Reattaching device:", args.device_id)
        reattach_device(args.device_id, args.master_id)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
