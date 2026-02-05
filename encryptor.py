import sys
import os

def generate_payload_h(input_bin):
    if not os.path.exists(input_bin):
        print(f"[-] Error: {input_bin} not found.")
        return

    with open(input_bin, 'rb') as f:
        plaintext = f.read()

    xor_key = 0xAA 
    ciphertext = bytearray([b ^ xor_key for b in plaintext])

    with open("payload.h", "w") as h:
        h.write(f"unsigned char encryptedShellcode[] = {{ {', '.join([hex(b) for b in ciphertext])} }};\n")
        h.write(f"unsigned int shellcodeLen = {len(ciphertext)};\n")
        h.write(f"unsigned char xorKey = {hex(xor_key)};\n")

    print(f"[*] Generated payload.h ({len(ciphertext)} bytes)")

if __name__ == "__main__":
    generate_payload_h(sys.argv[1])
