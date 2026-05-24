import os
import sys
import platform
import time
def inicializar_entorno():
    sistema = platform.system()
    print(f'[*] Detectando Arquitectura Fisica... Sistema: {sistema}')
    print(f'[*] Asignando buferes de memoria RAM en texto plano para logs...')
    if sistema == 'Windows':
        interfaz_optima = 'Wi-Fi'
    elif sistema == 'Linux':
        interfaz_optima = 'wlan0'
    else:
        interfaz_optima = 'Loopback'
    return interfaz_optima
def generar_log_plano(ip, mac, estado='ACTIVO'):
    timestamp = int(time.time())
    log_linea = f'{timestamp}|{ip}|{mac}|{estado}\n'
    with open('red_monitoreo.log', 'a') as f:
        f.write(log_linea)
if __name__ == '__main__':
    iface = inicializar_entorno()
    print(f'[+] Orquestador Bare-Metal listo en interfaz: {iface}')
    print('[*] Escribiendo telemetria directamente en "red_monitoreo.log"...')
    generar_log_plano('192.168.1.81', '54:2b:57:0a:18:d7', 'CAMARA_EXPUESTA')
    print('[+] Log generado exitosamente.')
