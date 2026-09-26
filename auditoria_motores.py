import socket
import sys
import threading
from datetime import datetime

# Puertos críticos a evaluar basados en motores de búsqueda, renderizado y administración
PUERTOS_OBJETIVO = {
    80: "HTTP (Panel de administración expuesto)",
    443: "HTTPS (Panel web cifrado)",
    554: "RTSP (Streaming de video/Cámaras sin cifrar)",
    1900: "SSDP/UPnP (Motor de búsqueda/Renderizado multimedia)",
    5353: "mDNS (Descubrimiento local/Fuga de Hostname)",
    8008: "Google Cast / Chromecast API",
    9000: "DLNA Media Server (Renderizado alternativo)",
    62078: "Apple iOS Sync/AirPlay Service"
}

# Lista de IPs obtenidas de tu escaneo previo
DISPOSITIVOS_A_ESCANEAR = [
    "192.168.1.180", "192.168.1.162", "192.168.1.97", 
    "192.168.1.76", "192.168.1.98", "192.168.1.81", 
    "192.168.1.177", "192.168.1.174", "192.168.1.254"
]

print_lock = threading.Lock()

def escanear_puerto(ip, puerto, servicio):
    try:
        # Configuración de socket de baja latencia con timeout estricto para ahorrar RAM
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.5)
        resultado = sock.connect_ex((ip, puerto))
        
        if resultado == 0:
            with print_lock:
                print(f"[!] ALERTA -> IP: {ip:<15} | Puerto Abierto: {puerto:<5} | Motor: {servicio}")
        sock.close()
    except Exception:
        pass

def auditoria_host(ip):
     hilos = []
     for puerto, servicio in PUERTOS_OBJETIVO.items():
         t = threading.Thread(target=escanear_puerto, args=(ip, puerto, servicio))
         hilos.append(t)
         t.start()
     for t in hilos:
         t.join()

if __name__ == "__main__":
    print(f"[*] Iniciando auditoría de la pila de red: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("[*] Evaluando vulnerabilidades de exposición de servicios locales...\n")
    
    for host in DISPOSITIVOS_A_ESCANEAR:
        auditoria_host(host)
        
    print("\n[*] Auditoría finalizada de manera limpia.")
