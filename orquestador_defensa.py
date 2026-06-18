import socket, json, os, time
def forzar_bypass_bloqueo(target_ip):
 print(f"⚡ [IA-BYPASS] Detectado ataque en caliente. Aislando: {target_ip}")
 archivos = ["servicios_descubiertos.json", "telemetria_sandbox.json"]
 for arch in archivos:
  try:
   if os.path.exists(arch):
    with open(arch, "r") as f: data = json.load(f)
    if "metricas_red" in data and target_ip in data["metricas_red"]: del data["metricas_red"][target_ip]
    elif target_ip in data: del data[target_ip]
    with open(arch, "w") as f: json.dump(data, f, indent=4)
    print(f"   ↳ [OK] Purga defensiva completada en {arch}")
  except Exception as e: print(f"   ⚠️ Fallo en {arch}: {str(e)}")
def honeypot():
 print("🍯 [IA-ORQUESTADOR] Modo Defensa Unificado activo en puerto 8080...")
 try:
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); s.bind(("0.0.0.0", 8080)); s.listen(5)
   while True:
    conn, addr = s.accept()
    with conn:
     print(f"\a[🚨 ALERTA] Intruso detectado interactuando desde la IP: {addr[0]}")
     forzar_bypass_bloqueo(addr[0])
     conn.sendall(b"HTTP/1.1 200 OK\r\nServer: Apache/2.4.41\r\n\r\n<html><body><h1>Access Denied</h1></body></html>\r\n")
 except KeyboardInterrupt: print("\n🛑 Orquestador de defensa apagado.")
if __name__ == "__main__": honeypot()
