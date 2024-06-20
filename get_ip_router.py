#!/usr/bin/env python3

import socket
from termcolor import colored

class FindPort:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def show_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            try:

                s.connect((self.host, self.port))
                print(colored(f"\n[+]The port {self.port} is open", 'green'))

            except (ConnectionRefusedError, socket.timeout):
                print(colored(f"\n[!]The port {self.port} is closed", 'red'))



def get_hp():
    host = input(colored("\n[?]Get me the host: ", 'cyan'))
    port = int(input(colored("\n[?]Get me the port: ", 'cyan')))
    return host, port


def main():

    host, port = get_hp()

    guest1 = FindPort(host, port)
    guest1.show_port()


if __name__ == "__main__":
    main()
