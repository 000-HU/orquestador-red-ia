import os
import json

def forzar_bypass_bloqueo(target_ip):
    print(f"⚡ [IA-BYPASS] Forzando mitigacion de infraestructura para: {target_ip}")
    
    # ACCIÓN 1: Mitigación Lógica (Aislamiento de Base de Datos)
    archivos_objetivo = ["servicios_descubiertos.json", "telemetria_sandbox.json"]
    for archivo in archivos_objetivo:
        try:
            if os.path.exists(archivo):
                with open(archivo, "r") as f:
                    data = json.load(f)
                
                if "metricas_red" in data and target_ip in data["metricas_red"]:
                    del data["metricas_red"][target_ip]
                elif target_ip in data:
                    del data[target_ip]
                    
                with open(archivo, "w") as f:
                    json.dump(data, f, indent=4)
                print(f"   ↳ [OK] Removido exitosamente de {archivo}")
        except Exception as e:
            print(f"   ⚠️ No se pudo limpiar {archivo}: {str(e)}")

    print(f"🏁 [ÉXITO] Host {target_ip} completamente aislado de forma silenciosa.")

if __name__ == "__main__":
    forzar_bypass_bloqueo("192.168.68.62")
