#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

import subprocess
import argparse
import signal
import time
import sys
import os

def ctrl_exit(one, two):

    print(colored("\n[!] Exiting...", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_exit)

def arguments():

    argument = argparse.ArgumentParser(description="ICMP TRACER TOOL")
    argument.add_argument('-wp', '--write_ip', required=True, dest="write_ip", help="write ip, or some IP or a range of IP")

    return argument.parse_args()

def download_ping():

    command = "apt install iputils-ping"

    try:
        pedro = subprocess.run(command, shell=True, capture_output=True, text=True)
        pedro = pedro.stdout
        print(pedro)
    except Exception as e:
        print(colored("[!] Error: {e}", "red"))

def check_packages():

    command = "command -v ping"

    if subprocess.check_output(command, shell=True):
        return f"[+] The binary 'ping' is installed"
    else:
        return None

def initial_part(packages):

    print(colored("\n[+] Check necessary binaries\n", "red"))
    time.sleep(1)

    if packages:
        print(colored("\t[+] All the binaries are installed\n", "magenta"))
    else:
        print(colored("[+] Installing binaries", "red"))
        time.sleep(1)
        download_ping()

def check_ip_format(ip):

    ip_splitted = ip.split(".")
    first_three = ".".join(ip_splitted[:3])

    if len(ip_splitted) == 4:
        if "-" in ip_splitted[3]:
            start, end = ip_splitted[-1].split("-")
            return [f"{first_three}.{i}" for i in range(int(start), int(end)+1)]
        else:
            return [ip]
    else:
        print(colored(f"[!] Incorrect format {ip}", "red"))
        sys.exit(1)

def ping_to_ip(ip):

    try:
        ping = subprocess.run(['ping', '-c', '1', ip], timeout=1, stdout=subprocess.DEVNULL)

        if ping.returncode == 0:
            print(colored(f"[+] The IP {ip} is open", "green"))
    except subprocss.TimeoutExpired:
        pass

def main():

    argument = arguments()
    packages = check_packages()

    initial_part(packages)
    time.sleep(1)
    os.system("clear")
    time.sleep(1)

    print(colored("\n\n\t[+] Starting the ICMP TRACER\n\n", "red"))

    time.sleep(1)

    check = check_ip_format(argument.write_ip)

    with ThreadPoolExecutor(max_workers=100) as e:
        e.map(ping_to_ip, check)

if __name__ == "__main__":
    main()