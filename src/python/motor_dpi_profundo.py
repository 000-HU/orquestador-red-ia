import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP
import collections
import socket

# 1. Configuración de Análisis
stats = collections.Counter()
print("="*60)
print("  MOTOR DE ANÁLISIS DE RED PROFUNDA v3.0 (DPI STYLE)")
print("="*60)

# 2. Función de Inspección de Paquetes
def analizar_paquete(pkt):
    if IP in pkt:
        # Extraer Info de Capa 3 y 4
        src = pkt[IP].src
        dst = pkt[IP].dst
        proto = "TCP" if TCP in pkt else "UDP" if UDP in pkt else "OTRO"
        
        if TCP in pkt or UDP in pkt:
            dport = pkt.dport
            # Intentar identificar servicio por puerto
            try:
                servicio = socket.getservbyport(dport)
            except:
                servicio = "Desconocido"
            
            registro = f"{proto} | Puerto: {dport} ({servicio})"
            stats[registro] += 1
            print(f"[CAPTURA] {src} -> {dst} | {registro}", end="\r")

# 3. Ejecución de la Captura
print(f"\n[INFO] Iniciando Sniffer en tiempo real (Estilo Wireshark)...")
try:
    # Captura 100 paquetes para el análisis profundo
    scapy.sniff(prn=analizar_paquete, count=100, store=0)
except Exception as e:
    print(f"\n[ERROR] ¿Tienes Npcap instalado? Error: {e}")

# 4. Reporte de Inteligencia de Red
print("\n\n" + "="*20 + " REPORTE DE PROTOCOLOS " + "="*20)
for conexion, total in stats.most_common(10):
    print(f"-> {conexion:<30} | Paquetes detectados: {total}")
print("="*63)
