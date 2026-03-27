import os
import subprocess

# Versión simplificada y ultra-ligera para tu Celeron N4020
profiles_path = os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')

if not os.path.exists(profiles_path):
    print("Error: Instala y abre Firefox al menos una vez antes de correr este script.")
else:
    perfiles = [d for d in os.listdir(profiles_path) if os.path.isdir(os.path.join(profiles_path, d))]
    if perfiles:
        perfil = os.path.join(profiles_path, perfiles[0])
        userjs = os.path.join(perfil, 'user.js')
        
        # Configuraciones de 'poda' extrema para la RAM
        config = [
            'user_pref("browser.cache.memory.capacity", 51200);', # Limitar cache RAM a 50MB
            'user_pref("dom.ipc.processCount", 1);',            # Solo 1 proceso (Ahorro masivo)
            'user_pref("browser.sessionhistory.max_total_viewers", 0);', # No guardar páginas previas en RAM
            'user_pref("browser.tabs.animate", false);',        # Sin animaciones
            'user_pref("toolkit.telemetry.enabled", false);'    # Cero telemetría
        ]
        
        with open(userjs, 'w') as f:
            f.write('\n'.join(config))
        print(f"EXITO: Configuracion minimalista aplicada en {perfiles[0]}")
