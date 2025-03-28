#!/bin/bash

# Function to check if a command is available
command_exists() {
    command -v "$1" &>/dev/null
}

# Function to install Python 3 and pip
install_python() {
    if ! command_exists python3; then
        echo "[*] Installing python3..."
        sudo apt-get install python3 -y || { echo "[✘] Failed to install python3."; return 1; }
    else
        echo "[✔] python3 is already installed."
    fi

    if ! command_exists pip3; then
        echo "[*] Installing pip3..."
        sudo apt-get install python3-pip -y || { echo "[✘] Failed to install pip3."; return 1; }
    else
        echo "[✔] pip3 is already installed."
    fi
}

# Function to install necessary tools for penetration testing
install_tools() {
    echo "[*] Checking and installing necessary tools..."

    # Check for required tools and install if necessary
    if ! command_exists nmap; then
        echo "[*] Installing nmap..."
        sudo apt-get install nmap -y || { echo "[✘] Failed to install nmap."; return 1; }
    else
        echo "[✔] nmap is already installed."
    fi

    if ! command_exists aircrack-ng; then
        echo "[*] Installing aircrack-ng..."
        sudo apt-get install aircrack-ng -y || { echo "[✘] Failed to install aircrack-ng."; return 1; }
    else
        echo "[✔] aircrack-ng is already installed."
    fi

    if ! command_exists macchanger; then
        echo "[*] Installing macchanger..."
        sudo apt-get install macchanger -y || { echo "[✘] Failed to install macchanger."; return 1; }
    else
        echo "[✔] macchanger is already installed."
    fi

    if ! command_exists iw; then
        echo "[*] Installing iw..."
        sudo apt-get install iw -y || { echo "[✘] Failed to install iw."; return 1; }
    else
        echo "[✔] iw is already installed."
    fi

    if ! command_exists arpspoof; then
        echo "[*] Installing dsniff (for arpspoof)..."
        sudo apt-get install dsniff -y || { echo "[✘] Failed to install arpspoof (dsniff)."; return 1; }
    else
        echo "[✔] arpspoof (dsniff) is already installed."
    fi

    if ! command_exists airbase-ng; then
        echo "[*] Installing airbase-ng (part of aircrack-ng package)..."
        sudo apt-get install airbase-ng -y || { echo "[✘] Failed to install airbase-ng."; return 1; }
    else
        echo "[✔] airbase-ng is already installed."
    fi

    if ! command_exists airodump-ng; then
        echo "[*] Installing airodump-ng (part of aircrack-ng package)..."
        sudo apt-get install airodump-ng -y || { echo "[✘] Failed to install airodump-ng."; return 1; }
    else
        echo "[✔] airodump-ng is already installed."
    fi

    # --- Zusätzliche Installation für neue Features ---

    if ! command_exists tc; then
        echo "[*] Installing tc (provided by iproute2)..."
        sudo apt-get install iproute2 -y || { echo "[✘] Failed to install iproute2 (tc)."; return 1; }
    else
        echo "[✔] tc is already installed."
    fi
}

# Install Python dependencies
install_python

# Install required tools for penetration testing
install_tools

# Copy the pwnix script to /usr/local/bin
echo "[*] Copying pwnix script to /usr/local/bin..."
if sudo cp pwnix.py /usr/local/bin/pwnix; then
    sudo chmod +x /usr/local/bin/pwnix
    echo "[✔] pwnix script copied to /usr/local/bin and is executable."
else
    echo "[✘] Failed to copy pwnix script to /usr/local/bin."
    exit 1
fi

# Install additional Python packages
echo "[*] Installing Python dependencies..."
if sudo pip3 install scapy; then
    echo "[✔] scapy Python package installed."
else
    echo "[✘] Failed to install scapy Python package."
    exit 1
fi

# Verify the installation of pwnix
if command_exists pwnix; then
    echo "[✔] pwnix has been successfully installed and is executable from anywhere."
else
    echo "[✘] pwnix installation failed. Please check the logs for more details."
    exit 1
fi

# Final check-up to ensure everything was installed correctly
echo "[*] Final verification: Checking installed tools..."

# Check if all required tools are installed
tools=("nmap" "aircrack-ng" "macchanger" "iw" "arpspoof" "airbase-ng" "airodump-ng" "scapy" "pwnix" "tc")

for tool in "${tools[@]}"; do
    if ! command_exists "$tool"; then
        echo "[✘] $tool is missing. Installation failed!"
        exit 1
    else
        echo "[✔] $tool is installed."
    fi
done

# End of installation
echo "[✔] Installation complete!"
