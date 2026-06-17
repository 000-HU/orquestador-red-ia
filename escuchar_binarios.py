import socket
import sys

HOST = "172.26.51.205" 

def escanear_binarios():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        s.bind((HOST, 0))
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        
        print(f"[*] Escuchando binarios de red en {HOST}... Presiona Ctrl+C para detener.")
        print("="*60)

        while True:
            datos_binarios, addr = s.recvfrom(65565)
            payload = datos_binarios[20:]
            if payload:
                texto_plano = "".join([chr(b) if 32 <= b < 127 else "." for b in payload])
                if texto_plano.strip(" ."):
                    print(f"[Origen: {addr[0]}] -> Texto Plano:")
                    print(f"{texto_plano}")
                    print("-" * 40)
    except KeyboardInterrupt:
        print("\n[-] Deteniendo la escucha de binarios.")
        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    except Exception as e:
        print(f"[-] Error: {e}")
        print("[!] Asegúrate de ejecutar Git Bash como Administrador.")

if __name__ == "__main__":
    escanear_binarios()
