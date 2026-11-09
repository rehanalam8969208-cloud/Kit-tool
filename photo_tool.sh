#!/bin/bash

# Auto-Update trigger
bash updater.sh

run_python() {
    python core_tools.py "$@"
}

cat << 'EOF' > core_tools_runner.py
import sys
import os
import time

# --- HACKER THEME COLORS ---
GREEN = '\033[1;32m'
CYAN = '\033[1;36m'
RED = '\033[1;31m'
YELLOW = '\033[1;33m'
RESET = '\033[0m'

sys.path.append('.')
from core_tools import *

def hacker_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(GREEN + char + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

if __name__ == "__main__":
    while True:
        os.system('clear')
        print(CYAN + "=============================================" + RESET)
        print(GREEN + "    _  _   _   ___ _  _____ ___ " + RESET)
        print(GREEN + "   | || | /_\\ / __| |/ / __| _ \\" + RESET)
        print(GREEN + "   | __ |/ _ \\ (__| ' <| _||   /" + RESET)
        print(GREEN + "   |_||_/_/ \\_\\___|_|\\_\\___|_|_\\" + RESET)
        print(CYAN + "=============================================" + RESET)
        print(YELLOW + "      [ CYBER PHOTO TOOLKIT v1.0 ]" + RESET)
        print(CYAN + "=============================================" + RESET)
        print(GREEN + "  [1]" + RESET + " Photo mein Secret Message chhipao")
        print(GREEN + "  [2]" + RESET + " Photo se Secret Message nikalo")
        print(GREEN + "  [3]" + RESET + " Photo ko Glitch (Kharab) karo")
        print(GREEN + "  [4]" + RESET + " Photo ko Restore (Sahi) karo")
        print(RED + "  [0]" + RESET + " System Exit")
        print(CYAN + "=============================================" + RESET)
        
        choice = input(YELLOW + "root@termux:~# " + RESET)

        if choice == '1':
            print(CYAN + "\n[+] Initializing Stego Module..." + RESET)
            img_path = input(GREEN + "Enter Photo Name > " + RESET)
            msg = input(GREEN + "Enter Secret Payload > " + RESET)
            out_path = input(GREEN + "Save As (e.g. secret) > " + RESET)
            hide_message(img_path, msg, out_path)
            input(YELLOW + "\n[Press ENTER to return...]" + RESET)
            
        elif choice == '2':
            print(CYAN + "\n[+] Extracting Payload..." + RESET)
            img_path = input(GREEN + "Enter Photo Name > " + RESET)
            extract_message(img_path)
            input(YELLOW + "\n[Press ENTER to return...]" + RESET)
            
        elif choice == '3':
            print(CYAN + "\n[+] Bypassing Security... Glitching Image..." + RESET)
            img_path = input(GREEN + "Enter Photo Name > " + RESET)
            out_path = input(GREEN + "Save As (e.g. glitch) > " + RESET)
            key = input(GREEN + "Set Encryption Key > " + RESET)
            glitch_image(img_path, out_path, key)
            input(YELLOW + "\n[Press ENTER to return...]" + RESET)
            
        elif choice == '4':
            print(CYAN + "\n[+] Decrypting Pixels..." + RESET)
            img_path = input(GREEN + "Enter Glitched Photo > " + RESET)
            out_path = input(GREEN + "Save As (e.g. fixed) > " + RESET)
            key = input(GREEN + "Enter Encryption Key > " + RESET)
            restore_image(img_path, out_path, key)
            input(YELLOW + "\n[Press ENTER to return...]" + RESET)
            
        elif choice == '0':
            print(RED + "\n[!] Terminating Session... Goodbye." + RESET)
            break
        else:
            print(RED + "\n[-] Access Denied! Invalid Command." + RESET)
            time.sleep(1)
EOF

python core_tools_runner.py
