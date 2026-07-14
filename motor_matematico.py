import json
import os
import math

def analizar_anomalias():
    print("[Python] Iniciando procesamiento matricial de la pila de red...")
    
    # Datos de telemetría simulados (Paquetes por segundo en canales de entrada)
    datos_trafico = [45, 52, 48, 120, 50, 47, 53, 200, 46]
    
    # 1. Calcular Media Matemática pura
    total = sum(datos_trafico)
    media = total / len(datos_trafico)
    
    # 2. Calcular Desviación Estándar sin librerías externas
    varianza = sum((x - media) ** 2 for x in datos_trafico) / len(datos_trafico)
    desviacion_estandar = math.sqrt(varianza)
    
    print(f"[Python] Media de tráfico calculada: {media:.2f} pps")
    print(f"[Python] Desviación estándar: {desviacion_estandar:.2f}")
    
    # 3. Umbral de Anomalía Asimétrica (Z-Score > 2)
    threshold = 2.0
    for i, pps in enumerate(datos_trafico):
        z_score = (pps - media) / (1 if desviacion_estandar == 0 else desviacion_estandar)
        
        if abs(z_score) > threshold:
            print(f"[!] CRÍTICO en Índice {i}: {pps} pps detectados. Z-Score: {z_score:.2f}")

if __name__ == "__main__":
    analizar_anomalias()
