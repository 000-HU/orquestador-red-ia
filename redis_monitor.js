import { createClient } from 'redis';

const client = createClient({
    url: 'redis://127.0.0.1:6379'
});

client.on('error', (err) => console.error('[-] Error en el cliente de Redis:', err));

async function iniciarMonitor() {
    await client.connect();
    console.log('[+] Sincronizado con el buffer de Redis Iris (127.0.0.1:6379)');
    console.log('[*] Escuchando eventos y telemetría en tiempo real...\n');

    // Bucle persistente para extraer los datos asíncronos en paralelo
    while (true) {
        try {
            // Realiza un bloqueo de lectura (BLPOP) esperando datos en la lista
            const resultado = await client.blPop('telemetry_stream', 0);
            if (resultado) {
                console.log(`[🚨 EVENTO DETECTADO] Clave: ${resultado.key}`);
                console.log(`[DATA]: ${resultado.element}\n`);
            }
        } catch (error) {
            console.error('[-] Error durante el monitoreo de la memoria:', error);
            break;
        }
    }
}

iniciarMonitor();

