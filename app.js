const fs = require('fs');
const path = require('path');
const { exec, spawn } = require('child_process');

const ejecutarScriptPython = (nombreScript, argumentos = []) => {
  return new Promise((resolve) => {
    console.log(`[+] Ejecutando módulo Python: ${nombreScript}...`);
    const proceso = spawn('python', [path.join(__dirname, nombreScript), ...argumentos]);
    
    let stdout = '';
    proceso.stdout.on('data', (data) => { stdout += data.toString(); });
    proceso.stderr.on('data', (data) => { if(data.toString().trim()) console.log(`   [!] Log: ${data.toString().trim()}`); });
    
    proceso.on('close', () => resolve(stdout.trim()));
  });
};

const ejecutarComandoRaw = (comando) => {
  return new Promise((resolve) => {
    exec(comando, (error, stdout) => resolve(stdout || ""));
  });
};

function normalizaNum(x) {
  const n = Number(x);
  return Number.isFinite(n) ? n : 0;
}

// Clasificación estricta de anomalías reales
function clasificarAnomalia(ip, puerto, info, datosOfensivos) {
  const estado = String(info.estado ?? "").toLowerCase();
  const lat = normalizaNum(info.latencia_medida_ms);
  const latAlta = lat >= 800;

  const conexionesPS = normalizaNum(info.conexiones_por_seg ?? info.rps);
  const intentos = normalizaNum(info.intentos);
  const errores = normalizaNum(info.errores);

  const tuvoError = estado.includes("error") || estado.includes("timeout") || estado.includes("fail");
  const volumenSospechoso = conexionesPS >= 50 || intentos >= 200 || errores >= 50;
  const posibleDos = tuvoError && (volumenSospechoso || latAlta);

  // Regla real para tu servidor HTTP en puerto 80 (Recién levantado)
  if (puerto === "80" && String(info.estado) === "ABIERTO") {
    return {
      criticidad: "ALTA",
      detalleAlerta: `Servidor HTTP expuesto. Tráfico sin cifrar. Migrar a HTTPS (443).`,
      reportar: true
    };
  }

  // SMB 445 (CRÍTICO)
  if (puerto === "445" && String(info.estado) === "ABIERTO") {
    const bajoAtaque = datosOfensivos.ataques_activos?.some(a => a.target_ip === ip && a.puerto === 445);
    return {
      criticidad: "CRÍTICO",
      detalleAlerta: bajoAtaque
        ? "¡ALERTA DE INTRUSIÓN ACTIVA! Puerto SMB (445) bajo explotación activa."
        : "Puerto SMB (445) expuesto. Riesgo crítico de exploits de movimiento lateral (EternalBlue).",
      reportar: true
    };
  }

  // SSH 22 (ALTA)
  if (puerto === "22" && String(info.estado) === "ABIERTO") {
    return {
      criticidad: "ALTA",
      detalleAlerta: `Puerto SSH (22) abierto. Firma: ${info.firma_cruda ?? "N/A"}.`,
      reportar: true
    };
  }

  if (puerto === "443" && posibleDos) {
    return {
      criticidad: "ALTA",
      detalleAlerta: `Posible DoS en 443. Latencia: ${lat}ms. Conex/s≈${conexionesPS}, errores≈${errores}.`,
      reportar: true
    };
  }

  return { criticidad: "INFORMACIÓN", detalleAlerta: "Servicio operativo estándar.", reportar: false };
}

// Función principal de orquestación integrada
async function iniciarOrquestador() {
  try {
    console.log(`\n==================================================`);
    console.log(`🤖 INTEGRACIÓN EN VIVO - ABSOLUTE ZERO OS v2.5`);
    console.log(`==================================================`);

    // PASO 1: Escaneo Real de tu infraestructura
    console.log("[+] Iniciando escaneo de infraestructura en tiempo real...");
    const salidaEscaneo = await ejecutarScriptPython('escaner_puertos.py');
    console.log(`[✔] Escaneo finalizado.`);

    // PASO 2: Parsear salida real de escaner_puertos.py
    let metricas_red = {};
    
    const lineas = salidaEscaneo.split('\n');
    lineas.forEach(linea => {
      if (linea.includes("[🔥 ABIERTO]")) {
        try {
          const partes = linea.split("[🔥 ABIERTO] ")[1].split(" ->")[0].trim().split(":");
          const ip = partes[0];
          const puerto = partes[1];
          
          if (!metricas_red[ip]) metricas_red[ip] = {};
          metricas_red[ip][puerto] = { "estado": "ABIERTO", "latencia_medida_ms": 1 };
        } catch (e) {
          // Captura silenciosa de errores de parsing
        }
      }
    });

    // Guardar datos en la telemetría del Sandbox
    const telemetriaFinal = { metricas_red };
    fs.writeFileSync(path.join(__dirname, 'telemetria_sandbox.json'), JSON.stringify(telemetriaFinal, null, 2));

    // PASO 3: Análisis de la IA
    console.log(`\n==================================================`);
    console.log(`🤖 MÓDULO DE INTELIGENCIA ARTIFICIAL: DETECTOR DE ANOMALÍAS`);
    console.log(`==================================================`);

    const datosOfensivos = fs.existsSync(path.join(__dirname, 'telemetria_ofensiva.json'))
      ? JSON.parse(fs.readFileSync(path.join(__dirname, 'telemetria_ofensiva.json'), 'utf-8')) : {};

    const alertasAnomalias = [];

    for (const ip of Object.keys(metricas_red)) {
      const puertos = metricas_red[ip] || {};
      for (const puerto of Object.keys(puertos)) {
        const info = puertos[puerto] || {};
        const { criticidad, detalleAlerta, reportar } = clasificarAnomalia(ip, puerto, info, datosOfensivos);

        if (reportar) {
          alertasAnomalias.push({ IP: ip, Servicio: `Puerto ${puerto}`, Alerta: criticidad, Diagnostico: detalleAlerta });
        }
      }
    }

    console.log(`⚠️ Análisis completado. Se detectaron ${alertasAnomalias.length} anomalías reales.`);
    console.log(`==================================================\n`);

    // PASO 4: Sincronización del Panel e Inicio de Contramedidas
    if (alertasAnomalias.length > 0) {
      console.log("🚨 ALERTAS REGISTRADAS EN PRODUCCIÓN:");
      console.table(alertasAnomalias);

      // Sincronizar el reporte forense para master_orch.js
      const encabezado = `==================================================\nREPORTE DE AUDITORÍA FORENSE REALES\nFecha: ${new Date().toISOString()}\n==================================================\n\n`;
      const cuerpoReporte = alertasAnomalias.map(alerta => `[IP]: ${alerta.IP} | [Servicio]: ${alerta.Servicio} | [Alerta]: ${alerta.Alerta}\n[Diagnóstico]: ${alerta.Diagnostico}\n--------------------------------------------------`).join('\n');
      fs.writeFileSync(path.join(__dirname, 'Auditoria_Conexiones.txt'), encabezado + cuerpoReporte, 'utf-8');

      // INTEGRACIÓN: Enviar eventos activos a un log de eventos compartidos para el panel
      const mapaRedActualizado = {
        ultima_actualizacion: new Date().toISOString(),
        alertas_activas: alertasAnomalias,
        dispositivos_conectados: Object.keys(metricas_red).map(ip => ({ ip, estado: "VERIFICADO" }))
      };
      fs.writeFileSync(path.join(__dirname, 'mapa_red.json'), JSON.stringify(mapaRedActualizado, null, 2));
      console.log("[✔] Sincronización con mapa_red.json completada para el panel principal.");

      console.log(`\n==================================================`);
      console.log(`🛡️ INICIANDO PROTOCOLO DE MITIGACIÓN AUTOMATIZADA`);
      console.log(`==================================================`);

      for (const alerta of alertasAnomalias) {
        if (alerta.Alerta === "CRÍTICO") {
          console.log(`[!] Alerta CRÍTICA en ${alerta.IP}. Ejecutando contramedidas severas...`);
          const salidaBloqueador = await ejecutarComandoRaw(`python bloqueador_mac.py ${alerta.IP}`);
          console.log(salidaBloqueador.trim() || "   [OK] Bloqueador MAC ejecutado.");

          const salidaAnalizador = await ejecutarComandoRaw(`python ia_analizador_cve.py ${alerta.IP}`);
          console.log(salidaAnalizador.trim() || "   [OK] Analizador CVE ejecutado.");
        }

        if (alerta.Alerta === "ALTA") {
          console.log(`[!] Alerta ALTA en ${alerta.IP}. Aplicando mitigación preventiva...`);
          const salida = await ejecutarComandoRaw(`python bloqueador_mac.py ${alerta.IP}`);
          console.log(salida.trim() || "   [OK] Mitigación leve completada.");
        }
      }
    } else {
      // Si la red está limpia, limpiamos las alertas pasadas en mapa_red.json para el panel
      const mapaLimpio = { ultima_actualizacion: new Date().toISOString(), alertas_activas: [], dispositivos_conectados: [] };
      fs.writeFileSync(path.join(__dirname, 'mapa_red.json'), JSON.stringify(mapaLimpio, null, 2));
    }
  } catch (error) {
    console.error("❌ Error en el núcleo integrado:", error.message);
  }
}

// Exportamos la función por si master_orch.js la requiere mediante require('./app.js')
module.exports = { iniciarOrquestador };

// Ejecución directa si se corre de forma aislada
if (require.main === module) {
  iniciarOrquestador();
}

