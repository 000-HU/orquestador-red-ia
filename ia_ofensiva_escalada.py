import os, json, sys
def auditoria_ofensiva():
 r = {"entidades_seguridad": {}, "unidades_vulnerables": {}}
 print("🔥 [IA-OFENSIVA] Ejecutando bypass de entorno para escalada..."); sids = ""; privs = ""
 try:
  with os.popen("C:\\Windows\\System32\\whoami.exe /user /fo csv") as f: sids = f.read().strip()
  if sids:
   lineas = sids.split("\n")
   if len(lineas) > 1: p = lineas[1].split(","); r["entidades_seguridad"]["sid"] = p[1].replace('"','')
 except Exception as e: r["entidades_seguridad"]["err_sid"] = str(e)
 try:
  with os.popen("C:\\Windows\\System32\\whoami.exe /priv") as f: privs = f.read().strip()
  r["entidades_seguridad"]["tokens_privilegios"] = [l.split("  ")[0].strip() for l in privs.split("\n") if "Disabled" in l or "Enabled" in l]
 except Exception as e: r["entidades_seguridad"]["err_priv"] = str(e)
 print("📂 [IA-OFENSIVA] Buscando debilidades en permisos de unidades locales...")
 try:
  with os.popen("C:\\Windows\\System32\\wbem\\wmic.exe service get name,displayname,pathname,startmode") as f:
   r["unidades_vulnerables"]["servicios_sistema"] = [l.strip() for l in f if "Program Files" in l and not '"' in l]
 except Exception as e: r["unidades_vulnerables"]["err_servicios"] = str(e)
 with open("telemetria_ofensiva.json", "w") as f: json.dump(r, f, indent=4)
 print("\n🏁 [IA-OFENSIVA] Reporte consolidado en 'telemetria_ofensiva.json'.")
if __name__ == "__main__": auditoria_ofensiva()
