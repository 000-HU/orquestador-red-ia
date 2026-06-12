const { exec } = require('child_process');
const path = require('path');
const http = require('http');
const fs = require('fs');

const PUERTO = 3001; 
let reporteIA = { timestamp: "N/A", anomalias: [] };

const servidor = http.createServer((req, res) => {
    // 🛡️ Habilitar CORS Global Bare-Metal para saltar bloqueos en LibreWolf
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    // Servir el script de inyección con el tipo MIME correcto (evita error nosniff)
    if (req.url === '/master_orch.js') {
        fs.readFile(path.join(__dirname, 'master_orch.js'), (err, js) => {
            if (err) {
                res.writeHead(404, { 'Content-Type': 'text/plain' });
                res.end('Archivo master_orch.js no encontrado en el disco.');
            } else {
                res.writeHead(200, { 'Content-Type': 'application/javascript; charset=UTF-8' });
                res.end(js);
            }
        });
    } 
    else if (req.url === '/' || req.url === '/index.html') {
        fs.readFile(path.join(__dirname, 'index.html'), (err, html) => {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(html);
        });
    } 
    else if (req.url === '/api/anomalias') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(reporteIA.anomalias));
    } 
    else if (req.url === '/api/reportar' && req.method === 'POST') {
        let cuerpo = '';
        req.on('data', chunk => { cuerpo += chunk; });
        req.on('end', () => {
            try {
                reporteIA = JSON.parse(cuerpo);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: "Procesado" }));
                console.log(`📡 [Axios] Telemetría de TensorFlow recibida en el puerto ${PUERTO}.`);
            } catch (e) {
                res.writeHead(400); res.end("Error JSON");
            }
        });
    } else {
        res.writeHead(404); res.end();
    }
});

servidor.listen(PUERTO, () => {
    console.log(`==================================================`);
    console.log(`🤖 CORE UNIFICADO ACTIVADO — PUERTO ${PUERTO}`);
    console.log(`🏠 Control local en: http://localhost:${PUERTO}`);
    console.log(`==================================================\n`);
    
    console.log("🧠 Ejecutando pipelines analíticos de bajo nivel...");
    const rutaApp = path.join(__dirname, 'app.js');
    exec(`node "${rutaApp}"`, (err, stdout) => {
        if (!err) console.log(stdout);
    });
});
