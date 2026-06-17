import socket
import json
from concurrent.futures import ThreadPoolExecutor

# Puertos críticos a verificar en el entorno real
PUERTOS_OBJETIVO = [22, 80, 443, 139, 445, 3000, 3001, 8080]
IPS = [f"172.26.55.{i}" for i in range(224, 255)]

def escanear_host_puerto(ip, puerto):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            resultado = s.connect_ex((ip, puerto))
            if resultado == 0:
                print(f"[🔥 ABIERTO] {ip}:{puerto} -> Servicio activo detectado.")
                return puerto
    except Exception:
        pass
    return None

def escanear_ip(ip):
    puertos_abiertos = []
    for puerto in PUERTOS_OBJETIVO:
        res = escanear_host_puerto(ip, puerto)
        if res:
            puertos_abiertos.append(res)
    return ip, puertos_abiertos

print("⚡ Iniciando escaneo de puertos de bajo nivel en bloque 172.26.55.224-254...")
resultados = {}

with ThreadPoolExecutor(max_workers=20) as executor:
    for ip, puertos in executor.map(escanear_ip, IPS):
        if puertos:
            resultados[ip] = puertos

# Guardar hallazgos en tu mapa estructural
with open('servicios_descubiertos.json', 'w') as f:
    json.dump(resultados, f, indent=4)

print("🏁 Escaneo finalizado. Resultados guardados en 'servicios_descubiertos.json'.")
