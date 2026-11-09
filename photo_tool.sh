#!/bin/bash

# Auto-Update trigger
bash updater.sh

run_python() {
    python core_tools.py "$@"
}

cat << 'EOF' > core_tools_runner.py
import sys
sys.path.append('.')
from core_tools import *
import os

if __name__ == "__main__":
    while True:
        os.system('clear')
        print("=====================================")
        print("   🕵️‍♂️ CYBER PHOTO TOOLKIT 🕵️‍♂️")
        print("=====================================")
        print("1. Photo mein Secret Message chhipao")
        print("2. Photo se Secret Message nikalo")
        print("3. Photo ko Glitch (Kharab) karo")
        print("4. Photo ko Restore (Sahi) karo")
        print("0. Exit")
        print("=====================================")
        
        choice = input("Apna option chuno (1/2/3/4/0): ")

        if choice == '1':
            img_path = input("\nPhoto ka naam daalo: ")
            msg = input("Kya secret message chhipana hai?: ")
            out_path = input("Nayi photo ka naam (jaise: secret): ")
            hide_message(img_path, msg, out_path)
            input("\nEnter dabao...")
        elif choice == '2':
            img_path = input("\nPhoto ka naam daalo: ")
            extract_message(img_path)
            input("\nEnter dabao...")
        elif choice == '3':
            img_path = input("\nPhoto ka naam daalo: ")
            out_path = input("Kharab photo ka naam (jaise: glitch): ")
            key = input("Secret Key daalo (ise yaad rakhna): ")
            glitch_image(img_path, out_path, key)
            input("\nEnter dabao...")
        elif choice == '4':
            img_path = input("\nGlitch photo ka naam daalo: ")
            out_path = input("Sahi photo ka naam (jaise: fixed): ")
            key = input("Wahi Secret Key daalo: ")
            restore_image(img_path, out_path, key)
            input("\nEnter dabao...")
        elif choice == '0':
            print("Bye!")
            break
EOF

python core_tools_runner.py
