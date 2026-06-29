import socket
import sys

# Configuración del socket defensivo
PUERTO = 8081
BLACKLIST = ['192.168.1.100', '10.0.0.5']  # Agrega aquí IPs sospechosas conocidas

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind(('0.0.0.0', PUERTO))
    s.listen(5)
    print(f"👑 [DEFENSA: ACTIVA] Monitoreando tráfico en puerto {PUERTO}...")
except Exception as e:
    print(f"❌ Error al levantar el socket: {e}")
    sys.exit(1)

# Bucle infinito seguro de escucha
try:
    while True:
        cliente_socket, direccion = s.accept()
        ip_origen = direccion[0]
        
        print(f"[🔍 TRÁFICO] Conexión entrante desde: {ip_origen}")
        
        # Lógica de mitigación mediante Blacklist
        if ip_origen in BLACKLIST:
            print(f"[⚠️ ACCIÓN CRÍTICA] IP en lista negra interceptada: {ip_origen}")
            try:
                cliente_socket.send(b'ROOT_CONTROL: Acceso Denegado por Politica de Seguridad\n')
            except Exception:
                pass
            finally:
                cliente_socket.close()
        else:
            # Flujo normal para conexiones permitidas
            try:
                cliente_socket.send(b'ROOT_CONTROL: Conexion Recibida\n')
            except Exception:
                pass
            finally:
                cliente_socket.close()

except KeyboardInterrupt:
    print("\n🛑 Apagando el orquestador de defensa de forma segura...")
finally:
    s.close()
    sys.exit(0)
