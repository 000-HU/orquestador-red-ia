#include <windows.h>
#include <iostream>
#include <vector>
#include <thread>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

// Estructura para la telemetría y control de los puertos en paralelo
struct SocketEspejo {
    SOCKET socketFd;
    int puerto;
    bool activo;
};

// 1. MONITOREO PROFUNDO DE CARPETAS (Capa de Sistema de Archivos)
void MonitorearCarpetaCritica(const wchar_t* ruta) {
    HANDLE hDir = CreateFileW(
        ruta,
        FILE_LIST_DIRECTORY,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        NULL,
        OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS,
        NULL
    );

    if (hDir == INVALID_HANDLE_VALUE) {
        std::wcerr << L"[-] Error al enganchar la carpeta: " << ruta << std::endl;
        return;
    }

    std::wcout << L"[+] Capa de monitoreo activa en memoria para: " << ruta << std::endl;

    std::vector<BYTE> buffer(4096);
    DWORD bytesDevueltos;

    while (true) {
        if (ReadDirectoryChangesW(
                hDir, buffer.data(), buffer.size(), TRUE,
                FILE_NOTIFY_CHANGE_FILE_NAME | FILE_NOTIFY_CHANGE_DIR_NAME | FILE_NOTIFY_CHANGE_LAST_WRITE,
                &bytesDevueltos, NULL, NULL)) {
            
            // Puntero para recorrer la estructura de eventos en el buffer de la RAM
            FILE_NOTIFY_INFORMATION* pInfo = reinterpret_cast<FILE_NOTIFY_INFORMATION*>(buffer.data());
            do {
                std::wstring nombreArchivo(pInfo->FileName, pInfo->FileNameLength / sizeof(WCHAR));
                std::wcout << L"[🚨 ALERTA DE SISTEMA]: Modificación detectada en archivo: " << nombreArchivo;
                
                if (pInfo->Action == FILE_ACTION_ADDED) std::wcout << L" (Archivo Creado)" << std::endl;
                else if (pInfo->Action == FILE_ACTION_MODIFIED) std::wcout << L" (Archivo Modificado)" << std::endl;
                else std::wcout << L" (Acción: " << pInfo->Action << L")" << std::endl;

                // Avanzar el puntero a la siguiente estructura en la matriz si existe
                if (pInfo->NextEntryOffset == 0) break;
                pInfo = reinterpret_cast<FILE_NOTIFY_INFORMATION*>(reinterpret_cast<BYTE*>(pInfo) + pInfo->NextEntryOffset);
            } while (pInfo);
        }
    }
    CloseHandle(hDir);
}

// 2. MONITOREO DE PUERTOS EN PARALELO (Capa de Red)
void EscuchaPuertoReactivo(int puerto) {
    SOCKET listenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (listenSocket == INVALID_SOCKET) return;

    sockaddr_in serverService;
    serverService.sin_family = AF_INET;
    serverService.sin_addr.s_addr = htonl(INADDR_ANY); // Escucha global en la interfaz
    serverService.sin_port = htons(puerto);

    if (bind(listenSocket, (SOCKADDR*)&serverService, sizeof(serverService)) == SOCKET_ERROR) {
        closesocket(listenSocket);
        return; // Puerto ocupado por un servicio legítimo o intruso
    }

    if (listen(listenSocket, SOMAXCONN) == SOCKET_ERROR) {
        closesocket(listenSocket);
        return;
    }

    while (true) {
        sockaddr_in clientAddr;
        int clientAddrSize = sizeof(clientAddr);
        // El hilo se bloquea aquí hasta que alguien intenta ingresar en paralelo
        SOCKET clientSocket = accept(listenSocket, (SOCKADDR*)&clientAddr, &clientAddrSize);
        
        if (clientSocket != INVALID_SOCKET) {
            char ipCliente[INET_ADDRSTRLEN];
            getnameinfo((SOCKADDR*)&clientAddr, sizeof(clientAddr), ipCliente, sizeof(ipCliente), NULL, 0, NI_NUMERICHOST);
            
            std::cout << "[🚨 ALERTA DE RED]: Intento de conexión simultánea detectado en Puerto [:" 
                      << puerto << "] desde IP: " << ipCliente << " -> Desconectando de inmediato." << std::endl;
            
            // Reacción inmediata: Mitigación cerrando el socket en la RAM
            closesocket(clientSocket);
        }
    }
    closesocket(listenSocket);
}

int main() {
    // Inicializar la infraestructura de red de Windows (Winsock)
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "[-] Error al inicializar Winsock." << std::endl;
        return 1;
    }

    // Vector de hilos para gestionar la ejecución paralela
    std::vector<std::thread> mallaHilos;

    // A. Lanzar monitoreo de la carpeta del proyecto/sistema
    mallaHilos.push_back(std::thread(MonitorearCarpetaCritica, L"C:\\Lab_Privado\\IA_y_Analisis\\orquestador-red-ia"));

    // B. Lanzar la malla de puertos trampa/espejo en paralelo para mitigar escaneos
    std::vector<int> puertosA_Monitorear = {3001, 3002, 3003, 3004, 4450}; // Puertos de prueba
    for (int puerto : puertosA_Monitorear) {
        mallaHilos.push_back(std::thread(EscuchaPuertoReactivo, puerto));
    }

    std::cout << "[+] Infraestructura de reacción síncrona desplegada en memoria." << std::endl;

    // Unir hilos para mantener el proceso principal en escucha persistente
    for (auto& th : mallaHilos) {
        if (th.joinable()) th.join();
    }

    WSACleanup();
    return 0;
}
