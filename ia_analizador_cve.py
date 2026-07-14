import json, os, time
def analizar():
 print("🤖 [IA-ORQUESTADOR] Iniciando motor de analisis de vulnerabilidades...")
 try:
  with open("telemetria_sandbox.json", "r") as f: d = json.load(f)
 except FileNotFoundError:
  print("❌ Error: No se encontro telemetria_sandbox.json. Ejecuta el extractor primero."); return
 r = {"timestamp_analisis": time.time(), "hosts_afectados": {}}
 for ip, ports in d.get("metricas_red", {}).items():
  for p, info in ports.items():
   firma = info.get("firma_cruda", "")
   if "OpenSSH_for_Windows_8.1" in firma:
    if ip not in r["hosts_afectados"]: r["hosts_afectados"][ip] = []
    r["hosts_afectados"][ip].append({
     "puerto": p, "servicio": "SSH", "version": "OpenSSH Windows 8.1", "nivel_riesgo": "ALTO",
     "cve_asociados": ["CVE-2023-38408", "CVE-2021-28041", "CVE-2020-14163"],
     "descripcion": "La version 8.1 de OpenSSH para Windows posee fallos criticos de ejecucion remota de codigo (RCE) y de denegacion de servicio (DoS) si no cuenta con parches de mitigacion de Microsoft.",
     "remediacion": "Actualizar Win32-OpenSSH a la ultima version estable a traves de PowerShell (winget install Microsoft.OpenJDK o via GitHub oficial de PowerShell)." 
    })
   if p == "80" and info.get("estado") == "ABIERTO":
    if ip not in r["hosts_afectados"]: r["hosts_afectados"][ip] = []
    r["hosts_afectados"][ip].append({
     "puerto": p, "servicio": "HTTP", "version": "Desconocida (Hidden)", "nivel_riesgo": "BAJO",
     "cve_asociados": [],
     "descripcion": "El servidor web del router oculta su firma de software. Aunque reduce la informacion para un atacante, la interfaz de administracion sigue expuesta en texto plano.",
     "remediacion": "Deshabilitar la administracion web por el puerto 80 HTTP y forzar unicamente el uso de HTTPS por el puerto 443."
    })
 with open("reporte_vulnerabilidades.json", "w") as f: json.dump(r, f, indent=4)
 print("\n🚠 [IA-ORQUESTADOR] Reporte de riesgos generado con exito en 'reporte_vulnerabilidades.json'.")
if __name__ == "__main__": analizar()
