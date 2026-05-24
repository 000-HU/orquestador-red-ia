const fs = require('fs');

function obtenerDispositivos() {
    try {
        const data = fs.readFileSync('dispositivos_scan.csv', 'utf8');
        const dispositivos = data.trim().split('\n').map(line => {
            const [ip, mac] = line.split(',');
            return { ip, mac, timestamp: new Date().toISOString() };
        });
        console.table(dispositivos);
        return dispositivos;
    } catch (err) {
        console.error("Error: Asegúrate de que 'dispositivos_scan.csv' exista.", err.message);
    }
}

obtenerDispositivos();
