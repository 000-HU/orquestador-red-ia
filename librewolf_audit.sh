#!/bin/bash

# Configuración de los dos segmentos detectados
SEGMENTOS=("172.26.51" "172.26.55")
OUTPUT_FILE="mapa_red.json"

echo "📡 Iniciando escaneo secuencial en los segmentos..."

# Inicializa el archivo JSON estructurado
echo "{" > "$OUTPUT_FILE"
echo "    \"dispositivos\": [" >> "$OUTPUT_FILE"

PRIMER_ELEMENTO=true

for seg in "${SEGMENTOS[@]}"; do
    echo "🔎 Escaneando segmento $seg.x..."
    for i in {1..254}; do
        ip="$seg.$i"
        
        # Ping rápido: 1 solo paquete, espera máxima de 150ms
        if ping -n 1 -w 150 "$ip" > /dev/null 2>&1; then
            fecha=$(date +"%Y-%m-%dT%H:%M:%S")
            
            # Recupera la dirección MAC desde la caché ARP de Windows
            mac_line=$(arp -a "$ip" 2>/dev/null | grep -i "$ip")
            mac="Desconocida"
            
            # Expresión regular para aislar la MAC en formato Windows (XX-XX-XX...)
            if [[ "$mac_line" =~ ([0-9a-fA-F]{2}-){5}[0-9a-fA-F]{2} ]]; then
                mac="${BASH_REMATCH[0]}"
                mac="${mac//-/:}" # Cambia guiones por dos puntos para estandarizar
            fi
            
            # Manejo de comas estructurales para JSON válido
            if [ "$PRIMER_ELEMENTO" = true ]; then
                PRIMER_ELEMENTO=false
            else
                echo "," >> "$OUTPUT_FILE"
            fi
            
            # Escritura directa en bloque del objeto JSON
            cat <<EOF >> "$OUTPUT_FILE"
        {
            "ip": "$ip",
            "status": "activo",
            "ultima_conexion": "${fecha}",
            "mac": "${mac^^}"
        }
EOF
            echo "   [+] Host activo encontrado: $ip"
        fi
    done
done

# Cierre correcto del archivo estructurado
echo "" >> "$OUTPUT_FILE"
echo "    ]" >> "$OUTPUT_FILE"
echo "}" >> "$OUTPUT_FILE"

echo "✅ Escaneo finalizado con éxito. Datos guardados en $OUTPUT_FILE"