import os, json, time
def auditar_servicios_nativos():
 print("🔥 [IA-OFENSIVA] Extrayendo telemetria via PowerShell y CIM nativo..."); r = {"timestamp": time.time(), "servicios_modificables": []}
 cmd = "powershell -NoProfile -Command \"Get-CimInstance -ClassName Win32_Service | Where-Object { \$_.StartMode -eq 'Auto' -and \$_.PathName -notlike '*System32*' } | Select-Object Name, DisplayName, PathName, StartMode | ConvertTo-Json -Compress\"\"
 try:
  with os.popen(cmd) as f: salida = f.read().strip()
  if salida:
   try:
    datos = json.loads(salida)
    if isinstance(datos, dict): datos = [datos]
    for s in datos:
     path = s.get("PathName", "")
     if path and not path.startswith('"') and " " in path:
      r["servicios_modificables"].append({"name": s.get("Name"), "display": s.get("DisplayName"), "path": path, "vector": "Unquoted Service Path Real"})
   except Exception:
    r["raw_output"] = salida
 except Exception as e: r["error"] = str(e)
 with open("telemetria_servicios.json", "w") as f: json.dump(r, f, indent=4)
 print("\n🏁 [IA-OFENSIVA] Auditoria nativa completada en 'telemetria_servicios.json'.")
if __name__ == "__main__": auditar_servicios_nativos()
