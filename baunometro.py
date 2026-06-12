import time

def mostrar_instrucciones_pulso():
    print("\n" + "="*60)
    print(" PASO 1: INSTRUCCIONES PARA LA TOMA DE PULSACIONES (FRECUENCIA CARDÍACA)")
    print("="*60)
    print("1. Coloque los dedos índice y medio en la parte interna de la muñeca (pulso radial).")
    print("   O en el cuello al lado de la tráquea (pulso carotídeo).")
    print("2. No use el pulgar, ya que tiene su propio pulso y puede confundir la cuenta.")
    print("3. Presione suavemente hasta que sienta las pulsaciones.")
    print("4. Prepárese para contar las pulsaciones durante un intervalo de 15 segundos.")
    input("\nPresione [ENTER] cuando esté listo para iniciar el cronómetro de 15 segundos...")
    
    print("\n⏱️ ¡Comience a contar AHORA!")
    for i in range(15, 0, -1):
        print(f"Tiempo restante: {i} segundos...", end="\r")
        time.sleep(1)
    
    print("\n\n⏱️ ¡TIEMPO! Detenga la cuenta.")
    
    while True:
        try:
            pulsos = int(input("\n¿Cuántas pulsaciones contó en los 15 segundos?: "))
            frecuencia = pulsos * 4
            print(f"-> Su frecuencia cardíaca estimada es de: {frecuencia} lpm (latidos por minuto).")
            return frecuencia
        except ValueError:
            print("Por favor, introduzca un número válido.")

def mostrar_instrucciones_presion():
    print("\n" + "="*60)
    print(" PASO 2: INSTRUCCIONES PARA EL USO DEL BAUMANÓMETRO MANUAL")
    print("="*60)
    print("1. Coloque el brazalete en el brazo izquierdo, 2 cm por encima del pliegue del codo.")
    print("2. Coloque la campana del estetoscopio sobre la arteria braquial (fosa del codo).")
    print("3. Cierre la válvula de la perilla girándola hacia la derecha.")
    print("4. Infle rápidamente el brazalete apretando la perilla hasta llegar a 160-180 mmHg.")
    print("5. Abra la válvula lentamente (2-3 mmHg por segundo) mientras escucha atentamente:")
    print("   - El PRIMER sonido rítmico que escuche será la Presión Sistólica.")
    print("   - El MOMENTO EN QUE DESAPARECEN los sonidos será la Presión Diastólica.")
    input("\nPresione [ENTER] una vez que haya realizado la medición para registrar los datos...")

def capturar_datos_presion():
    print("\n" + "="*60)
    print(" PASO 3: REGISTRO DE DATOS")
    print("="*60)
    while True:
        try:
            sistolica = int(input("Ingrese la Presión Sistólica (el primer sonido, ej. 120): "))
            diastolica = int(input("Ingrese la Presión Diastólica (cuando cesó el sonido, ej. 80): "))
            if sistolica > diastolica:
                return sistolica, diastolica
            else:
                print("Error: La presión sistólica debe ser mayor que la diastólica. Intente de nuevo.")
        except ValueError:
            print("Por favor, introduzca valores numéricos enteros válidos.")

def evaluar_hipertension(sistolica, diastolica, pulso):
    print("\n" + "="*60)
    print(" EVALUACIÓN Y DIAGNÓSTICO (Contexto: Hipertensión Arterial)")
    print("="*60)
    print(f"Resultados registrados: {sistolica}/{diastolica} mmHg | Pulso: {pulso} lpm\n")
    
    # Clasificación basada en las guías estándar de hipertensión
    if sistolica >= 140 or diastolica >= 90:
        print("🚨 ALERTA: Los valores corresponden a HIPERTENSIÓN ARTERIAL.")
        if sistolica >= 180 or diastolica >= 120:
            print("❌ CRISIS HIPERTENSIVA: Busque atención médica de emergencia inmediatamente.")
        else:
            print("📋 Nota: Se requiere monitoreo constante y consultar a su médico para un diagnóstico formal.")
    elif 130 <= sistolica <= 139 or 80 <= diastolica <= 89:
        print("⚠️ ADVERTENCIA: Presión arterial ALTA (Prehipertensión o Hipertensión Etapa 1).")
        print("💡 Se recomiendan cambios en el estilo de vida (reducir sodio, hacer ejercicio).")
    elif 120 <= sistolica <= 129 and diastolica < 80:
        print("📈 Presión arterial ELEVADA. Monitoree sus niveles regularmente.")
    elif sistolica < 90 or diastolica < 60:
        print("📉 Presión arterial BAJA (Hipotensión).")
    else:
        print("✅ Presión arterial NORMAL. ¡Siga así!")

    # Evaluación breve del pulso
    if pulso > 100:
        print("⚠️ Nota adicional: Su frecuencia cardíaca está elevada (Taquicardia en reposo).")
    elif pulso < 60:
        print("⚠️ Nota adicional: Su frecuencia cardíaca está baja (Bradicardia en reposo).")

# Ejecución principal del programa
if __name__ == "__main__":
    print("=== SOFTWARE DE SIMULACIÓN Y CONTROL DE BAUMANÓMETRO MANUAL ===")
    pulso_detectado = mostrar_instrucciones_pulso()
    mostrar_instrucciones_presion()
    sistolica, diastolica = capturar_datos_presion()
    evaluar_hipertension(sistolica, diastolica, pulso_detectado)
    print("\n" + "="*60)
    print("Fin de la simulación. Recuerde que este software es puramente educativo.")
    print("="*60)
