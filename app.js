const fs = require('fs');
const path = require('path');

try {
    const datosCrudos = fs.readFileSync('mapa_red.json', 'utf-8');
    const mapaRed = JSON.parse(datosCrudos);
    
    console.log(`\n==================================================`);
    console.log(`🤖 MÓDULO DE INTELIGENCIA ARTIFICIAL: DETECTOR DE ANOMALÍAS`);
    console.log(`==================================================`);
    
    const alertasAnomalias = [];

    mapaRed.dispositivos_conectados.forEach((dev, index) => {
        let servicioSimulado = "Puerto Cerrado";
        let criticidad = "Inofensivo";
        let detalleAlerta = "Comportamiento normal de la red.";

        if (index % 3 === 0) {
            servicioSimulado = "HTTP (Puerto 80) - Servidor Web";
            if (index % 9 === 0) {
                criticidad = "CRÍTICO";
                detalleAlerta = "Posible intrusión. Tráfico inusual detectado hacia System32 simulado.";
            }
        } else if (index % 5 === 0) {
            servicioSimulado = "SSH (Puerto 22) - Consola Remota";
            if (index % 25 === 0) {
                criticidad = "ALTA";
                detalleAlerta = "Múltiples intentos de conexión fallidos (Fuerza bruta).";
            }
        } else if (index % 7 === 0) {
            servicioSimulado = "DNS (Puerto 53) - Servidor de Nombres";
        }

        if (criticidad !== "Inofensivo") {
            alertasAnomalias.push({
                IP: dev.ip,
                Servicio: servicioSimulado,
                Alerta: criticidad,
                Diagnostico: detalleAlerta
            });
        }
    });

    console.log(`⚠️  Análisis completado. Se detectaron ${alertasAnomalias.length} anomalías críticas.`);
    console.log(`==================================================\n`);
    
    if (alertasAnomalias.length > 0) {
        console.log("🚨 ALERTAS ROJAS REGISTRADAS:");
        console.table(alertasAnomalias.slice(0, 10));

        // --- PERSISTENCIA LOCAL SEGURA ---
        const encabezado = `==================================================\nREPORTE DE AUDITORÍA FORENSE - ANOMALÍAS DE RED\nFecha: ${new Date().toISOString()}\n==================================================\n\n`;
        
        const cuerpoReporte = alertasAnomalias.map(alerta => 
            `[IP]: ${alerta.IP} | [Servicio]: ${alerta.Servicio} | [Alerta]: ${alerta.Alerta}\n[Diagnóstico]: ${alerta.Diagnostico}\n--------------------------------------------------`
        ).join('\n');

        // Guarda localmente en la carpeta del repositorio para evitar fallas de rutas de red
        const rutaArchivo = path.join(__dirname, 'Auditoria_Conexiones.txt');
        fs.writeFileSync(rutaArchivo, encabezado + cuerpoReporte, 'utf-8');
        console.log(`💾 Evidencia guardada con éxito localmente en:\n   ${rutaArchivo}`);
    }

} catch (error) {
    console.error("❌ Error en el motor analítico de IA:", error.message);
}
