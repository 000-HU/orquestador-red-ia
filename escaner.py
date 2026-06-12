import os
import platform
import subprocess
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

SUBNET_PREFIX = "172.26."
OUTPUT_FILE = "mapa_red.json"
MAX_THREADS = 50

def ping_host(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", "-w", "1000", ip]
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            return {"ip": ip, "status": "activo", "ultima_conexion": datetime.now().isoformat()}
    except Exception:
        pass
    return None

def obtener_dispositivos_arp():
    dispositivos = {}
    try:
        command = "arp -a"
        output = subprocess.check_output(command, shell=True, text=True, encoding="cp850")
        for linea in output.splitlines():
            partes = linea.split()
            if len(partes) >= 3:
                ip_candidata = partes[0]
                if SUBNET_PREFIX in ip_candidata:
                    mac = partes[1].replace("-", ":").lower()
                    dispositivos[ip_candidata] = mac
    except Exception as e:
        print(f"[-] Error al leer la tabla ARP: {e}")
    return dispositivos

def escanear_red():
    print(f"[*] Iniciando escaneo activo en el segmento {SUBNET_PREFIX}0.0/16...")
    ips_a_probar = []
    
    # Rango de subredes detectadas en tu tabla ARP
    subredes = [50, 51, 55]
    
    for subred in subredes:
        for host in range(1, 255):
            ips_a_probar.append(f"{SUBNET_PREFIX}{subred}.{host}")
            
    nodos_activos = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        resultados = executor.map(ping_host, ips_a_probar)
        for res in resultados:
            if res:
                nodos_activos.append(res)
                print(f"[+] Dispositivo encontrado: {res['ip']}")

    print("[*] Cruzando datos con la tabla ARP del sistema...")
    tabla_mac = obtener_dispositivos_arp()
    
    mapa_red = {
        "fecha_escaneo": datetime.now().isoformat(),
        "dispositivos_conectados": []
    }
    
    for nodo in nodos_activos:
        ip = nodo["ip"]
        nodo["mac"] = tabla_mac.get(ip, "Desconocida")
        mapa_red["dispositivos_conectados"].append(nodo)
        
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(mapa_red, f, indent=4, ensure_ascii=False)
        print(f"[+] Escaneo completado. Archivo '{OUTPUT_FILE}' actualizado.")
    except Exception as e:
        print(f"[-] Error al guardar el archivo JSON: {e}")

if __name__ == "__main__":
    escanear_red()
