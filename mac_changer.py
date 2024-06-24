#!/usr/bin/env python3

import subprocess
import re
import subprocess
import argparse
import os
from termcolor import colored

def arguments():

    argument = argparse.ArgumentParser(description='Mac changer')
    argument.add_argument('-i', '--interface', dest='interface', help='-i ens33')
    argument.add_argument('-m', '--mac', dest='mac', help='-m 00:03:fb:45:34:eg')
    argument.add_argument('-r', '--reset', action='store_true', dest='reset', help='-r')

    return argument.parse_args()

def get_permanent_mac_interface():

    command = "ifconfig | awk '{print $1}' | head -n 1 | tr ':' ' ' | awk '{print $1}'"
    interface_command = subprocess.run(command, shell=True, capture_output=True, text=True)
    interface = interface_command.stdout

    command2= "ifconfig | awk '/ether/' |  awk '{print $2}'"
    mac_command = subprocess.run(command2, shell=True, capture_output=True, text=True)
    mac = mac_command.stdout

    return interface, mac

def save_mac_and_interface():

    param = []

    interface, mac = get_permanent_mac_interface()
    param.append(interface)
    param.append(mac)

    if not os.path.exists('parameters'):
        for i in param:
            with open('parameters', 'a') as file:
                file.write(i)

def change_automatic(interface, mac):
    subprocess.run(['ifconfig', interface, 'down'])
    subprocess.run(['ifconfig', interface, 'hw', 'ether', mac])
    subprocess.run(['ifconfig', interface, 'up'])


def reset_mac_interface():

    if os.path.exists('parameters'):
        with open('parameters', 'r') as file:
            lines = file.readlines()
            interface = lines[0].strip()
            mac = lines[1].strip()
            change_automatic(interface, mac)

def valid_parameters(interface, mac):

    valid_interface = re.match(r'^[e][n|t][s|h]\d{1,2}$', interface)
    valid_mac = re.match(r'^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}$', mac)

    return valid_interface and valid_mac

def change_all():

    save_mac_and_interface()
    argument = arguments()
    interface = argument.interface
    mac = argument.mac

    if argument.reset:
        reset_mac_interface()
    elif valid_parameters(interface, mac):
        change_automatic(interface, mac)
    else:
        print(colored(f"[!] Invalid Information", 'red'))

def main():
    change_all()

if __name__ == "__main__":
    main()