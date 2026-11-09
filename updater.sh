#!/bin/bash

# Aapka GitHub Repo URL (Dhyan rahe, aakhir mein .git nahi lagana)
REPO_URL="https://github.com/AAPKA_USERNAME/Cyber-Photo-Toolkit.git"

echo "[*] Checking for updates on GitHub..."
cd "$(dirname "$0")"

# Check karo ki kya code git repo hai
if [ -d ".git" ]; then
    # Git se latest changes fetch karo (bina kuch delete kiye)
    git fetch --all > /dev/null 2>&1
    
    # Check karo ki local aur remote mein koi farq (difference) hai ya nahi
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse @{u} 2>/dev/null)
    
    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "[+] Naya update mila hai! Auto-update ho raha hai..."
        git reset --hard origin/main > /dev/null 2>&1
        git pull origin main > /dev/null 2>&1
        echo "[+] Update Successful!"
        chmod +x *.sh
        sleep 1
    else
        echo "[+] Aapka tool pehle se hi latest version par hai."
        sleep 1
    fi
else
    echo "[-] Git repository nahi mili. Update skip."
fi
