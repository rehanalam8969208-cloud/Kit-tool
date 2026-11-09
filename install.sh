#!/bin/bash

echo "========================================="
echo "   CYBER PHOTO TOOLKIT INSTALLER      "
echo "========================================="

# 1. Update and Install Dependencies
echo "[*] Installing required packages..."
pkg update -y && pkg upgrade -y
pkg install python -y
pkg install libjpeg-turbo -y
pkg install python-pillow -y

# 2. Make tools executable
echo "[*] Setting up permissions..."
chmod +x photo_tool.sh

# 3. Create Shortcut Command (The Magic)
echo "[*] Creating shortcut command 'photo'..."
cat << 'EOF' > $PREFIX/bin/photo
#!/data/data/com.termux/files/usr/bin/bash
# Shortcut to run the Cyber Photo Toolkit
cd $(dirname $(readlink -f $0 2>/dev/null || echo $0))/../home/Cyber-Photo-Toolkit 2>/dev/null || cd ~/Cyber-Photo-Toolkit
bash photo_tool.sh
EOF

chmod +x $PREFIX/bin/photo

echo "========================================="
echo "[+] Installation Complete!"
echo "[+] Ab aap kisi bhi folder se sirf 'photo' type karke tool chala sakte hain."
echo "========================================="
