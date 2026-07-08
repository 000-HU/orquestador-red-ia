import os
import json

# Definición semántica de categorías
CATEGORIAS = {
    "PRODUCCION_Y_MOTORES": [
        "app.js", "master_orch.js", "orquestador_core.py", "orquestador_defensa.py", 
        "orquestador_red.py", "motor_matematico.py", "motor_matematico.cpp", "src", "config"
    ],
    "AUDITORIA_Y_TELEMETRIA_SOSPECHOSA": [
        "telemetria_credenciales.json", "telemetria_ofensiva.json", "telemetria_sandbox.json", 
        "volcado_memoria_blob.txt", "volcado_detallado.txt", "ia_ofensiva_escalada.py", 
        "panel_escalada.html", "discover_ocultos.py", "descubrir_ocultos.py", "kill_sshd.js", "kill_sshd_core.cpp"
    ],
    "BASURA_Y_CACHE": [
        "node_modules", "package-lock.json", "alpine.tar.gz", "linea_tiempo_abril.txt", 
        ".txt", "abd.txt", "prueba", "__pycache__"
    ]
}

def obtener_tamaño(ruta):
    if os.path.isfile(ruta):
        return os.path.getsize(ruta)
    total = 0
    if os.path.isdir(ruta):
        for dirpath, _, filenames in os.walk(ruta):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
    return total

def auditar():
    reporte = {
        "1_PRODUCCION_UTIL (Conservar)": [],
        "2_TELEMETRIA_Y_SOSPECHOSOS (Revisar/Mudar a D)": [],
        "3_BASURA_Y_CACHE (Eliminar/Purgar)": [],
        "4_NO_CLASIFICADO": []
    }
    
    elementos = os.listdir('.')
    for item in elementos:
        if item in ['.git', '.github', 'auditor_semantico.py']:
            continue
            
        peso_bytes = obtener_tamaño(item)
        peso_mb = round(peso_bytes / (1024 * 1024), 2)
        info = {"nombre": item, "tamaño_mb": peso_mb}
        
        if item in CATEGORIAS["PRODUCCION_Y_MOTORES"]:
            reporte["1_PRODUCCION_UTIL (Conservar)"].append(info)
        elif item in CATEGORIAS["AUDITORIA_Y_TELEMETRIA_SOSPECHOSA"]:
            reporte["2_TELEMETRIA_Y_SOSPECHOSOS (Revisar/Mudar a D)"].append(info)
        elif item in CATEGORIAS["BASURA_Y_CACHE"]:
            reporte["3_BASURA_Y_CACHE (Eliminar/Purgar)"].append(info)
        else:
            reporte["4_NO_CLASIFICADO"].append(info)

    # Ordenar cada categoría por peso de mayor a menor
    for cat in reporte:
        reporte[cat] = sorted(reporte[cat], key=lambda x: x['tamaño_mb'], reverse=True)
        
    print(json.dumps(reporte, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    auditar()
