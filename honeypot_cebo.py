import socket, sys, time
def lanzar_cebo():
 print("🍯 [IA-HONEYPOT] Desplegando puertos cebo en el Sandbox... (Ctrl+C para salir)")
 cebo_port = 8080
 try:
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind(("0.0.0.0", cebo_port))
   s.listen(5)
   print(f"   ↳ Estacion de engano activa escuchando en el puerto: {cebo_port}")
   while True:
    conn, addr = s.accept()
    with conn:
     timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
     print(f"\a[🚨 INTRUSO DETECTADO] IP Remota {addr[0]} ataco el puerto cebo {cebo_port} a las {timestamp}!")
     conn.sendall(b"HTTP/1.1 200 OK\r\nServer: Apache/2.4.41 (Ubuntu)\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Login</h1></body></html>\r\n")
 except KeyboardInterrupt:
  print("\n🛑 Honeypot desactivado de forma segura.")
 except Exception as e:
  print(f"❌ Error en el Honeypot: {str(e)}")
if __name__ == "__main__": lanzar_cebo()
