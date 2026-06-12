const { exec } = require('child_process');
const path = require('path');

console.log('🤖 [Sistema Zero] Iniciando auditoría global automatizada...');

const rutaApp = path.join(__dirname, 'app.js');

exec(`node "${rutaApp}"`, (error, stdout, stderr) => {
    if (error) {
        console.error(`❌ Error al ejecutar el detector de anomalías: ${error.message}`);
        return;
    }
    if (stderr) {
        console.error(`⚠️ Advertencia en el script: ${stderr}`);
        return;
    }
    console.log(stdout);
    console.log('✅ [Sistema Zero] Auditoría de red finalizada exitosamente.');
});
