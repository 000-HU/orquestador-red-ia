const { execSync } = require('child_process');
const fs = require('fs');

const CONFIG_FILE = 'network_state.json';

function ejecutar(cmd) {
    try { return execSync(cmd).toString(); } 
    catch (e) { return null; }
}

console.log("\n[!] INICIANDO ORQUESTADOR DE RED INTELIGENTE");

// 1. Compilación y Ejecución
ejecutar('javac RedRecursiva.java');
const rawOutput = ejecutar('java RedRecursiva');

if (!rawOutput) {
    console.error("[X] Error crítico en el motor Java.");
    process.exit(1);
}

// 2. Extracción de Datos (Regex para latencia)
const rutas = rawOutput.split('\n').filter(l => l.includes('Latencia Total'));
const mejor = rutas.sort((a, b) => parseInt(a.match(/\d+/g).pop()) - parseInt(b.match(/\d+/g).pop()))[0];
const latenciaActual = parseInt(mejor.match(/\d+/g).pop());

// 3. Comparación con Historial (Memoria del Orquestador)
let historial = { mejor_latencia: Infinity, alertas: 0 };
if (fs.existsSync(CONFIG_FILE)) {
    historial = JSON.parse(fs.readFileSync(CONFIG_FILE));
}

console.log(`\n>>> ESTADO ACTUAL: ${latenciaActual}ms`);

if (latenciaActual < historial.mejor_latencia) {
    console.log("✅ NUEVO RÉCORD: ¡Ruta optimizada detectada!");
    historial.mejor_latencia = latenciaActual;
} else if (latenciaActual > 50) {
    console.log("⚠️ ALERTA: Latencia crítica detectada en la topología.");
    historial.alertas++;
}

// 4. Persistencia (Base de Datos ligera)
fs.writeFileSync(CONFIG_FILE, JSON.stringify(historial, null, 2));
console.log(`[SQL-Lite Style] Log guardado en ${CONFIG_FILE}`);
console.log(`RUTA ÓPTIMA: ${mejor.trim()}`);
