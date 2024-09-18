import psutil
import subprocess
import platform
import datetime
import sys
from scapy.all import sr1, IP, ICMP, TCP
import os
import socket
import random
import pyfiglet

# Text to display
text = "Agentless Hacker"

# All ASCII art and text from the Metasploit theme, Rabbit, Skull, and "I love you" designs
ascii_art_list = [
    # AL Hacker 2
    r'''
               .;lxO0KXXXK0Oxl:.
           ,o0WMMMMMMMMMMMMMMMMMMKd,
        'xNMMMMMMMMMMMMMMMMMMMMMMMMMWx,
      :KMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMK:
    .KMMMMMMMMMMMMMMMWNNNWMMMMMMMMMMMMMMMX,
   lWMMMMMMMMMMMXd:..     ..;dKMMMMMMMMMMMMo
  xMMMMMMMMMMWd.               .oNMMMMMMMMMMk
 oMMMMMMMMMMx.                    dMMMMMMMMMMx
.WMMMMMMMMM:                       :MMMMMMMMMM,
xMMMMMMMMMo                         lMMMMMMMMMO
NMMMMMMMMW                    ,cccccoMMMMMMMMMWlccccc;
MMMMMMMMMX                     ;KMMMMMMMMMMMMMMMMMMX:
NMMMMMMMMW.                      ;KMMMMMMMMMMMMMMX:
xMMMMMMMMMd                        ,0MMMMMMMMMMK;
.WMMMMMMMMMc                         'OMMMMMM0,
 lMMMMMMMMMMk.                         .kMMO'
  dMMMMMMMMMMWd'                         ..
   cWMMMMMMMMMMMNxc'.                ##########
    .0MMMMMMMMMMMMMMMMWc            #+#    #+#
      ;0MMMMMMMMMMMMMMMo.          +:+
        .dNMMMMMMMMMMMMo          +#++:++#+
           'oOWMMMMMMMMo                +:+
               .,cdkO0K;        :+:    :+:                                
                                :::::::+:
                      AL Hacker
    ''',
    # Metasploit ASCII Art
    r'''
         d88888b db    db d88888b d8b   db d888888b d888888b 
         88'     88    88 88'     888o  88   `88'   `~88~' 
         88ooooo 88    88 88ooooo 88V8o 88    88       88    
         88~~~~~ 88    88 88~~~~~ 88 V8o88    88       88    
         88.     88b  d88 88.     88  V888   .88.      88    
         Y88888P ~Y8888P' Y88888P VP   V8P Y888888P    YP    
                Agentless Hacker by Rapid7     
    ''',
    # Skull ASCII Art
    r'''
                      ########                  #
                      #################            #
                   ######################         #
                  #########################      #
                ############################
               ##############################
               ###############################
              ###############################
              ##############################
                              #    ########   #
                 ##        ###        ####   ##
                                      ###   ###
                                    ####   ###
               ####          ##########   ####
               #######################   ####
                 ####################   ####
                  ##################  ####
                    ############      ##
                       ########        ###
                      #########        #####
                    ############      ######
                   ########      #########
                     #####       ########
                       ###       #########
                      ######    ############
                     #######################
                     #   #   ###  #   #   ##
                     ########################
                      ##     ##   ##     ##
                            https://Agentless-Hacker.com
    ''',
    # Rabbit ASCII Art
    r'''
                        (`.         ,-,
                        ` `.    ,;' /
                         `.  ,'/ .'
                          `. X /.'
                .-;--''--.._` ` (
              .'            /   `
             ,           ` '   Q '            ======Agentless Hacker======
             ,         ,   `._    \
          ,.|         '     `-.;_'
           ' `    ,   )   .'
              `._ ,  '   /_
                 ; ,''-,;' ``-
                  `-..__--
    ''',
    # I love you ASCII Art
    r'''
IIIIII    dTb.dTb        .---.
  II     4'  v  'B   .'"".'/|\`.""'.
  II     6.     .P  :  .' / | \ `.  :
  II     'T;. .;P'  '.'  /  |  \  `.'
  II      'T; ;P'    `. /   |   \ .'
IIIIII     'YvP'       `-.|.-'

I love shells --egypt @ Agentless-Hacker
    '''
]

# Function to create and display random text art
def generate_text_art(text):
    fonts = pyfiglet.FigletFont.getFonts()
    random_font = random.choice(fonts)
    fig = pyfiglet.Figlet(font=random_font)
    art_text = fig.renderText(text)
    return art_text

# Function to display a random ASCII image
def display_random_ascii_image():
    random_image = random.choice(ascii_art_list)
    print(random_image)

# Generate and display the text art
print(generate_text_art(text))

# Display a random ASCII image below the text
display_random_ascii_image()

# Initialize system information
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
    firewall_rules = subprocess.run(["sudo", "ufw", "status"], capture_output=True, text=True)
    if "inactive" in firewall_rules.stdout:
        firewall_issues.append("Firewall is inactive, check security settings.")
    return firewall_issues

# Check UAC settings from the system configuration
def check_uac_settings():
    uac_issues = []
    try:
        uac_status = subprocess.run(["sudo", "getenforce"], capture_output=True, text=True)
        if "Disabled" in uac_status.stdout:
            uac_issues.append("SELinux is disabled. This can expose the system to vulnerabilities.")
    except Exception as e:
        uac_issues.append(f"Could not read UAC settings: {str(e)}")
    return uac_issues

# Function to aggregate vulnerability checks
def check_vulnerabilities():
    vulnerabilities = []
    vulnerabilities.extend(check_firewall_rules())
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
    import pdfkit
    config = pdfkit.configuration()
    pdfkit.from_string(html_content, 'vulnerability_report.pdf', configuration=config)

# Admin check function
def is_admin():
    return os.geteuid() == 0

# Main function with console interface
def main():
    while True:
        print("\nWelcome to the Agent-less Linux Vulnerability and Network Scanner!")
        print("1. System Vulnerability Check")
        print("2. Network Open Port Scan")
        print("3. Network Topology Scan")
        print("4. Generate Full Report")
        print("5. Exit")
        choice = input("Select an option (1-5): ")

        if choice == '5':
            print("Exiting the program. Goodbye!")
            break

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

if _name_ == "_main_":
    if is_admin():
        main()
    else:
        print("This script requires administrative privileges. Please run as root.")
  sys.exit()