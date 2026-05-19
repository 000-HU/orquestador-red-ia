const http = require('http'); 
const fs = require('fs'); 

http.createServer((req, res) => { 
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost'); 
    
    fs.readFile('datos_vector.bin', (err, data) => { 
        if (err) { 
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('Error: No hay vectores'); 
            return; 
        } 
        console.log('>>> Escaneando Red Escolar: ' + data.length + ' nodos detectados'); 
        res.writeHead(200, { 'Content-Type': 'application/octet-stream' });
        res.end(data); 
    }); 
}).listen(3001, '127.0.0.1', () => console.log('>>> MASTER ORCH SEGURO - ACTIVO EN LOCALHOST:3001'));
