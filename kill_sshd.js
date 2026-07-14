import { exec } from 'child_process';

console.log('[*] Iniciando detención del servicio en memoria...');

// Comando nativo para detener el servicio de forma inmediata
exec('net stop sshd', (error, stdout, stderr) => {
    if (error) {
        if (error.message.includes('Access is denied') || error.message.includes('acceso denegado')) {
            console.error('[-] Error: Se requieren privilegios de Administrador.');
            console.log('[*] Intenta ejecutar tu consola como Administrador.');
        } else {
            console.error(`[-] Error al detener el servicio: ${error.message}`);
        }
        return;
    }
    if (stderr) {
        console.error(`[-] Stderr: ${stderr}`);
        return;
    }
    console.log(`[+] Resultado del SCM:\n${stdout}`);
});
