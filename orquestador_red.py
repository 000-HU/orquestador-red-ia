import sys
import time
from scapy.all import sniff, ARP, IP
dispositivos_vistos = set()
def generar_log_plano(ip, mac, estado='ACTIVO'):
    timestamp = int(time.time())
    log_linea = f'{timestamp}|{ip}|{mac}|{estado}\n'
    with open('red_monitoreo.log', 'a') as f:
        f.write(log_linea)
def analizar_trafico(pkt):
    mac_origen, ip_origen = None, None
    if pkt.haslayer(ARP):
        mac_origen, ip_origen = pkt.hwsrc, pkt.psrc
    elif pkt.haslayer(IP):
        mac_origen, ip_origen = pkt.src, pkt[IP].src
    if mac_origen and ip_origen and ip_origen != '0.0.0.0' and not mac_origen.startswith('33:33'):
        if mac_origen not in dispositivos_vistos:
            dispositivos_vistos.add(mac_origen)
            estado = 'CAMARA_EXPUESTA' if ip_origen == '192.168.1.81' else 'APPLE_DISP' if ip_origen in ['192.168.1.174','192.168.1.177'] else 'ACTIVO'
            print(f'[+] DETECTADO -> IP: {ip_origen:<15} | MAC: {mac_origen} | Logeado')
            generar_log_plano(ip_origen, mac_origen, estado)
if __name__ == '__main__':
    print('[*] Orquestador hibrido unificado corriendo...')
    print('[*] Escribiendo binarios de red directamente a logs en disco duro.\n')
    try:
        sniff(iface='Wi-Fi', filter='arp or ip', prn=analizar_trafico, store=0)
    except KeyboardInterrupt:
        print('\n[*] Monitoreo finalizado por el usuario.')
