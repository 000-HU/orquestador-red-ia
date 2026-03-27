import os, socket, subprocess, time

def check(p):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return "OPERATIVO" if s.connect_ex(('127.0.0.1', p)) == 0 else "CAÍDO"

while True:
    os.system('cls') # Limpia la pantalla estilo terminal pura
    print("="*45)
    print(" BARE-METAL MULTI-ORCHESTRATOR v2.5")
    print("="*45)
    print(f"[NODE-ORCH] P:3000 -> {check(3000)}")
    print(f"[IA-PYTHON] P:5000 -> {check(5000)}")
    print(f"[DB-REDE]   P:8080 -> {check(8080)}")
    print("-" * 45)
    print("1. Levantar Master Orch (Node.js)")
    print("2. Levantar Monitor DPI (Python)")
    print("3. Ver Bitácora Técnica")
    print("4. Salir")
    
    op = input("\nSeleccione [1-4]: ")
    
    if op == "1":
        print("[Lanzando Node.js...]")
        subprocess.Popen(["node", "master_orch.js"], shell=True)
        time.sleep(2) # Espera a que el puerto abra
    elif op == "2":
        print("[Lanzando Python DPI...]")
        subprocess.Popen(["python", "monitor_completo.py"], shell=True)
        time.sleep(2)
    elif op == "3":
        os.system("notepad BITACORA_TECNICA.md")
    elif op == "4":
        break

