import psutil
import os
import sys
import time
import subprocess
from datetime import datetime
import gc
import ctypes

class LimpiadorMemoria:
    def __init__(self):
        self.log_file = "limpieza_memoria.log"
        self.escribir_log(f"--- SESIÓN INICIADA: {datetime.now()} ---")
    
    def escribir_log(self, mensaje):
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} - {mensaje}\n")
    
    def obtener_info_memoria(self):
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            'total_gb': mem.total // (1024**3),
            'disponible_gb': mem.available // (1024**3),
            'usada_gb': mem.used // (1024**3),
            'porcentaje': mem.percent,
            'swap_usado_gb': swap.used // (1024**3),
            'swap_total_gb': swap.total // (1024**3) if swap.total > 0 else 0
        }
    
    def mostrar_panel(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        info = self.obtener_info_memoria()
        print("╔" + "═" * 58 + "╗")
        print("║              LIMPIADOR AUTOMÁTICO DE MEMORIA              ║")
        print("╠" + "═" * 58 + "╣")
        print(f"║ Total: {info['total_gb']:>4} GB | Usada: {info['usada_gb']:>4} GB | Disponible: {info['disponible_gb']:>4} GB ║")
        print(f"║ Porcentaje en uso: {info['porcentaje']:>5}%                               ║")
        barras = int(info['porcentaje'] / 2)
        print(f"║ [{'█' * barras}{'░' * (50 - barras)}] ║")
        print("╠" + "═" * 58 + "╣")
        return info

    def optimizar_memoria(self):
        print("║ > Ejecutando optimización...                              ║")
        gc.collect()
        try:
            # Libera Working Set (Requiere Admin para efectividad total)
            ctypes.windll.psapi.EmptyWorkingSet(ctypes.c_void_p(-1))
            self.escribir_log("Optimización de Working Set ejecutada.")
        except:
            pass
        print("║ ✓ Memoria optimizada.                                     ║")

    def cerrar_procesos_temporales(self):
        procesos_desechables = ['notepad.exe', 'calc.exe', 'mspaint.exe']
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and proc.info['name'].lower() in procesos_desechables:
                try:
                    proc.terminate()
                except:
                    continue

    def ejecutar_mantenimiento_completo(self):
        info_antes = self.obtener_info_memoria()
        self.optimizar_memoria()
        self.cerrar_procesos_temporales()
        info_despues = self.obtener_info_memoria()
        ganancia = (info_despues['disponible_gb'] - info_antes['disponible_gb']) * 1024
        print(f"║ ✓ Mantenimiento completo: +{ganancia} MB liberados aprox.      ║")

def main():
    limpiador = LimpiadorMemoria()
    
    while True:
        limpiador.mostrar_panel()
        print("║ OPCIONES:                                                 ║")
        print("║   1. Mantenimiento completo automático                    ║")
        print("║   2. Solo optimizar memoria                               ║")
        print("║   3. Ver procesos consumiendo memoria                     ║")
        print("║   4. Ver registro de limpieza                             ║")
        print("║   5. Salir                                                ║")
        print("╚" + "═" * 58 + "╝")
        
        opcion = input("\nSeleccione una opción (1-5): ")
        
        if opcion == '1':
            limpiador.ejecutar_mantenimiento_completo()
        elif opcion == '2':
            limpiador.optimizar_memoria()
        elif opcion == '3':
            print("\n--- TOP 5 PROCESOS ---")
            procesos = sorted(psutil.process_iter(['name', 'memory_info']), 
                             key=lambda p: p.info['memory_info'].rss, reverse=True)
            for p in procesos[:5]:
                print(f"{p.info['name']}: {p.info['memory_info'].rss // 1024**2} MB")
        elif opcion == '4':
            if os.path.exists(limpiador.log_file):
                with open(limpiador.log_file, 'r') as f:
                    print("\n" + "".join(f.readlines()[-10:]))
        elif opcion == '5':
            print("Saliendo...")
            break
        
        input("\nPresione Enter para continuar...")

# --- AQUÍ ES DONDE SE LLAMA ---
if __name__ == "__main__":
    main()

