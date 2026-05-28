#!/usr/bin/env python3

from termcolor import colored
from pwn import *

import sys, signal, hashlib, argparse, subprocess

class hash_crack:

    def __init__(self):
        self.arguments = self.argument()
        self.wordlist = []
        self.hashed_passwords = []
        self.usernames = []
        signal.signal(signal.SIGINT, self.def_handler)

    def def_handler(self, sig, frame):

        print(colored("[!] Exiting...", 'red'))
        sys.exit(1)

    def argument(self):

        argu = argparse.ArgumentParser(description='HashCrack (md5)')
        argu.add_argument('-pf', '--passwords_file', required=True, dest="passwords_file", help="Write the file of the passwords or passwords separed by , | EX: -pf passwords.txt || -pf has1,has2,has3")
        argu.add_argument('-wl', '--wordlist', required=True, dest="path_wordlist", help="Choose the wordlist you will use")
        argu.add_argument('-us', '--user_in_file', dest="users_file", help="If you want, you Can provide the users for each password (separated by commas or as a file), The md5 password must match with the user, write the password and the user in the same position | EX: -pf has1,has2 -us user_has1,user_has2")

        return argu.parse_args()

    def try_open_file(self, file, list_append):

        try:
            with open(file, 'r', errors='ignore') as data_added:
                for data in data_added.readlines():
                    list_append.append(data.strip())
        except Exception as e:
            print(colored(f"\t\n[!] Could not continue with the program Due to {e}", "red"))
            sys.exit(1)

    def provide_data(self, file, list_append, value=False):

        if(',' in file):
            for data in file.split(','):
                list_append.append(data.strip())
        else:
            self.try_open_file(file, list_append)

    def crack_password(self):

        print(colored(f"\n{'-'*20} Cracked Hashes {'-'*20}\n", "yellow"))

        bar = log.progress("Brute Forcing MD5 Hashes")
        bar.status("[+] Starting \n")
        for index,password in enumerate(self.hashed_passwords):
            for crack_pass in self.wordlist:
                try:
                    username = self.usernames[index] if self.usernames[index] else 'No_User_Provided'
                except IndexError:
                    username = 'No_User_Provide'
                bar.status(f"[-] MD5 HASH: {password} - Username: {username} - Testing: {crack_pass}")
                if(password == hashlib.md5(crack_pass.encode()).hexdigest()):
                    log.success(f"MD5 HASH: {password} - Username {username} - Password: {crack_pass}")
                    break

        bar.success("Brute forcing Finished")

    def print_hashes_users(self):

        print(colored(f"\n{'-'*20} Hashes To crack {'-'*20}\n", "red"))

        for index,hashed_passwd in enumerate(self.hashed_passwords):
            try:
                username = self.usernames[index] if self.usernames[index] else 'No_User_Provied'
            except IndexError:
                username = 'No_User_Provided'
            print(colored(f"\t[?] Username: {username} - MD5_HASH: {hashed_passwd}", "blue"))
        print("\n")

    def check_data(self):

        self.provide_data(self.arguments.passwords_file, self.hashed_passwords)
        self.provide_data(self.arguments.path_wordlist, self.wordlist)
        if (self.arguments.users_file):
            self.provide_data(self.arguments.users_file, self.usernames)
    
        self.print_hashes_users()

        self.crack_password()

def main():

    command = 'figlet "HASH CRACK" | lolcat -f | boxes -d tex-box'
    subprocess.run(command, shell=True)

    poo_cracked = hash_crack()
    poo_cracked.check_data()

if __name__ == "__main__":
    main()
