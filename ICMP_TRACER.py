#!/usr/bin/env python3

import re
import sys
import signal
import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

def ctrl_exit(one, two):

    print(colored(f'[!] Exiting...', 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_exit)

def arguments():
    argument = argparse.ArgumentParser(description='ICMP TRACER')
    argument.add_argument('-i', '--ip_addres', required=True, dest='ip_addres', help='one ip: -i 192.168.255.255; range: -i 192.168.1.1-254')

    return argument.parse_args()

def valid_ip_range(value):
    parts = value.group()
    parts_list = parts.split('.')

    ip_three = '.'.join(parts_list[:3])

    ip_start, ip_end = parts_list[3].split('-')

    return ip_three, ip_start, ip_end

def check_format_ip(ip):

    octet = []
    ip_address = []

    valid1 = re.match(r'^([0-9]{3}\.){2}[0-9]{1,3}\.[0-9]{1,3}$', ip)
    valid2 = re.match(r'^([0-9]{3}\.){2}[0-9]{1,3}\.[0-9]{1,3}\-[0-9]{1,3}', ip)

    if valid1:
        return [ip]
    elif valid2:
        one, two, three = valid_ip_range(valid2)
        return [f'{one}.{i}' for i in range(int(two), int(three)+1)]

def get_ttl(ip):

    command = f"ping -c 1 {ip} | awk 'NR==2' | cut -d '=' -f 3 | tr ' ' '\n'  | awk 'NR==1'"
    result_in = subprocess.run(command, shell=True, capture_output=True, text=True)
    results = result_in.stdout
    return results

def type_ttl(ttl):

    if ttl == 64:
        return colored('[+] TTL linux', 'magenta')
    elif ttl == 32:
        return colred('[+] TTL Windows 95/98/NT', 'cyan')
    elif ttl == 128:
        return colored('[+] TTL Windows 2000/XP/2003/Vista/7/8/10', 'cyan')

def ping_connection(ip):

    try:
        connection = subprocess.run(['ping', '-c', '1', ip], timeout=1, stdout=subprocess.DEVNULL)

        if connection.returncode == 0:
            ip_ttl = get_ttl(ip)
            ttl = type_ttl(int(ip_ttl))
            print(colored(f'\n[+] The IP {ip} is active - {ttl}', 'green'))

    except subprocess.TimeoutExpired:
        pass

def main():
    argument = arguments()
    pedro = check_format_ip(argument.ip_addres)

    max_work = 100

    try:
        with ThreadPoolExecutor(max_workers=max_work) as executor:
            executor.map(ping_connection, pedro)
    except TypeError:
        print(colored('[!] Invalid format', 'red'))

if __name__ == "__main__":
    main()