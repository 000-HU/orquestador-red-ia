const { exec } = require('child_process');

exec('wmic process where name="librewolf.exe" get ProcessId, ThreadCount', (err, stdout, stderr) => {
    if (err) {
        console.error(`[-] Error al ejecutar la auditoría: ${err.message}`);
        return;
    }
    
    console.log("================================================");
    console.log("   AUDITORÍA DE HILOS ACTIVOS (LIBREWOLF)       ");
    console.log("================================================");
    console.log(stdout.trim());
});
