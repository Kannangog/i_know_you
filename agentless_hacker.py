import wmi
import socket
import psutil
import platform
from datetime import datetime
import subprocess
import winreg
import pdfkit
from scapy.all import sr1, IP, ICMP, TCP
import ctypes
import sys

# Initialize WMI object
c = wmi.WMI()

# Function to gather basic system information
def get_system_info():
    system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.machine(),
        "Hostname": platform.node(),
        "CPU": platform.processor(),
        "RAM (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2)
    }
    return system_info

# Function to gather details about installed hotfixes
def get_hotfixes():
    hotfixes = []
    for hotfix in c.Win32_QuickFixEngineering():
        hotfixes.append(hotfix.Description)
    return hotfixes

# Function to gather network information
def get_network_info():
    network_info = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                network_info.append({
                    "Interface": interface,
                    "IP Address": addr.address
                })
    return network_info

# Check firewall settings
def check_firewall_rules():
    firewall_issues = []
    firewall_rules = subprocess.run(["powershell", "Get-NetFirewallRule"], capture_output=True, text=True)
    if "Disabled" in firewall_rules.stdout:
        firewall_issues.append("Some firewall rules are disabled, check security settings.")
    return firewall_issues

# Check Windows Defender settings
def check_windows_defender():
    defender_issues = []
    defender_settings = subprocess.run(["powershell", "Get-MpPreference"], capture_output=True, text=True)
    if "DisableRealtimeMonitoring : True" in defender_settings.stdout:
        defender_issues.append("Windows Defender real-time protection is disabled!")
    return defender_issues

# Check UAC settings from the registry
def check_uac_settings():
    uac_issues = []
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, "EnableLUA")
        if value == 0:
            uac_issues.append("User Account Control (UAC) is disabled. This can expose the system to vulnerabilities.")
    except Exception as e:
        uac_issues.append(f"Could not read UAC settings: {str(e)}")
    return uac_issues

# Function to aggregate vulnerability checks
def check_vulnerabilities():
    vulnerabilities = []
    vulnerabilities.extend(check_firewall_rules())
    vulnerabilities.extend(check_windows_defender())
    vulnerabilities.extend(check_uac_settings())
    return vulnerabilities

# Function to scan open ports on a host (user provides IP)
def scan_open_ports(target_ip):
    open_ports = []
    for port in range(20, 1025):
        pkt = sr1(IP(dst=target_ip)/TCP(dport=port,flags="S"),timeout=0.5,verbose=0)
        if pkt and pkt.haslayer(TCP) and pkt.getlayer(TCP).flags == 0x12:  # SYN-ACK response
            open_ports.append(port)
    return open_ports

# Function to map connected devices in the local network (user provides subnet)
def network_topology_scan(subnet):
    devices = []
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        response = sr1(IP(dst=ip)/ICMP(), timeout=1, verbose=0)
        if response:
            devices.append(ip)
    return devices

# Function to generate a PDF report
def generate_pdf_report(system_info, network_info, vulnerabilities, target_ip, open_ports, network_devices):
    # Create HTML content for the report
    html_content = f"""
    <html>
    <head>
        <title>System Vulnerability Report</title>
    </head>
    <body>
        <h1>System Vulnerability Report</h1>
        <h2>System Information</h2>
        <ul>
    """
    for key, value in system_info.items():
        html_content += f"<li>{key}: {value}</li>"
    
    html_content += "</ul><h2>Network Information</h2><ul>"
    
    for net in network_info:
        html_content += f"<li>Interface: {net['Interface']}, IP Address: {net['IP Address']}</li>"
    
    html_content += "</ul><h2>Vulnerability Report</h2><ul>"
    
    if vulnerabilities:
        for vuln in vulnerabilities:
            html_content += f"<li>{vuln}</li>"
    else:
        html_content += "<li>No critical vulnerabilities found!</li>"
    
    html_content += f"</ul><h2>Open Ports on {target_ip}</h2><ul>"
    for port in open_ports:
        html_content += f"<li>Port: {port} is open</li>"
    
    html_content += "</ul><h2>Network Devices Detected</h2><ul>"
    for device in network_devices:
        html_content += f"<li>Device IP: {device}</li>"
    
    html_content += "</ul></body></html>"
    
    # Save HTML to PDF
    pdfkit.from_string(html_content, 'vulnerability_report.pdf')

# Admin check function
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Main function with console interface
def main():
    print("\nWelcome to the Agent-less Windows Vulnerability and Network Scanner!")
    print("1. System Vulnerability Check")
    print("2. Network Open Port Scan")
    print("3. Network Topology Scan")
    print("4. Generate Full Report")
    choice = input("Select an option (1-4): ")

    # Gather system information
    system_info = get_system_info()
    network_info = get_network_info()
    vulnerabilities = []
    open_ports = []
    network_devices = []
    target_ip = ""

    if choice == '1':
        print("\nRunning System Vulnerability Check...\n")
        vulnerabilities = check_vulnerabilities()
        if vulnerabilities:
            for vuln in vulnerabilities:
                print(f"Vulnerability: {vuln}")
        else:
            print("No critical vulnerabilities found!")
    
    elif choice == '2':
        target_ip = input("Enter the target IP address for open port scan: ")
        print(f"\nScanning open ports on {target_ip}...\n")
        open_ports = scan_open_ports(target_ip)
        if open_ports:
            for port in open_ports:
                print(f"Port {port} is open.")
        else:
            print(f"No open ports found on {target_ip}.")

    elif choice == '3':
        subnet = input("Enter the subnet (e.g., 192.168.1): ")
        print(f"\nScanning devices on subnet {subnet}...\n")
        network_devices = network_topology_scan(subnet)
        if network_devices:
            for device in network_devices:
                print(f"Device found: {device}")
        else:
            print(f"No devices found on subnet {subnet}.")

    elif choice == '4':
        target_ip = input("Enter the target IP address for full scan: ")
        print(f"\nRunning full scan on {target_ip}...\n")
        
        vulnerabilities = check_vulnerabilities()
        open_ports = scan_open_ports(target_ip)
        subnet = '.'.join(target_ip.split('.')[:-1])  # Assuming IP is in /24 subnet
        network_devices = network_topology_scan(subnet)
        
        # Generate PDF report
        generate_pdf_report(system_info, network_info, vulnerabilities, target_ip, open_ports, network_devices)
        print("\nFull scan complete. Report saved as 'vulnerability_report.pdf'.")

if __name__ == "__main__":
    if is_admin():
        main()
    else:
        print("This script requires administrative privileges. Please run as an Administrator.")
        sys.exit()
