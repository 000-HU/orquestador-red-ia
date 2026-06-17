import socket

# Escucha localmente en todas las interfaces en el puerto 3002 (no requiere admin)
HOST = "0.0.0.0"
PORT = 3002

def iniciar_escucha():
    # Socket UDP estándar, permitido para cualquier usuario
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    
    print(f"[*] Servidor Activo. Escuchando binarios en puerto: {PORT} (Modo Usuario)")
    print("=" * 60)
    
    try:
        while True:
            datos_binarios, addr = s.recvfrom(65535)
            # Conversión de binario crudo a texto plano legible
            texto_plano = "".join([chr(b) if 32 <= b < 127 else "." for b in datos_binarios])
            
            if texto_plano.strip(" ."):
                print(f"[Origen: {addr[0]}:{addr[1]}] -> Texto Plano:")
                print(f"{texto_plano}")
                print("-" * 40)
    except KeyboardInterrupt:
        print("\n[-] Escucha finalizada por el usuario.")
    finally:
        s.close()

if __name__ == "__main__":
    iniciar_escucha()
