const { spawn } = require('child_process');

console.log("🚀 [Master Orch] Inicializando Core del Sistema Zero...");

// 1. Levantar el Backend (API en Puerto 3001)
console.log("📡 Arrancando servidor de auditoría (app.js)...");
const servidor = spawn('node', ['app.js'], { stdio: 'inherit' });

// 2. Ejecutar Escáner de Red (Python) en segundo plano de forma asíncrona
function iniciarMonitoreo() {
    console.log("🔍 Iniciando escaner.py de forma asíncrona...");
    const escaner = spawn('python', ['escaner.py']);

    escaner.stdout.on('data', (data) => {
        console.log(`[Python Escaner]: ${data.toString().trim()}`);
    });

    escaner.stderr.on('data', (data) => {
        console.error(`[🚨 Error Escaner]: ${data.toString().trim()}`);
    });
}

// 3. Ejecutar Detector de Ocultos / Anomalías
function iniciarDeteccionAnomalias() {
    console.log("🎯 Iniciando descubrir_ocultos.py...");
    const detector = spawn('python', ['descubrir_ocultos.py']);

    detector.stdout.on('data', (data) => {
        console.log(`[Python Analizador]: ${data.toString().trim()}`);
    });
}

// Retardo de 2 segundos para asegurar que el servidor 3001 esté listo antes de los scripts
setTimeout(() => {
    iniciarMonitoreo();
    iniciarDeteccionAnomalias();
}, 2000);

// Manejo de cierre limpio de procesos hijos al salir
process.on('SIGINT', () => {
    console.log("\n🛑 Apagando Orquestador y deteniendo subprocesos...");
    servidor.kill();
    process.exit();
});
