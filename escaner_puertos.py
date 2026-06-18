import socket
import json
from concurrent.futures import ThreadPoolExecutor

PUERTOS_OBJETIVO = [22, 80, 443, 139, 445, 3000, 3001, 8080]

# Lectura dinámica del mapa de red generado previamente
try:
    with open("mapa_red.json", "r") as m:
        data = json.load(m)
    IPS = [d["ip"] for d in data.get("dispositivos_conectados", [])]
except Exception:
    print("❌ Error al leer mapa_red.json, usando rango por defecto.")
    IPS = [f"172.26.50.{i}" for i in range(1, 255)]

def escanear_host_puerto(ip, puerto):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
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

print(f"⚡ Iniciando escaneo dinámico de bajo nivel sobre {len(IPS)} hosts detectados...")
resultados = {}

with ThreadPoolExecutor(max_workers=30) as executor:
    for ip, puertos in executor.map(escanear_ip, IPS):
        if puertos:
            resultados[ip] = puertos

with open('servicios_descubiertos.json', 'w') as f:
    json.dump(resultados, f, indent=4)

print("🏁 Escaneo finalizado. Resultados guardados en 'servicios_descubiertos.json'.")
