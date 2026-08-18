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
    host_port = input("Enter your LPORT: ")
    payload_name = input("Enter your payload name(For example: explorer):\n")
    print(f"Setting LHOST to {lhost}")
    print(f"Setting LPORT to {host_port}")
    print(f"Setting payload name to: {payload_name}.exe")




host_ip = get_user_ip()
get_user_target(host_ip)

