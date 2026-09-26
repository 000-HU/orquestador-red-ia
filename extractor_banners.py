import socket
import json

# Cargar los servicios descubiertos previamente
try:
    with open("servicios_descubiertos.json", "r") as f:
        mapa_red = json.load(f)
except FileNotFoundError:
    # Respaldo con sintaxis corregida de forma manual y explícita
    mapa_red = {
        "192.168.68.1":,
        "192.168.68.67": [22, 139, 445]
    }

def obtener_banner(ip, puerto):
    banner = "No se pudo extraer (Timeout/Filtro)"
    try:
        # Protocolo TCP estándar de usuario (Bypass de privilegios)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5)
            s.connect((ip, puerto))
            
            # --- SSH (Puerto 22) ---
            if puerto == 22:
                respuesta = s.recv(1024)
                banner = respuesta.decode('utf-8', errors='ignore').strip()
                
            # --- HTTP / HTTPS (Puertos 80, 443) ---
            elif puerto in:
                peticion = b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\nUser-Agent: OrquestadorIA/1.0\r\n\r\n"
                s.sendall(peticion)
                respuesta = s.recv(2048)
                lineas = respuesta.decode('utf-8', errors='ignore').split('\r\n')
                servidor = [l for l in lineas if l.lower().startswith("server:")]
                banner = servidor[0] if servidor else (lineas[0] if lineas else "HTTP Activo")
                
            # --- DNS (Puerto 53 TCP) ---
            elif puerto == 53:
                peticion_dns = b'\x00\x1e\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03'
                s.sendall(peticion_dns)
                respuesta = s.recv(1024)
                banner = f"DNS Activo - Respondió bytes: {len(respuesta)}"
                
            # --- SMB / NETBIOS (Puertos 139, 445) ---
            else:
                s.sendall(b"\x00")
                respuesta = s.recv(512)
                banner = respuesta.decode('utf-8', errors='ignore').strip() or "Puerto abierto (Protocolo mudo)"
                
    except Exception as e:
        banner = f"Error de conexión: {str(e)}"
        
    return banner

reporte_banners = {}

print("🕵️‍♂️ Iniciando extracción de firmas y banners de bajo nivel...")
for ip, puertos in mapa_red.items():
    reporte_banners[ip] = {}
    print(f"\n🖥️ Analizando Host: {ip}")
    for puerto in puertos:
        print(f"   ↳ Extrayendo puerto {puerto}...")
        banner_detectado = obtener_banner(ip, puerto)
        reporte_banners[ip][puerto] = banner_detectado
        print(f"     [Resultado]: {banner_detectado}")

# Guardar reporte estructurado para la IA
with open("banners_extraidos.json", "w") as f:
    json.dump(reporte_banners, f, indent=4)

print("\n🏁 Extracción finalizada. Reporte guardado en 'banners_extraidos.json'.")
