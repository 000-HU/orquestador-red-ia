from scapy.all import sniff, IP, TCP, UDP
import collections

stats = collections.Counter()

def packet_analyzer(pkt):
    if IP in pkt:
        # Extraer Protocolo y Puertos
        protocolo = pkt.proto
        puerto_origen = pkt.sport if (TCP in pkt or UDP in pkt) else "N/A"
        puerto_destino = pkt.dport if (TCP in pkt or UDP in pkt) else "N/A"
        
        # Identificar tipo de tráfico
        tipo = "TCP" if TCP in pkt else "UDP" if UDP in pkt else "OTRO"
        registro = f"{tipo} Port:{puerto_destino}"
        stats[registro] += 1
        
        print(f"[DPI] Paquete capturado: {tipo} | Origen: {puerto_origen} -> Destino: {puerto_destino}", end="\r")

print("\n[AI-DEEP] Iniciando captura de red (Deep Packet Inspection)...")
# Captura 50 paquetes para el análisis rápido
sniff(prn=packet_analyzer, count=50, store=0)

print("\n\n--- RESUMEN DE ACTIVIDAD DE RED ---")
for proto, count in stats.most_common(5):
    print(f"Puerto/Protocolo: {proto} | Conexiones: {count}")
