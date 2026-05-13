#!/usr/bin/env python3
import argparse
import os
import sys
import time

import requests
from stem import Signal
from stem.control import Controller


def parse_args():
    parser = argparse.ArgumentParser(description="Request Tor circuit rotation and print public IP checks.")
    parser.add_argument("--server", default="127.0.0.1", help="Tor server address. Default: 127.0.0.1")
    parser.add_argument("--socks-port", type=int, default=9050, help="Tor SOCKS port. Default: 9050")
    parser.add_argument("--control-port", type=int, default=9051, help="Tor ControlPort. Default: 9051")
    parser.add_argument("--requests", type=int, default=5, help="Number of IP checks. Default: 5")
    parser.add_argument("--wait-seconds", type=int, default=15, help="Wait time after NEWNYM. Default: 15")
    parser.add_argument("--password-env", default="", help="Environment variable containing the ControlPort password.")
    parser.add_argument("--ip-check-url", default="https://icanhazip.com", help="Public IP check URL.")
    return parser.parse_args()


def get_control_password(password_env):
    if not password_env:
        return None

    value = os.environ.get(password_env, "")
    if not value:
        print("ERROR: password environment variable is empty: " + password_env, file=sys.stderr)
        return None

    return value


def get_public_ip(server, socks_port, ip_check_url):
    proxy_url = "socks5h://" + server + ":" + str(socks_port)
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    response = requests.get(ip_check_url, proxies=proxies, timeout=20)
    response.raise_for_status()
    return response.text.strip()


def renew_circuit(server, control_port, password):
    controller = Controller.from_port(address=server, port=control_port)

    try:
        if password is None:
            controller.authenticate()
        else:
            controller.authenticate(password=password)

        controller.signal(Signal.NEWNYM)
    finally:
        controller.close()


def run_rotation(args):
    password = get_control_password(args.password_env)
    seen_ips = []

    for index in range(1, args.requests + 1):
        try:
            public_ip = get_public_ip(args.server, args.socks_port, args.ip_check_url)
            seen_ips.append(public_ip)
            print("Request " + str(index) + ": " + public_ip)
        except Exception as exc:
            print("Request " + str(index) + " failed: " + str(exc), file=sys.stderr)

        if index < args.requests:
            try:
                renew_circuit(args.server, args.control_port, password)
                print("Requested Tor circuit renewal.")
            except Exception as exc:
                print("Circuit renewal failed: " + str(exc), file=sys.stderr)

            time.sleep(args.wait_seconds)

    unique_ips = sorted(set(seen_ips))
    print("")
    print("Unique IP count:", len(unique_ips))
    for public_ip in unique_ips:
        print("- " + public_ip)

    if len(unique_ips) > 1:
        print("Result: multiple public IP addresses observed.")
        return 0

    print("Result: no clear IP rotation observed.")
    return 2


def main():
    args = parse_args()
    return run_rotation(args)


if __name__ == "__main__":
    raise SystemExit(main())
