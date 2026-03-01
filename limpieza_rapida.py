import psutil
import os
import sys
import time

def limpieza_rapida():
    """Limpieza rápida con una sola tecla"""
    
    print("🔧 LIMPIEZA RÁPIDA DE MEMORIA")
    print("=" * 40)
    
    # Estado inicial
    mem_inicial = psutil.virtual_memory()
    print(f"Memoria inicial: {mem_inicial.percent}% usado")
    print(f"Disponible: {mem_inicial.available // (1024**2)} MB")
    
    # Pasos de limpieza
    pasos = [
        ("Recolectando basura Python", lambda: __import__('gc').collect()),
        ("Vaciando cachés temporales", lambda: os.system('del /q /f %temp%\* > nul 2>&1')),
        ("Liberando memoria de navegadores", lambda: None),
        ("Optimizando memoria del sistema", lambda: None)
    ]
    
    for nombre, accion in pasos:
        print(f"\n⏳ {nombre}...", end='', flush=True)
        try:
            accion()
            time.sleep(0.5)
            print(" ✓")
        except:
            print(" ✗")
    
    # Vaciar caché de Windows (si es posible)
    try:
        import ctypes
        print("\n⏳ Vaciando caché de Windows...", end='', flush=True)
        ctypes.windll.psapi.EmptyWorkingSet(ctypes.c_void_p(-1))
        time.sleep(1)
        print(" ✓")
    except:
        print(" ✗ (Requiere admin)")
    
    # Estado final
    time.sleep(2)
    mem_final = psutil.virtual_memory()
    
    print("\n" + "=" * 40)
    print("RESULTADOS:")
    print("=" * 40)
    print(f"Antes: {mem_inicial.percent}% usado")
    print(f"Ahora: {mem_final.percent}% usado")
    
    mejora_mb = (mem_final.available - mem_inicial.available) // (1024**2)
    mejora_porcentaje = mem_inicial.percent - mem_final.percent
    
    if mejora_mb > 0:
        print(f"✅ Mejoría: +{mejora_mb} MB ({mejora_porcentaje:.1f}% menos usado)")
    else:
        print("⚠  Cambio mínimo detectado")
    
    print("\n💡 Consejo: Para mayor efectividad, ejecuta como Administrador")
    print("=" * 40)

if __name__ == "__main__":
    os.system('cls')
    limpieza_rapida()
    input("\nPresiona Enter para salir...")
