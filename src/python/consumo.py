import psutil
import time
import os

def mostrar_consumo():
    while True:
        procesos = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                io = proc.io_counters()
                total_bytes = io.read_bytes + io.write_bytes
                procesos.append((proc.info['name'], total_bytes))
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue
        
        os.system('cls')
        
        procesos.sort(key=lambda x: x[1], reverse=True)
        
        print(f"{'PROCESO':<25} | {'CONSUMO TOTAL (MB)':<15}")
        print("-" * 45)
        for nombre, b in procesos[:15]:
            megas = b / (1024 * 1024)
            print(f"{nombre:<25} | {megas:>12.2f} MB")
        
        print("\n[ Presiona Ctrl+C para detener ]")
        time.sleep(2)

if __name__ == "__main__":
    mostrar_consumo()
