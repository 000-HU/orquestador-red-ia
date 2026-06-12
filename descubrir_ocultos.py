import socket
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

SUBNET_PREFIX = "172.26."
PUERTOS_A_VERIFICAR = [22, 80, 443, 3000, 8080]
MAX_THREADS = 100

# Cargar los dispositivos que ya conocemos para no duplicar
try:
    with open("mapa_red.json", "r", encoding="utf-8") as f:
        datos_existentes = json.load(f)
        ips_conocidas = {d["ip"] for d in datos_existentes.get("dispositivos_conectados", [])}
except Exception:
    ips_conocidas = set()

def escanear_puertos_host(ip):
    """Verifica si el host tiene puertos abiertos aunque no responda a ping."""
    if ip in ips_conocidas:
        return None
        
    for puerto in PUERTOS_A_VERIFICAR:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                result = s.connect_ex((ip, puerto))
                if result == 0:
                    return {
                        "ip": ip,
                        "status": "oculto_activo",
                        "puerto_detectado": puerto,
                        "ultima_conexion": datetime.now().isoformat(),
                        "mac": "Filtrada por Firewall"
                    }
        except Exception:
            pass
    return None

def descubrir_ocultos():
    print("[*] Buscando hosts ocultos detrás de firewalls (Escaneo de Sockets)...")
    subredes = [50, 51, 55]
    ips_a_probar = []
    
    for subred in subredes:
        for host in range(1, 255):
            ips_a_probar.append(f"{SUBNET_PREFIX}{subred}.{host}")
            
    nodos_ocultos = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        resultados = executor.map(escanear_puertos_host, ips_a_probar)
        for res in resultados:
            if res:
                nodos_ocultos.append(res)
                print(f"[!] Nodo oculto detectado: {res['ip']} (Puerto {res['puerto_detectado']})")

    if nodos_ocultos:
        try:
            with open("mapa_red.json", "r+", encoding="utf-8") as f:
                data = json.load(f)
                data["dispositivos_conectados"].extend(nodos_ocultos)
                data["fecha_actualizacion_ocultos"] = datetime.now().isoformat()
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()
            print(f"[+] Completado. Se agregaron {len(nodos_ocultos)} nodos ocultos a 'mapa_red.json'.")
        except Exception as e:
            print(f"[-] Error al actualizar el mapa de red: {e}")
    else:
        print("[+] No se detectaron nuevos dispositivos ocultos en los puertos estándar.")

if __name__ == "__main__":
    discover_ocultos = descubrir_ocultos()
