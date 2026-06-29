const http = require('http');
const { exec } = require('child_process');

const PUERTO = 3001;

const servidor = http.createServer((req, res) => {
    // Configuración global de cabeceras CORS para permitir la conexión desde el panel HTML
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Manejo de peticiones preflight OPTIONS del navegador
    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        return res.end();
    }

    // ─── ENDPOINT 1: PURGA AGRESIVA DE LA PILA MEDIANTE POWERSHELL CONTRA EL INTRUSO ───
    if (req.method === 'POST' && req.url === '/api/purgar-nativa') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        
        console.log(`[*] Ejecutando anulación agresiva de OpenSSH mediante hilos de PowerShell...`);
        
        // Comando directo que deshabilita el servicio SSH y lo detiene de inmediato por la fuerza
        const cmdPowerShell = `powershell -Command "Set-Service -Name sshd -StartupType Disabled; Stop-Service -Name sshd -Force"`;
        
        exec(cmdPowerShell, (error, stdout, stderr) => {
            if (error) {
                console.error(`[-] Falla en el kernel al ejecutar comando: ${error.message}`);
                return res.end(JSON.stringify({ status: `Falla: ${error.message}` }));
            }
            
            console.log(`[+] ¡SERVICIO OPENSSH DESTRUIDO CON ÉXITO!`);
            console.log(`[INFO] Sockets del puerto 22 liberados. Conexión del intruso de Linux muerta.`);
            return res.end(JSON.stringify({ status: "CONEXIÓN DEL INTRUSO ELIMINADA - PUERTO 22 CERRADO" }));
        });
        return;
    }

    // ─── ENDPOINT 2: INTERCEPTACIÓN CAPA 7 SIMULADA (FACEBOOK GRAPH) ───
    if (req.url.includes('/v25.0/me')) {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        const respuestaSimulada = {
            id: "101009283748291",
            name: "Jared Rico - Entorno de Auditoria Local",
            email: "jared.rico.audit@absolutezero.org",
            segment_status: "isolated_loopback",
            simulation_timestamp: new Date().toISOString()
        };

        console.log(`[TRAZADO] Petición interceptada exitosamente en Capa 7: ${req.url}`);
        return res.end(JSON.stringify(respuestaSimulada, null, 2));
    }

    // ─── ENDPOINT DEFAULT: ESTADO GENERAL DEL ENTORNO ───
    res.writeHead(200, { 'Content-Type': 'application/json' });
    const estadoEntorno = {
        status: "online",
        orquestador: "Absolute-Zero-OS",
        segmento: "Simulador de Red Local Activo",
        timestamp: new Date().toISOString()
    };

    res.end(JSON.stringify(estadoEntorno, null, 2));
});

servidor.listen(PUERTO, () => {
    console.log(`==================================================`);
    console.log(`[OK] Servidor de Aislamiento Activo en Puerto: ${PUERTO}`);
    console.log(`[INFO] Dominios ://facebook.com enrutados localmente.`);
    console.log(`==================================================`);
});

