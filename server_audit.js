const http = require('http');

const PUERTO = 3001; 

const servidor = http.createServer((req, res) => {
    res.writeHead(200, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Connection': 'keep-alive',
        'Server': 'Absolute-Zero-OS-Simulator'
    });

    if (req.url.includes('/v25.0/me')) {
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
    console.log(`[INFO] Dominios graph.facebook.com enrutados localmente.`);
    console.log(`==================================================`);
});
