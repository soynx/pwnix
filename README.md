# pwnix

- **About pwnix**  
  pwnix is a handy Linux tool designed for penetration testers who need to manage and configure network devices easily. Whether you’re listing network interfaces, changing MAC addresses, or setting up advanced features like VLANs and QoS, pwnix has got you covered. It’s built to be straightforward and effective, saving you time during your assessments.  
  **Quick Links:** [ip link man page](https://man7.org/linux/man-pages/man8/ip-link.8.html) | [iptables Tutorial](https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html)

---

- **What pwnix Can Do**  
  - **List Network Interfaces**  
    Quickly see all your network devices (e.g., eth0, wlan0, wlp2s0) using a simple command. This feature gives you an instant overview of your current network setup.  
    **Quick Links:** [ip link usage](https://man7.org/linux/man-pages/man8/ip-link.8.html)
  
  - **Activate Monitor Mode**  
    Easily switch your wireless interface into monitor mode so you can capture raw Wi-Fi traffic—a must-have for wireless testing.  
    **Quick Links:** [airmon-ng documentation](https://www.aircrack-ng.org/doku.php?id=airmon-ng) | [iwconfig man page](https://linux.die.net/man/8/iwconfig)
  
  - **Spoof Your MAC Address**  
    Change your MAC address on the fly with either the built-in commands or tools like macchanger. This is great for hiding your identity or bypassing MAC filters.  
    **Quick Links:** [macchanger GitHub](https://github.com/alobbs/macchanger)
  
  - **Configure IP Addresses**  
    Set a static IP address on any interface. pwnix can flush old settings and apply new ones, letting you simulate different network environments effortlessly.  
    **Quick Links:** [ip address configuration](https://man7.org/linux/man-pages/man8/ip-address.8.html)
  
  - **Block Protocols and IPs**  
    Use iptables to block unwanted protocols (like ICMP, TCP, or UDP) or specific IP addresses. This helps in isolating traffic during tests.  
    **Quick Links:** [iptables man page](https://man7.org/linux/man-pages/man8/iptables.8.html)
  
  - **Manage IP Forwarding**  
    Toggle IP forwarding on and off with a simple command—perfect for turning your machine into a router or firewall when needed.  
    **Quick Links:** [sysctl documentation](https://man7.org/linux/man-pages/man8/sysctl.8.html)
  
  - **DNS and NAT Setup**  
    Easily configure DNS settings and set up NAT (Network Address Translation) to control traffic flow. This is useful for creating testing environments that mimic real-world networks.  
    **Quick Links:** [NAT configuration](https://www.linuxjournal.com/article/10916)
  
  - **Promiscuous Mode**  
    Beyond monitor mode, pwnix lets you enable promiscuous mode so your interface can capture all network packets passing by—ideal for thorough traffic analysis.  
    **Quick Links:** [ip link man page](https://man7.org/linux/man-pages/man8/ip-link.8.html)
  
  - **VLAN Configuration**  
    Create and manage VLANs to segment your network. With this feature, you can easily set up virtual LAN interfaces (like eth0.10) for testing complex network scenarios.  
    **Quick Links:** [VLAN on Linux (ArchWiki)](https://wiki.archlinux.org/title/VLAN)
  
  - **Adjust MTU Settings**  
    Change the Maximum Transmission Unit (MTU) of any network interface. Adjusting MTU can help you optimize performance or troubleshoot packet fragmentation issues.  
    **Quick Links:** [MTU Configuration](https://www.cyberciti.biz/faq/what-is-mtu/)
  
  - **Set Up Basic QoS**  
    Configure Quality of Service (QoS) settings using the `tc` command to manage bandwidth and simulate network conditions. This is a great way to test how your network handles different loads.  
    **Quick Links:** [tc man page](https://man7.org/linux/man-pages/man8/tc.8.html)

- **Installation Made Easy**  
  pwnix comes with an installation script (`install.sh`) that takes care of everything for you. It checks for all necessary dependencies—like Python3, pip3, nmap, aircrack-ng, macchanger, iw, and tc (via iproute2)—and ensures they’re installed correctly. Just run the script, and you’re good to go!  
  **Quick Links:** [iproute2 on Ubuntu](https://packages.ubuntu.com/search?keywords=iproute2)

- **How to Use pwnix**  
  Once installed, simply run the command `pwnix` from anywhere on your system. pwnix is designed with a simple command-line interface that supports multiple subcommands:  
  - `list` – Display all network interfaces.  
  - `monitor` – Enable or disable monitor mode on a wireless interface.  
  - `set-mac` – Change the MAC address for a specific interface.  
  - `set-ip` – Configure a static IP address on an interface.  
  - `block-protocol` – Block a specific protocol on an interface.  
  - `enable-forwarding` / `disable-forwarding` – Turn IP forwarding on or off.  
  - `configure-dns` – Set up DNS for a network interface.  
  - `configure-nat` – Configure NAT on an interface.  
  - `block-ip` – Block traffic from a specified IP address.  
  - `firewall-status` – Display current firewall rules.  
  - `promisc` – Activate or deactivate promiscuous mode.  
  - `configure-vlan` – Create and activate a VLAN on a base interface.  
  - `set-mtu` – Adjust the MTU of an interface.  
  - `configure-qos` – Set up a basic QoS configuration with bandwidth limitations.  
  **Quick Links:** [ArgumentParser documentation](https://docs.python.org/3/library/argparse.html)

- **Getting Involved**  
  We welcome contributions! If you find a bug, have a feature request, or just want to help improve pwnix, please open an issue or submit a pull request on our GitHub repository. Let’s build a better tool together.  
  **Quick Links:** [GitHub Guide to Contributing](https://opensource.guide/how-to-contribute/)

Enjoy using pwnix, and happy testing!

---
## Disclaimer  
This code is provided for **educational and legal security research purposes only**. The author of this repository does not endorse or encourage any illegal activities, including but not limited to unauthorized penetration testing, hacking, or any form of cybercrime.  

By using this code, you agree to the following:  

- You will only use it in environments where you have explicit authorization.  
- You are solely responsible for ensuring compliance with all applicable laws and regulations.  
- The author assumes **no liability** for any misuse of this code or any consequences arising from its use.  
- If you are unsure whether a specific use case is legal, consult a legal professional before proceeding.  

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. This means:  

- Any modifications or derivative works must be open-source under the same license.  
- If you use this software as part of a service accessible over a network, you must also provide access to the source code.  
- **This license does NOT grant permission to use the software for illegal activities.**  

For full license details, see the [AGPL-3.0 License](LICENSE).  

---