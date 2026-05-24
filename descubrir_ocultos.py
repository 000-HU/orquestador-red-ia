import sys
from scapy.all import sniff, ARP, IP, UDP

# Diccionario para almacenar los dispositivos detectados {MAC: IP}
dispositivos = {}

def analizar_trafico(pkt):
    mac_origen = None
    ip_origen = None

    # Detectar dispositivos mediante paquetes ARP en la red
    if pkt.haslayer(ARP):
        mac_origen = pkt.hwsrc
        ip_origen = pkt.psrc
    
    # Detectar dispositivos mediante paquetes IPv4 generales (pings, consultas DNS, etc.)
    elif pkt.haslayer(IP):
        mac_origen = pkt.src
        ip_origen = pkt.payload.src if hasattr(pkt.payload, 'src') else pkt[IP].src

    # Filtrar direcciones vacías, de difusión o tu propia máquina
    if mac_origen and ip_origen and ip_origen != "0.0.0.0" and not mac_origen.startswith("33:33"):
        if mac_origen not in dispositivos:
            dispositivos[mac_origen] = ip_origen
            print(f"[+] DISPOSITIVO DETECTADO -> IP: {ip_origen:<15} | MAC: {mac_origen}")

print("[*] Orquestador escuchando el tráfico de red... Capturando dispositivos ocultos.")
print("[*] Mantén el ping corriendo en la otra ventana. Presiona Ctrl+C para finalizar.\n")

try:
    # Captura paquetes de forma promiscua filtrando el segmento local de Telmex
    sniff(iface="Wi-Fi", filter="arp or ip", prn=analizar_trafico, store=0)
except Exception as e:
    print(f"[!] Error: {e}")
    print("[!] Recuerda ejecutar la terminal como Administrador para habilitar Npcap.")
