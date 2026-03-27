import psutil
import time
import os
from datetime import datetime

def mostrar_consumo_completo():
    try:
        while True:
            # Datos del sistema
            cpu_percent = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()
            disk_io = psutil.disk_io_counters()
            
            # Procesos
            procesos = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    io = proc.io_counters()
                    total_bytes = io.read_bytes + io.write_bytes
                    if total_bytes > 0:
                        procesos.append((
                            proc.info['name'],
                            proc.info['pid'],
                            total_bytes,
                            proc.info['memory_percent']
                        ))
                except:
                    continue
            
            os.system('cls')
            
            # Encabezado del sistema
            print("=" * 70)
            print(f"SISTEMA - {datetime.now().strftime('%H:%M:%S')}")
            print("=" * 70)
            print(f"CPU: {cpu_percent:>5.1f}% | Memoria: {memory.percent:>5.1f}% ({memory.used//(1024**3)}/{memory.total//(1024**3)} GB)")
            print(f"Disco Lectura: {disk_io.read_bytes//(1024**2):>6} MB | Escritura: {disk_io.write_bytes//(1024**2):>6} MB")
            print("-" * 70)
            
            # Tabla de procesos
            if procesos:
                procesos.sort(key=lambda x: x[2], reverse=True)
                
                print(f"{'No.':<3} {'PROCESO':<22} {'PID':<8} {'DISCO (MB)':>12} {'MEM %':>8}")
                print("-" * 70)
                
                for i, (nombre, pid, b, mem) in enumerate(procesos[:15], 1):
                    megas = b / (1024 * 1024)
                    print(f"{i:<3} {nombre[:22]:<22} {pid:<8} {megas:>11.2f} {mem:>7.1f}")
            
            print("-" * 70)
            print("[ Ctrl+C para detener | Actualiza cada 3 segundos ]")
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n¡Monitor detenido! Presiona Enter para salir...")
        input()

if __name__ == "__main__":
    mostrar_consumo_completo()
