import sys
from scapy.all import IPv6, ICMPv6ND_NS, ICMPv6NDOptSrcLLAddr, srp, get_if_hwaddr

def escanear_ipv6(interfaz):
    print(f"[*] Iniciando escaneo profundo en interfaz: {interfaz}")
    
    try:
        mi_mac = get_if_hwaddr(interfaz)
    except:
        mi_mac = "00:00:00:00:00:00"

    paquete = (
        IPv6(dst="ff02::1") / 
        ICMPv6ND_NS(tgt="fe80::5a76:acff:fe7e:6a90") / 
        ICMPv6NDOptSrcLLAddr(lladdr=mi_mac)
    )
    
    respuestas, _ = srp(paquete, iface=interfaz, timeout=5, verbose=False)
    
    print("\n[+] Dispositivos detectados en la red Wi-Fi:")
    print("-" * 60)
    print(f"{'Dirección IPv6':<45} | {'Dirección MAC':<17}")
    print("-" * 60)
    
    dispositivos_vistos = set()
    for enviado, recibido in respuestas:
        ip_origen = recibido[IPv6].src
        mac_origen = recibido.src
        if mac_origen not in dispositivos_vistos:
            print(f"{ip_origen:<45} | {mac_origen:<17}")
            dispositivos_vistos.add(mac_origen)
            
    if not dispositivos_vistos:
        print("[!] No se recibieron respuestas directas. Asegúrate de ejecutar la terminal como Administrador.")

if __name__ == "__main__":
    escanear_ipv6("Wi-Fi")
