import socket
import json
import sys
from concurrent.futures import ThreadPoolExecutor

PUERTOS_OBJETIVO = [22, 80, 443, 139, 445, 3000, 3001, 8080]

# 1. Intentar leer mapa dinámico o recibir IP por argumento desde Node.js
if len(sys.argv) > 1:
    IPS = [sys.argv[1]]  # Si app.js le pasa una IP específica, escanea solo esa
else:
    try:
        with open("mapa_red.json", "r") as m:
            data = json.load(m)
        IPS = [d["ip"] for d in data.get("dispositivos_conectados", [])]
    except Exception:
        # Si falla el mapa, usamos Localhost por seguridad para las pruebas
        IPS = ["127.0.0.1"]

def escanear_host_puerto(ip, puerto):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            resultado = s.connect_ex((ip, puerto))
            if resultado == 0:
                print(f"[🔥 ABIERTO] {ip}:{puerto} -> Servicio activo detectado.")
                return (ip, puerto)
    except Exception:
        pass
    return None

def iniciar_escaneo():
    # Ejecución paralela masiva usando hilos
    tareas = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        for ip in IPS:
            for puerto in PUERTOS_OBJETIVO:
                tareas.append(executor.submit(escanear_host_puerto, ip, puerto))
    
    # Recolectar resultados estructurados
    resultados_finales = []
    for t in tareas:
        res = t.result()
        if res:
            resultados_finales.append(f"Host: {res[0]} | Puerto: {res[1]}")
            
    # Imprimir un resumen limpio para que app.js/IA lo analice sin ruido
    print("\n--- RESUMEN DE ESCANEO ---")
    if resultados_finales:
        print("\n".join(resultados_finales))
    else:
        print("No se detectaron puertos abiertos en los hosts escaneados.")

if __name__ == "__main__":
    iniciar_escaneo()
