
#!/bin/bash
# ==============================================================================
# ABSOLUTE-ZERO-OS: Emulador de Diagnóstico Crudo para Intel Celeron N4020
# ==============================================================================

DIR_LAB="/c/Lab_Privado/IA_y_Analisis/orquestador-red-ia"
cd "$DIR_LAB"

echo "[🚨 ABSOLUTE-ZERO-OS]: Inicializando lectura ciega del metal en texto plano..."

# Función para inyectar comandos de bajo nivel evadiendo la paginación visual
ejecutar_wmi_crudo() {
    # Llamada directa al núcleo de powershell sin cargar su frontend corporativo
    powershell.exe -NoProfile -NonInteractive -Command "$1" 2>/dev/null | tr -d '\r'
}

echo "=== 1. ESPECIFICACIONES DE LA MOTHERBOARD ==="
ejecutar_wmi_crudo "Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer, Product, Version | Format-List"

echo "=== 2. IDENTIFICACIÓN DEL FIRMWARE (BIOS) ==="
ejecutar_wmi_crudo "Get-CimInstance Win32_Bios | Select-Object Name, Version, SerialNumber | Format-List"

echo "=== 3. ANÁLISIS DE ENTROPÍA DE RED (CONEXIONES ACTIVAS) ==="
# Extrae los sockets reales vinculándolos al ID del proceso (PID) en la RAM
ejecutar_wmi_crudo "Get-NetTCPConnection | Where-State {\$_.State -eq 'Established'} | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess | Format-Table"

echo "=== 4. AUDITORÍA DE PRIVILEGIOS DE USUARIO ==="
ejecutar_wmi_crudo "Get-LocalGroupMember -Group 'Administrators' | Select-Object Name, PrincipalSource | Format-List"
