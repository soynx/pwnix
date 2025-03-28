#!/usr/bin/env python3
import argparse
import subprocess
import sys
import shutil
import os
import logging
import random

# Setup logging
LOG_FILE = os.path.expanduser("~/.pwnix.log")
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def check_tool(tool):
    """Check if a given tool is available on the system."""
    if shutil.which(tool) is None:
        logging.error(f"Required tool '{tool}' is not installed or not in PATH.")
        print(f"[ERROR] Required tool '{tool}' is not installed or not in PATH.")
        sys.exit(1)


def require_root():
    """Check if the script is run with root privileges."""
    if os.geteuid() != 0:
        logging.error("This operation requires root privileges. Please run as root or with sudo.")
        print("[ERROR] This operation requires root privileges. Please run as root or with sudo.", file=sys.stderr)
        sys.exit(1)


def run_command(cmd):
    """Execute a system command and return its output."""
    try:
        logging.debug(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {' '.join(cmd)}")
        logging.error(f"Error output: {e.stderr.strip()}")
        print(f"[ERROR] Command failed: {' '.join(cmd)}")
        print(f"[ERROR] Error output: {e.stderr.strip()}")
        sys.exit(1)


# Network Commands

def list_interfaces(args):
    check_tool("ip")
    output = run_command(["ip", "link", "show"])
    print(output)


def set_monitor_mode(args):
    require_root()
    check_tool("iw")
    if args.enable:
        cmd = ["iw", "dev", args.interface, "set", "type", "monitor"]
        action = "enabling"
    else:
        cmd = ["iw", "dev", args.interface, "set", "type", "managed"]
        action = "disabling"

    print(f"[INFO] {action.capitalize()} monitor mode for interface {args.interface}")
    run_command(cmd)


def change_mac(args):
    require_root()
    check_tool("ip")
    print(f"[INFO] Changing MAC address of {args.interface} to {args.new_mac}")
    run_command(["ip", "link", "set", "dev", args.interface, "down"])
    run_command(["ip", "link", "set", "dev", args.interface, "address", args.new_mac])
    run_command(["ip", "link", "set", "dev", args.interface, "up"])
    print("[INFO] MAC address changed successfully.")

def set_mac_random(args):
    """
    Generate a random MAC address and set it for the given interface.
    The MAC address is generated as locally administered and unicast.
    """
    require_root()
    check_tool("ip")
    # Generate a random MAC address:
    # - The first octet is forced to be locally administered and unicast.
    first_octet = (random.randint(0x00, 0xff) & 0xfc) | 0x02
    mac = [first_octet] + [random.randint(0x00, 0xff) for _ in range(5)]
    new_mac = ':'.join(f"{octet:02x}" for octet in mac)
    print(f"[INFO] Changing MAC address of {args.interface} to {new_mac} (random)")
    run_command(["ip", "link", "set", "dev", args.interface, "down"])
    run_command(["ip", "link", "set", "dev", args.interface, "address", new_mac])
    run_command(["ip", "link", "set", "dev", args.interface, "up"])
    print("[INFO] Random MAC address set successfully.")


def set_ip(args):
    require_root()
    check_tool("ip")
    netmask = args.netmask if args.netmask else "24"
    ip_with_mask = f"{args.ip}/{netmask}"
    print(f"[INFO] Setting IP address {ip_with_mask} for interface {args.interface}")
    run_command(["ip", "addr", "flush", "dev", args.interface])
    run_command(["ip", "addr", "add", ip_with_mask, "dev", args.interface])
    print("[INFO] IP address set successfully.")


def block_protocol(args):
    require_root()
    check_tool("iptables")
    print(f"[INFO] Blocking protocol {args.protocol} on interface {args.interface}")
    run_command(["iptables", "-A", "INPUT", "-i", args.interface, "-p", args.protocol, "-j", "DROP"])
    print("[INFO] Protocol blocked successfully.")


def enable_ip_forwarding(args):
    require_root()
    check_tool("sysctl")
    print(f"[INFO] Enabling IP forwarding...")
    run_command(["sysctl", "-w", "net.ipv4.ip_forward=1"])
    print("[INFO] IP forwarding enabled.")


def disable_ip_forwarding(args):
    require_root()
    check_tool("sysctl")
    print(f"[INFO] Disabling IP forwarding...")
    run_command(["sysctl", "-w", "net.ipv4.ip_forward=0"])
    print("[INFO] IP forwarding disabled.")


def configure_dns(args):
    require_root()
    check_tool("resolvconf")
    print(f"[INFO] Configuring DNS to {args.dns_server}")
    run_command(["resolvconf", "-a", args.interface, "-m", "0", "-n", args.dns_server])
    print(f"[INFO] DNS configured to {args.dns_server}")


def nat_configure(args):
    require_root()
    check_tool("iptables")
    print(f"[INFO] Configuring NAT with {args.interface}")
    run_command(["iptables", "-t", "nat", "-A", "POSTROUTING", "-o", args.interface, "-j", "MASQUERADE"])
    print("[INFO] NAT configuration completed.")


def block_ip(args):
    require_root()
    check_tool("iptables")
    print(f"[INFO] Blocking IP {args.ip} on interface {args.interface}")
    run_command(["iptables", "-A", "INPUT", "-i", args.interface, "-s", args.ip, "-j", "DROP"])
    print(f"[INFO] IP {args.ip} blocked.")


def firewall_status(args):
    check_tool("iptables")
    output = run_command(["iptables", "-L"])
    print(f"[INFO] Current firewall status:\n{output}")

def set_promiscuous_mode(args):
    """Enable or disable promiscuous mode on an interface."""
    require_root()
    check_tool("ip")
    state = "on" if args.enable else "off"
    print(f"[INFO] Setting promiscuous mode {state} for interface {args.interface}")
    run_command(["ip", "link", "set", "dev", args.interface, "promisc", state])
    print(f"[INFO] Promiscuous mode {state}.")


def configure_vlan(args):
    """Configure a VLAN on a given interface."""
    require_root()
    check_tool("ip")
    vlan_interface = f"{args.interface}.{args.vlan_id}"
    print(f"[INFO] Configuring VLAN {args.vlan_id} on interface {args.interface} as {vlan_interface}")
    run_command(["ip", "link", "add", "link", args.interface, "name", vlan_interface, "type", "vlan", "id", args.vlan_id])
    run_command(["ip", "link", "set", vlan_interface, "up"])
    print("[INFO] VLAN configured successfully.")


def set_mtu(args):
    """Set the MTU for a given interface."""
    require_root()
    check_tool("ip")
    print(f"[INFO] Setting MTU for interface {args.interface} to {args.mtu}")
    run_command(["ip", "link", "set", "dev", args.interface, "mtu", args.mtu])
    print("[INFO] MTU set successfully.")


def configure_qos(args):
    """Configure basic QoS using tc on a given interface."""
    require_root()
    check_tool("tc")
    print(f"[INFO] Configuring QoS on interface {args.interface} with rate limit {args.rate}")
    # Delete any existing qdisc to avoid conflicts
    run_command(["tc", "qdisc", "del", "dev", args.interface, "root"])
    # Add a basic HTB qdisc
    run_command(["tc", "qdisc", "add", "dev", args.interface, "root", "handle", "1:", "htb", "default", "30"])
    # Add a class with the specified rate limit
    run_command(["tc", "class", "add", "dev", args.interface, "parent", "1:", "classid", "1:1", "htb", "rate", args.rate])
    print("[INFO] QoS configured successfully.")




# Argument Parsing Setup
def main():
    parser = argparse.ArgumentParser(description="Network management tool with various features for penetration testing.")
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    subparsers.required = True

    # Network Interface commands
    parser_list = subparsers.add_parser("list", help="List all network interfaces")
    parser_list.set_defaults(func=list_interfaces)

    parser_monitor = subparsers.add_parser("monitor", help="Enable or disable monitor mode on a wireless interface")
    parser_monitor.add_argument("interface", help="Wireless interface name (e.g., wlan0)")
    group = parser_monitor.add_mutually_exclusive_group(required=True)
    group.add_argument("--enable", action="store_true", help="Enable monitor mode")
    group.add_argument("--disable", action="store_false", dest="enable", help="Disable monitor mode (set to managed mode)")
    parser_monitor.set_defaults(func=set_monitor_mode)

    parser_mac = subparsers.add_parser("set-mac", help="Change the MAC address of an interface")
    parser_mac.add_argument("interface", help="Interface for which to change the MAC address")
    parser_mac.add_argument("new_mac", help="New MAC address (format: xx:xx:xx:xx:xx:xx)")
    parser_mac.set_defaults(func=change_mac)

    parser_mac_rnd = subparsers.add_parser("set-mac-rnd", help="Set a random MAC address for an interface")
    parser_mac_rnd.add_argument("interface", help="Interface for which to set a random MAC address")
    parser_mac_rnd.set_defaults(func=set_mac_random)

    parser_ip = subparsers.add_parser("set-ip", help="Set a specific IP address for an interface")
    parser_ip.add_argument("interface", help="Interface for which the IP address will be set")
    parser_ip.add_argument("ip", help="IP address to set")
    parser_ip.add_argument("--netmask", help="Netmask (default: 24)", default="24")
    parser_ip.set_defaults(func=set_ip)

    parser_block = subparsers.add_parser("block-protocol", help="Block a specific protocol on an interface")
    parser_block.add_argument("interface", help="Interface on which to block the protocol")
    parser_block.add_argument("protocol", help="Protocol to block (e.g., icmp, tcp, udp)")
    parser_block.set_defaults(func=block_protocol)

    # IP Forwarding
    parser_enable_forwarding = subparsers.add_parser("enable-forwarding", help="Enable IP forwarding")
    parser_enable_forwarding.set_defaults(func=enable_ip_forwarding)

    parser_disable_forwarding = subparsers.add_parser("disable-forwarding", help="Disable IP forwarding")
    parser_disable_forwarding.set_defaults(func=disable_ip_forwarding)

    # DNS Configuration
    parser_dns = subparsers.add_parser("configure-dns", help="Configure DNS server for an interface")
    parser_dns.add_argument("interface", help="Interface name to configure DNS")
    parser_dns.add_argument("dns_server", help="DNS server IP address")
    parser_dns.set_defaults(func=configure_dns)

    # NAT Configuration
    parser_nat = subparsers.add_parser("configure-nat", help="Configure NAT (Network Address Translation)")
    parser_nat.add_argument("interface", help="Interface for NAT")
    parser_nat.set_defaults(func=nat_configure)

    # Block IP
    parser_block_ip = subparsers.add_parser("block-ip", help="Block a specific IP address on an interface")
    parser_block_ip.add_argument("interface", help="Interface on which to block the IP")
    parser_block_ip.add_argument("ip", help="IP address to block")
    parser_block_ip.set_defaults(func=block_ip)

    # Firewall Status
    parser_firewall = subparsers.add_parser("firewall-status", help="Show current firewall status")
    parser_firewall.set_defaults(func=firewall_status)

    # NEW FEATURES 1.3.8:
    parser_promisc = subparsers.add_parser("promisc", help="Enable or disable promiscuous mode on an interface")
    parser_promisc.add_argument("interface", help="Interface to set promiscuous mode")
    group_promisc = parser_promisc.add_mutually_exclusive_group(required=True)
    group_promisc.add_argument("--enable", action="store_true", help="Enable promiscuous mode")
    group_promisc.add_argument("--disable", action="store_false", dest="enable", help="Disable promiscuous mode")
    parser_promisc.set_defaults(func=set_promiscuous_mode)

    parser_vlan = subparsers.add_parser("configure-vlan", help="Configure a VLAN on an interface")
    parser_vlan.add_argument("interface", help="Base interface (e.g., eth0)")
    parser_vlan.add_argument("vlan_id", help="VLAN ID to configure")
    parser_vlan.set_defaults(func=configure_vlan)

    parser_mtu = subparsers.add_parser("set-mtu", help="Set the MTU for an interface")
    parser_mtu.add_argument("interface", help="Interface name")
    parser_mtu.add_argument("mtu", help="MTU value (e.g., 1500)")
    parser_mtu.set_defaults(func=set_mtu)

    parser_qos = subparsers.add_parser("configure-qos", help="Configure basic QoS on an interface")
    parser_qos.add_argument("interface", help="Interface name")
    parser_qos.add_argument("rate", help="Rate limit (e.g., 1mbit)")
    parser_qos.set_defaults(func=configure_qos)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
