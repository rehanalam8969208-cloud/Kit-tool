#!/bin/bash
echo "====================================="
echo "  CYBER PHOTO TOOLKIT INSTALLER      "
echo "====================================="
pkg update && pkg upgrade -y
pkg install python -y
pkg install libjpeg-turbo -y
pkg install python-pillow -y
echo "[+] Setup Complete! Ab aap tool chala sakte hain."
chmod +x photo_tool.sh
