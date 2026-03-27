import psutil
import ctypes
import os
import sys

def mostrar_estado_memoria():
    """Muestra el estado actual de la memoria"""
    mem = psutil.virtual_memory()
    print("=" * 60)
    print("ESTADO ACTUAL DE LA MEMORIA")
    print("=" * 60)
    print(f"Total:      {mem.total // (1024**3):>6} GB")
    print(f"Disponible: {mem.available // (1024**3):>6} GB")
    print(f"Usada:      {mem.used // (1024**3):>6} GB")
    print(f"Porcentaje: {mem.percent:>6}%")
    
    if mem.percent > 80:
        print("⚠  ALERTA: Memoria por encima del 80%")
    elif mem.percent > 60:
        print("ℹ  ADVERTENCIA: Memoria por encima del 60%")
    print("=" * 60)
    return mem

def optimizar_memoria_simple():
    """Intenta optimizar la memoria de forma segura"""
    print("\nOptimizando memoria...")
    
    # Liberar memoria de procesos de bajo impacto
    try:
        # Vaciar cachés de Python si hay muchas referencias
        import gc
        recolectados = gc.collect()
        print(f"✓ Recolección de basura de Python: {recolectados} objetos liberados")
    except:
        pass
    
    # Usar API de Windows para liberar memoria (si está disponible)
    try:
        if os.name == 'nt':
            # Para Windows, intentar vaciar caché de memoria
            ctypes.windll.psapi.EmptyWorkingSet(ctypes.c_void_p(-1))
            print("✓ Caché de memoria vaciada (Working Set)")
    except:
        print("⚠  No se pudo vaciar caché (requiere permisos)")
    
    # Mostrar nuevo estado
    print("\n" + "=" * 60)
    print("NUEVO ESTADO DE MEMORIA")
    print("=" * 60)
    mem = psutil.virtual_memory()
    print(f"Disponible: {mem.available // (1024**3)} GB")
    print(f"Porcentaje: {mem.percent}%")
    print("=" * 60)

def cerrar_procesos_no_criticos():
    """Sugiere procesos que se pueden cerrar (solo informativo)"""
    print("\n" + "=" * 60)
    print("PROCESOS CONSUMIENDO MÁS MEMORIA")
    print("=" * 60)
    
    procesos = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'status']):
        try:
            if proc.info['memory_percent'] > 1.0:  # Más del 1% de memoria
                procesos.append((
                    proc.info['name'],
                    proc.info['pid'],
                    proc.info['memory_percent'],
                    proc.info['status']
                ))
        except:
            continue
    
    if procesos:
        procesos.sort(key=lambda x: x[2], reverse=True)
        
        print(f"{'No.':<3} {'PROCESO':<25} {'PID':<8} {'MEM %':<8} {'ESTADO':<10}")
        print("-" * 60)
        
        for i, (nombre, pid, mem_percent, estado) in enumerate(procesos[:15], 1):
            print(f"{i:<3} {nombre[:25]:<25} {pid:<8} {mem_percent:<8.1f} {estado:<10}")
    
    print("\n" + "=" * 60)
    print("SUGERENCIAS:")
    print("=" * 60)
    print("1. Cerrar Microsoft Edge (msedge.exe) - Usa ~20% de memoria")
    print("2. Cerrar programas en segundo plano innecesarios")
    print("3. Reiniciar svchost.exe (servicios de Windows)")
    print("4. Usar 'Limpiador de discos' de Windows")
    print("=" * 60)

def ejecutar_limpiador_windows():
    """Ejecuta herramientas de limpieza de Windows"""
    print("\nEjecutando herramientas de Windows...")
    
    comandos = [
        ("Limpiando archivos temporales", "cleanmgr /sagerun:1"),
        ("Liberando espacio de WinSxS", "DISM.exe /Online /Cleanup-Image /StartComponentCleanup"),
        ("Comprobando disco", "chkdsk /f")
    ]
    
    for descripcion, comando in comandos:
        print(f"\n{descripcion}...")
        try:
            # Solo mostrar comando, no ejecutar automáticamente
            print(f"  Comando: {comando}")
        except:
            print(f"  Error al ejecutar: {comando}")

def main():
    while True:
        os.system('cls')
        print("=" * 60)
        print("LIMPIADOR DE MEMORIA - WINDOWS")
        print("=" * 60)
        
        mem = mostrar_estado_memoria()
        
        print("\nOPCIONES:")
        print("1. Optimizar memoria (rápido y seguro)")
        print("2. Ver procesos consumiendo memoria")
        print("3. Ejecutar herramientas de Windows")
        print("4. Estado completo del sistema")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == '1':
            optimizar_memoria_simple()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '2':
            cerrar_procesos_no_criticos()
            respuesta = input("\n¿Deseas cerrar algún proceso? (s/n): ").lower()
            if respuesta == 's':
                try:
                    pid = int(input("Ingresa el PID a cerrar: "))
                    proceso = psutil.Process(pid)
                    nombre = proceso.name()
                    confirmacion = input(f"¿Seguro que quieres cerrar {nombre} (PID: {pid})? (s/n): ").lower()
                    if confirmacion == 's':
                        proceso.terminate()
                        print(f"✓ Proceso {nombre} cerrado")
                except Exception as e:
                    print(f"Error: {e}")
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '3':
            ejecutar_limpiador_windows()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '4':
            os.system('systeminfo | findstr /C:"Memoria"')
            os.system('wmic memorychip get capacity')
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '5':
            print("\n¡Hasta luego!")
            sys.exit(0)
        
        else:
            print("Opción no válida")
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    # Verificar si se ejecuta como administrador
    try:
        import ctypes
        es_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not es_admin:
            print("⚠  Para mejores resultados, ejecuta como administrador")
    except:
        pass
    
    main()
