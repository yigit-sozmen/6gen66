6gen66

6gen66 is a C++ framework that creates a persistent, network-aware payload through a shell-based generator script. It automates the creation of encrypted Windows binaries (via Mingw-w64) that utilize XOR-obfuscated shellcode, process injection into searchindexer.exe, and persistence via the Windows Registry.
Repository Structure

    6gen66.sh: The main TUI that orchestrates SSL generation, payload creation, encryption, and compilation.

    wrapper.cpp: The C++ source that handles network-readiness checks, process injection (APC Queuing), and "Run" key persistence.

    encryptor.py: A utility that takes raw shellcode and generates a payload.h file with an XOR-encrypted byte array.

    resource.rc: Version information metadata to make the generated binary appear as a legitimate "Windows Service Host Update" by Microsoft.

    handler.rc: A pre-configured Metasploit resource script to quickly launch the corresponding listener.

Requirements

To use the generator, your Linux environment must have the following dependencies installed:

    Metasploit-Framework: Provides msfvenom for shellcode generation.

    Mingw-w64: Specifically x86_64-w64-mingw32-g++ for cross-compiling Windows binaries on Linux.

    Python 3: To run the XOR encryption script.

    OpenSSL: For creating the "ms-unified" SSL certificates for HTTPS communication.

Quick Start Guide
1. Preparation

Give the generator script execution permissions:
Bash

chmod +x 6gen66.sh

2. Launch the Generator

Run the script to start the interactive TUI:
Bash

./6gen66.sh

3. Follow the Prompts

    LHOST: The script will auto-detect your public IP. You can accept it or enter a custom address.

    LPORT: Set your listener port (default is 443 for HTTPS traffic).

    Output Name: Choose the filename for your compiled .exe.

4. Start the Listener

Once the build is complete, the script generates a handler.rc file. Start your listener with one command:
Bash

msfconsole -r handler.rc

Technical Mechanics

    Encryption: The encryptor.py script applies a 0xAA XOR key to the raw binary before it is compiled into the C++ wrapper.

    Persistence: The payload adds itself to HKCU\Software\Microsoft\Windows\CurrentVersion\Run under the name "WindowsSearchUpdate".

    Injection: It targets C:\Windows\System32\searchindexer.exe, creates it in a suspended state, writes the decrypted shellcode to its memory, and uses QueueUserAPC to trigger execution.

    Network Awareness: The payload remains dormant and retries every 60 seconds until it detects a successful connection to Google, ensuring it only attempts a callback when the internet is active.

Legal Disclaimer

    WARNING: 6gen66 is developed for authorized security auditing, research, and educational purposes only. Unauthorized access to computer systems is illegal. The developer of 6gen66 assumes no liability and is not responsible for any misuse or damage caused by this program. Use responsibly and only on systems you own or have explicit permission to test.
