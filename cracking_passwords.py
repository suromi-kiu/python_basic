#!/usr/bin/env python3

from termcolor import colored
import sys, signal, hashlib, argparse, subprocess

class md5_hash_cracking:

    def __init__(self):

        self.cracked_passwords = {}
        self.arguments = self.argument()

        signal.signal(signal.SIGINT, self.def_handler)

    def def_handler(self, one, two):

        print(colored("[!] Exiting...", 'red'))
        sys.exit(1)

    def argument(self):

        argu = argparse.ArgumentParser(description='Tool to Execute force Bruting')
        argu.add_argument('-uf', '--users_in_file', dest="users_file", help="Provide the file which contains user for passwords (The data have to be matched with password, It means, same position in file)")
        argu.add_argument('-ft', '--file-target', required=True, dest="user_target", help="Write the file which contains the md5 passwords")
        argu.add_argument('-wl', '--word-list', required=True, dest="path_wordlist", help="Write the path of the wordlist that you will use to crack the md5 passwords")
        return argu.parse_args()

    def cracking(self):
        
        with open(self.arguments.user_target, 'r') as passwords:
            for password in passwords.readlines():
                dictionary = open(self.arguments.path_wordlist, 'rb')
                for dit_passwords in dictionary.readlines():
                    if (password.strip() == hashlib.md5(dit_passwords.strip()).hexdigest()):
                        self.cracked_passwords[password.strip()] = dit_passwords.decode().strip()
                        break

    def cracking_hash(self):

        command = 'figlet "HASH CRACK" | lolcat -f | boxes -d tex-box'
        subprocess.run(command, shell=True)
        print(colored(f"\n{'-'*20}Printing Data{'-'*20}\n","blue"))
        self.cracking()

        if self.arguments.users_file:
            enumed_users = []
            log_uer = 0
            with open(self.arguments.users_file, 'r') as users:
                for user in users.readlines():
                    enumed_users.append(user)
            for y,x in self.cracked_passwords.items():
                print(colored(f"[+] MD5 Value: {y} - User: {enumed_users[log_uer].strip()} - Password: {x}", "green"))
                log_uer += 1
        else:
            for y,x in self.cracked_passwords.items():
                print(colored(f"[+] MD5 Value {y} -- Decoded: {x}", 'green'))

def main():

    crack_hash = md5_hash_cracking()
    crack_hash.cracking_hash()

if __name__ == "__main__":

    main()
