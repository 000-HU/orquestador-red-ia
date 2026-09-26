import socket, json, platform, time
def run():
 t = {"nodo_origen": {"os": platform.system(), "os_release": platform.release(), "arquitectura": platform.machine(), "timestamp_utc": time.time()}, "metricas_red": {}}
 with open("servicios_descubiertos.json", "r") as f: o = json.load(f)
 for ip, puertos in o.items():
  t["metricas_red"][ip] = {}
  for p in puertos:
   ini = time.perf_counter(); est = "CERRADO/FILTRADO"; bn = "N/A"
   try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.settimeout(1.0)
     if s.connect_ex((ip, p)) == 0:
      est = "ABIERTO"
      if p == 22: bn = s.recv(1024).decode("utf-8", errors="ignore").strip()
      elif p in [80, 443]:
       s.sendall(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
       bn = s.recv(200).decode("utf-8", errors="ignore").replace("\r\n", " | ")[:100]
   except Exception as e: est = f"ERROR: {str(e)}"
   lat = (time.perf_counter() - ini) * 1000
   t["metricas_red"][ip][p] = {"estado": est, "latencia_medida_ms": round(lat, 2), "firma_cruda": bn}
   print(f"   ↳ [NODO] {ip}:{p} -> {est} ({round(lat, 1)}ms)")
 with open("telemetria_sandbox.json", "w") as f: json.dump(t, f, indent=4)
 print("\n🏁 [SANDBOX] Telemetria guardada con exito.")
if __name__ == "__main__": run()
