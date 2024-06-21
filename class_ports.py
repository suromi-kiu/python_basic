#!/usr/bin/env python3

import socket
import sys
import os
from concurrent.futures import ThreadPoolExecutor
import signal
import argparse
from termcolor import colored


class Port_scanner:

    def __init__(self):
        self.host = ''
        self.port = 0
        self.open_sockets = []

        signal.signal(signal.SIGINT, self.exit_ctrl)

    def exit_ctrl(self, sig, frame):
        print(colored("[!] Saliendo del programa", 'red'))
        for sock in self.open_sockets:
            sock.close()
        sys.exit(1)


    def get_arguments(self):
        getting = argparse.ArgumentParser(description='TCP PORT FINDER')
        getting.add_argument('-l', '--local', dest='local', required=True, help='Victim Ip to scan: Example: ./port_scanner -l 1.1.1.1')
        getting.add_argument('-p', '--port', dest='port', required=True, help='Victim port/ports: Example1: -p 1-100; Example2: -p 80; Example3: -p 22,80,443')
        values = getting.parse_args()

        self.host = values.local
        return values.port

    def creating_socket(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        self.open_sockets.append(sock)

        return sock

    def getting_ports(self, port):

        if '-' in port:
            start, end = map(int, port.split('-'))
            return range(start, end+1)
        elif ',' in port:
            return map(int, port.split(','))
        else:
            return (int(port),)

    def scanning_ports(self, port):

        sock = self.creating_socket()

        try: 
            sock.connect((self.host, port))
            print(colored(f"\n[+] The port {port} is open", 'green'))
        except (socket.timeout, ConnectionRefusedError):
            pass
        finally:
            sock.close()


    def final_test(self, port):

        with ThreadPoolExecutor(max_workers=100) as thport:
            thport.map(self.scanning_ports, port)


def main():

    router = Port_scanner() 

    port = router.get_arguments()
    final_port = router.getting_ports(port)
    router.final_test(final_port)


if __name__ == "__main__":
    main()